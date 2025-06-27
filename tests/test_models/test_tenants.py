import uuid
from datetime import datetime, timezone
from unittest.mock import Mock, patch

import pytest
from litegraph.models.tenant_metadata import TenantMetadataModel
from litegraph.resources.tenants import Tenant
from litegraph.models.tenant_statistics import TenantStatisticsModel
from litegraph.models.enumeration_result import EnumerationResultModel


@pytest.fixture
def valid_tenant_data():
    """Fixture providing valid tenant data."""
    return {
        "GUID": str(uuid.uuid4()),
        "Name": "Test Tenant",
        "CreatedUtc": datetime.now(timezone.utc).isoformat(),
        "Data": {"key": "value"},
    }


@pytest.fixture
def minimal_tenant_data():
    """Fixture providing minimal valid tenant data."""
    return {"GUID": str(uuid.uuid4())}


@pytest.fixture
def mock_client(monkeypatch):
    """Create a mock client and configure it."""
    client = Mock()
    client.base_url = "http://test-api.com"
    monkeypatch.setattr("litegraph.configuration._client", client)
    return client


class TestTenantMetadataModel:
    def test_valid_tenant_creation(self, valid_tenant_data):
        """Test creating a tenant with valid data."""
        tenant = TenantMetadataModel(**valid_tenant_data)
        assert tenant.guid == valid_tenant_data["GUID"]
        assert tenant.name == valid_tenant_data["Name"]
        assert isinstance(tenant.created_utc, datetime)

    def test_minimal_tenant_creation(self, minimal_tenant_data):
        """Test creating a tenant with minimal required data."""
        tenant = TenantMetadataModel(**minimal_tenant_data)
        assert tenant.guid == minimal_tenant_data["GUID"]
        assert tenant.name is None
        assert isinstance(tenant.created_utc, datetime)

    def test_auto_generated_fields(self):
        """Test auto-generated fields when creating tenant."""
        tenant = TenantMetadataModel()
        assert isinstance(tenant.created_utc, datetime)
        assert tenant.created_utc.tzinfo == timezone.utc

    def test_model_export(self):
        """Test model serialization."""
        test_data = {
            "GUID": str(uuid.uuid4()),
            "Name": "Test Tenant",
        }

        tenant = TenantMetadataModel(**test_data)
        exported = tenant.model_dump(by_alias=True)

        assert exported["GUID"] == test_data["GUID"]
        assert exported["Name"] == test_data["Name"]
        assert "CreatedUtc" in exported


class TestTenantResource:
    def test_delete_tenant(self, mock_client):
        """Test deleting a tenant."""
        # Test normal deletion
        Tenant.delete("test-guid")
        mock_client.request.assert_called_once_with(
            "DELETE", "v1.0/tenants/test-guid"
        )

        # Test force deletion
        mock_client.request.reset_mock()
        Tenant.delete("test-guid", force=True)
        mock_client.request.assert_called_once_with(
            "DELETE", "v1.0/tenants/test-guid?force"
        )

    def test_tenant_exists(self, mock_client):
        """Test checking if a tenant exists."""
        mock_client.request.return_value = True
        result = Tenant.exists("test-guid")
        assert result is True
        mock_client.request.assert_called_once()

    def test_retrieve_tenant(self, mock_client, valid_tenant_data):
        """Test retrieving a tenant."""
        mock_client.request.return_value = valid_tenant_data
        tenant = Tenant.retrieve("test-guid")
        assert isinstance(tenant, TenantMetadataModel)
        assert tenant.guid == valid_tenant_data["GUID"]
        mock_client.request.assert_called_once()

    def test_retrieve_all_tenants(self, mock_client, valid_tenant_data):
        """Test retrieving all tenants."""
        mock_client.request.return_value = [valid_tenant_data]
        tenants = Tenant.retrieve_all()
        assert isinstance(tenants, list)
        assert len(tenants) == 1
        assert isinstance(tenants[0], TenantMetadataModel)
        mock_client.request.assert_called_once()

    def test_create_tenant(self, mock_client, valid_tenant_data):
        """Test creating a tenant."""
        mock_client.request.return_value = valid_tenant_data
        tenant = Tenant.create(name="Test Tenant", data={"key": "value"})
        assert isinstance(tenant, TenantMetadataModel)
        assert tenant.name == valid_tenant_data["Name"]
        mock_client.request.assert_called_once()

    def test_update_tenant(self, mock_client, valid_tenant_data):
        """Test updating a tenant."""
        mock_client.request.return_value = valid_tenant_data
        tenant = Tenant.update("test-guid", name="Updated Tenant")
        assert isinstance(tenant, TenantMetadataModel)
        assert tenant.name == valid_tenant_data["Name"]
        mock_client.request.assert_called_once()

    @pytest.mark.parametrize(
        "field,value,expected_type",
        [
            ("name", "Test Tenant", str),
            ("name", None, type(None)),
            ("created_utc", datetime.now(timezone.utc), datetime),
        ],
    )
    def test_field_types(self, field, value, expected_type):
        """Test field type validation."""
        tenant = TenantMetadataModel(GUID=str(uuid.uuid4()), **{field: value})
        assert isinstance(getattr(tenant, field), expected_type)


def test_tenant_statistics_model_defaults():
    stats = TenantStatisticsModel()
    assert stats.graphs == 0
    assert stats.nodes == 0
    assert stats.edges == 0
    assert stats.labels == 0
    assert stats.tags == 0
    assert stats.vectors == 0


def test_tenant_statistics_model_custom_values():
    stats = TenantStatisticsModel(graphs=2, nodes=5, edges=10, labels=2, tags=3, vectors=7)
    assert stats.graphs == 2
    assert stats.nodes == 5
    assert stats.edges == 10
    assert stats.labels == 2
    assert stats.tags == 3
    assert stats.vectors == 7


def test_tenant_enumerate_with_query(mock_client):
    """Test enumerating tenants with a query."""
    mock_response = {
        "Success": True,
        "MaxResults": 100,
        "IterationsRequired": 1,
        "ContinuationToken": None,
        "EndOfResults": True,
        "TotalRecords": 2,
        "RecordsRemaining": 0,
        "Objects": [
            {"GUID": "tenant1", "Name": "Tenant 1"},
            {"GUID": "tenant2", "Name": "Tenant 2"}
        ],
        "Timestamp": {
            "Start": "2023-01-01T00:00:00Z",
            "End": "2023-01-01T00:00:01Z",
            "TotalMS": 1000.0,
            "Messages": {},
            "Metadata": None
        }
    }
    mock_client.request.return_value = mock_response
    
    from litegraph.models.expression import ExprModel
    from litegraph.enums.operator_enum import Opertator_Enum
    
    result = Tenant.enumerate_with_query(
        max_results=100, 
        include_data=True,
        expr=ExprModel(Left="field", Operator=Opertator_Enum.Equals, Right="value")
    )
    
    assert isinstance(result, EnumerationResultModel)
    assert result.success is True
    assert result.total_records == 2
    assert len(result.objects) == 2
    mock_client.request.assert_called_once()


def test_tenant_retrieve_statistics_single(mock_client):
    """Test retrieving statistics for a single tenant."""
    mock_response = {
        "Graphs": 3,
        "Nodes": 10,
        "Edges": 15,
        "Labels": 3,
        "Tags": 5,
        "Vectors": 2
    }
    mock_client.request.return_value = mock_response
    
    result = Tenant.retrieve_statistics("test-tenant-guid")
    
    assert isinstance(result, TenantStatisticsModel)
    assert result.graphs == 3
    assert result.nodes == 10
    assert result.edges == 15
    assert result.labels == 3
    assert result.tags == 5
    assert result.vectors == 2
    mock_client.request.assert_called_once()


def test_tenant_retrieve_statistics_all(mock_client):
    """Test retrieving statistics for all tenants."""
    mock_response = {
        "tenant1": {"Graphs": 3, "Nodes": 10, "Edges": 15, "Labels": 3, "Tags": 5, "Vectors": 2},
        "tenant2": {"Graphs": 1, "Nodes": 5, "Edges": 8, "Labels": 1, "Tags": 2, "Vectors": 1}
    }
    mock_client.request.return_value = mock_response
    
    result = Tenant.retrieve_statistics()
    
    assert isinstance(result, dict)
    assert len(result) == 2
    assert isinstance(result["tenant1"], TenantStatisticsModel)
    assert isinstance(result["tenant2"], TenantStatisticsModel)
    assert result["tenant1"].graphs == 3
    assert result["tenant2"].graphs == 1
    mock_client.request.assert_called_once()
