from datetime import datetime, timezone
import pytest
from unittest.mock import Mock

from litegraph.models.tag import TagModel
from litegraph.models.expression import ExprModel
from litegraph.enums.operator_enum import Opertator_Enum
from litegraph.resources.tags import Tag


@pytest.fixture
def mock_client(monkeypatch):
    """Create a mock client and configure it."""
    client = Mock()
    client.base_url = "http://test-api.com"
    client.tenant_guid = "test-tenant-guid"
    client.graph_guid = "test-graph-guid"
    monkeypatch.setattr("litegraph.configuration._client", client)
    return client


@pytest.fixture
def valid_tag_data():
    """Fixture providing valid tag data."""
    return {
        "GUID": "550e8400-e29b-41d4-a716-446655440000",
        "TenantGUID": "550e8400-e29b-41d4-a716-446655440001",
        "GraphGUID": "550e8400-e29b-41d4-a716-446655440002",
        "Key": "test-key",
        "Value": "test-value",
        "CreatedUtc": "2024-01-01T00:00:00+00:00",
        "LastUpdateUtc": "2024-01-01T00:00:00+00:00",
    }


def test_retrieve_all_tenant_tags(mock_client, valid_tag_data):
    """Test retrieve_all_tenant_tags method."""
    test_data = [
        {**valid_tag_data, "GUID": "tag-1", "Key": "key1", "Value": "value1"},
        {**valid_tag_data, "GUID": "tag-2", "Key": "key2", "Value": "value2"},
    ]
    mock_client.request.return_value = test_data
    mock_client.request.side_effect = None

    result = Tag.retrieve_all_tenant_tags()
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(item, TagModel) for item in result)
    assert result[0].guid == "tag-1"
    assert result[1].guid == "tag-2"

    # Test with explicit tenant_guid
    mock_client.request.reset_mock()
    mock_client.request.return_value = test_data
    result = Tag.retrieve_all_tenant_tags(tenant_guid="explicit-tenant")
    assert isinstance(result, list)
    assert len(result) == 2


def test_retrieve_all_graph_tags(mock_client, valid_tag_data):
    """Test retrieve_all_graph_tags method."""
    test_data = [
        {**valid_tag_data, "GUID": "tag-1", "Key": "key1", "Value": "value1"},
        {**valid_tag_data, "GUID": "tag-2", "Key": "key2", "Value": "value2"},
    ]
    mock_client.request.return_value = test_data
    mock_client.request.side_effect = None

    result = Tag.retrieve_all_graph_tags("test-tenant", "test-graph")
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(item, TagModel) for item in result)
    assert result[0].guid == "tag-1"
    assert result[1].guid == "tag-2"

    # Verify the request was made correctly
    mock_client.request.assert_called_once()
    called_args = mock_client.request.call_args
    assert called_args[0][0] == "GET"
    assert "graphs/test-graph/tags/all" in called_args[0][1]


def test_retrieve_node_tags(mock_client, valid_tag_data):
    """Test retrieve_node_tags method."""
    test_data = [
        {
            **valid_tag_data,
            "GUID": "tag-1",
            "NodeGUID": "node-guid-123",
            "Key": "key1",
            "Value": "value1",
        },
    ]
    mock_client.request.return_value = test_data
    mock_client.request.side_effect = None

    result = Tag.retrieve_node_tags("test-tenant", "test-graph", "node-guid-123")
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], TagModel)
    assert result[0].guid == "tag-1"
    assert result[0].node_guid == "node-guid-123"

    # Verify the request was made correctly
    mock_client.request.assert_called_once()
    called_args = mock_client.request.call_args
    assert called_args[0][0] == "GET"
    assert "nodes/node-guid-123/tags" in called_args[0][1]


def test_retrieve_edge_tags(mock_client, valid_tag_data):
    """Test retrieve_edge_tags method."""
    test_data = [
        {
            **valid_tag_data,
            "GUID": "tag-1",
            "EdgeGUID": "edge-guid-123",
            "Key": "key1",
            "Value": "value1",
        },
    ]
    mock_client.request.return_value = test_data
    mock_client.request.side_effect = None

    result = Tag.retrieve_edge_tags("test-tenant", "test-graph", "edge-guid-123")
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], TagModel)
    assert result[0].guid == "tag-1"
    assert result[0].edge_guid == "edge-guid-123"

    # Verify the request was made correctly
    mock_client.request.assert_called_once()
    called_args = mock_client.request.call_args
    assert called_args[0][0] == "GET"
    assert "edges/edge-guid-123/tags" in called_args[0][1]


def test_delete_all_tenant_tags(mock_client):
    """Test delete_all_tenant_tags method."""
    mock_client.request.return_value = None
    mock_client.request.side_effect = None

    Tag.delete_all_tenant_tags("test-tenant")
    mock_client.request.assert_called_once()
    called_args = mock_client.request.call_args
    assert called_args[0][0] == "DELETE"
    assert "tenants/test-tenant/tags/all" in called_args[0][1]


def test_delete_all_graph_tags(mock_client):
    """Test delete_all_graph_tags method."""
    mock_client.request.return_value = None
    mock_client.request.side_effect = None

    Tag.delete_all_graph_tags("test-tenant", "test-graph")
    mock_client.request.assert_called_once()
    called_args = mock_client.request.call_args
    assert called_args[0][0] == "DELETE"
    assert "graphs/test-graph/tags/all" in called_args[0][1]


def test_delete_graph_tags(mock_client):
    """Test delete_graph_tags method."""
    mock_client.request.return_value = None
    mock_client.request.side_effect = None

    Tag.delete_graph_tags("test-tenant", "test-graph")
    mock_client.request.assert_called_once()
    called_args = mock_client.request.call_args
    assert called_args[0][0] == "DELETE"
    assert "graphs/test-graph/tags" in called_args[0][1]
    assert called_args[1]["headers"] == {"Content-Type": "application/json"}


def test_delete_node_tags(mock_client):
    """Test delete_node_tags method."""
    mock_client.request.return_value = None
    mock_client.request.side_effect = None

    Tag.delete_node_tags("test-tenant", "test-graph", "node-guid-123")
    mock_client.request.assert_called_once()
    called_args = mock_client.request.call_args
    assert called_args[0][0] == "DELETE"
    assert "nodes/node-guid-123/tags" in called_args[0][1]
    assert called_args[1]["headers"] == {"Content-Type": "application/json"}


def test_delete_edge_tags(mock_client):
    """Test delete_edge_tags method."""
    mock_client.request.return_value = None
    mock_client.request.side_effect = None

    Tag.delete_edge_tags("test-tenant", "test-graph", "edge-guid-123")
    mock_client.request.assert_called_once()
    called_args = mock_client.request.call_args
    assert called_args[0][0] == "DELETE"
    assert "edges/edge-guid-123/tags" in called_args[0][1]
    assert called_args[1]["headers"] == {"Content-Type": "application/json"}


def test_tag_model_validation(valid_tag_data):
    """Test TagModel validation."""
    model = TagModel(**valid_tag_data)
    assert isinstance(model.guid, str)
    assert isinstance(model.tenant_guid, str)
    assert model.graph_guid == valid_tag_data["GraphGUID"]
    assert model.key == valid_tag_data["Key"]
    assert model.value == valid_tag_data["Value"]
    assert model.created_utc == datetime.fromisoformat(valid_tag_data["CreatedUtc"])
    assert model.last_update_utc == datetime.fromisoformat(
        valid_tag_data["LastUpdateUtc"]
    )


def test_enumerate_with_query(mock_client):
    """Test enumerate_with_query method."""
    mock_client.request.return_value = {
        "Objects": [
            {
                "GUID": "tag-1",
                "TenantGUID": "test-tenant",
                "Key": "key1",
                "Value": "value1",
            }
        ],
        "TotalRecords": 1,
        "Success": True,
        "Timestamp": {
            "Start": datetime.now(timezone.utc).isoformat(),
            "End": None,
            "Messages": {},
            "Metadata": None,
        },
        "MaxResults": 1000,
        "IterationsRequired": 0,
        "ContinuationToken": None,
        "EndOfResults": True,
        "RecordsRemaining": 0,
    }
    mock_client.request.side_effect = None

    # Test with valid EnumerationQueryModel parameters
    # Provide a valid expr to avoid ExprModel validation errors
    valid_expr = ExprModel(Left="Key", Operator=Opertator_Enum.Equals, Right="test-key")
    result = Tag.enumerate_with_query(
        labels=["label1"], tags={"key1": "value1"}, expr=valid_expr
    )
    assert result is not None
    assert hasattr(result, "objects")
    assert hasattr(result, "total_records")
    assert len(result.objects) == 1
    assert result.total_records == 1

