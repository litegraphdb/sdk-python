import uuid
from datetime import datetime, timezone

import pytest
from litegraph.models.edge import EdgeModel
from pydantic import ValidationError
from litegraph.resources.edges import Edge
from litegraph.models.enumeration_result import EnumerationResultModel
from unittest.mock import Mock


@pytest.fixture
def mock_client(monkeypatch):
    """Create a mock client and configure it."""
    client = Mock()
    client.base_url = "http://test-api.com"
    monkeypatch.setattr("litegraph.configuration._client", client)
    return client


@pytest.fixture
def valid_edge_data():
    """Fixture providing valid edge data."""
    return {
        "guid": str(uuid.uuid4()),
        "graph_guid": str(uuid.uuid4()),
        "name": "Test Edge",
        "from_node_guid": str(uuid.uuid4()),
        "to_node_guid": str(uuid.uuid4()),
        "cost": 100,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "data": {"key": "value"},
    }


@pytest.fixture
def minimal_edge_data():
    """Fixture providing minimal valid edge data."""
    return {"guid": str(uuid.uuid4()), "graph_guid": str(uuid.uuid4())}


def test_valid_edge_creation(valid_edge_data):
    """Test creating an edge with valid data."""
    edge = EdgeModel(**valid_edge_data)
    assert edge.guid == valid_edge_data["guid"]
    assert edge.graph_guid == valid_edge_data["graph_guid"]
    assert edge.name == valid_edge_data["name"]
    assert edge.from_node_guid == valid_edge_data["from_node_guid"]
    assert edge.to_node_guid == valid_edge_data["to_node_guid"]
    assert edge.cost == valid_edge_data["cost"]
    assert isinstance(edge.created_utc, datetime)
    assert edge.data == valid_edge_data["data"]


def test_minimal_edge_creation(minimal_edge_data):
    """Test creating an edge with minimal required data."""
    edge = EdgeModel(**minimal_edge_data)
    assert edge.guid == minimal_edge_data["guid"]
    assert edge.graph_guid == minimal_edge_data["graph_guid"]
    assert edge.name is None
    assert edge.from_node_guid == str(uuid.UUID(int=0))  # Default value
    assert edge.to_node_guid == str(uuid.UUID(int=0))  # Default value
    assert edge.cost == 0  # Default value
    assert isinstance(edge.created_utc, datetime)
    assert edge.data is None


def test_auto_generated_fields():
    """Test auto-generated fields when creating edge without required fields."""
    edge = EdgeModel()
    assert isinstance(edge.guid, str)
    uuid.UUID(edge.guid)  # Validates UUID format
    assert isinstance(edge.graph_guid, str)
    uuid.UUID(edge.graph_guid)  # Validates UUID format
    assert isinstance(edge.created_utc, datetime)
    assert edge.created_utc.tzinfo == timezone.utc


def test_default_values():
    """Test default values for fields."""
    edge = EdgeModel(GUID=str(uuid.uuid4()), GraphGUID=str(uuid.uuid4()))
    assert edge.from_node_guid == str(uuid.UUID(int=0))
    assert edge.to_node_guid == str(uuid.UUID(int=0))
    assert edge.cost == 0
    assert edge.name is None
    assert edge.data is None


def test_cost_validation():
    """Test cost field validation."""
    # Test valid costs
    valid_costs = [0, 1, 100]
    for cost in valid_costs:
        edge = EdgeModel(GUID=str(uuid.uuid4()), GraphGUID=str(uuid.uuid4()), Cost=cost)
        assert edge.cost == cost

    # Test invalid cost type
    with pytest.raises(ValidationError):
        EdgeModel(GUID=str(uuid.uuid4()), GraphGUID=str(uuid.uuid4()), Cost="invalid")


def test_node_guid_validation():
    """Test validation of From and To node GUIDs."""
    test_data = {
        "GUID": str(uuid.uuid4()),
        "GraphGUID": str(uuid.uuid4()),
    }

    # Test valid UUID strings
    valid_guid = str(uuid.uuid4())
    edge = EdgeModel(**test_data, From=valid_guid, To=valid_guid)
    assert edge.from_node_guid == valid_guid
    assert edge.to_node_guid == valid_guid


def test_data_field_validation():
    """Test validation of the Data field."""
    valid_data_cases = [
        {"key": "value"},
        {"numbers": [1, 2, 3]},
        {"nested": {"key": "value"}},
        None,
    ]

    for data in valid_data_cases:
        edge = EdgeModel(GUID=str(uuid.uuid4()), GraphGUID=str(uuid.uuid4()), Data=data)
        assert edge.data == data


def test_created_utc_validation():
    """Test CreatedUtc field validation."""
    # Test valid datetime formats
    valid_dates = [datetime.now(timezone.utc), datetime.now(timezone.utc).isoformat()]

    for date in valid_dates:
        edge = EdgeModel(
            GUID=str(uuid.uuid4()), GraphGUID=str(uuid.uuid4()), CreatedUtc=date
        )
        assert isinstance(edge.created_utc, datetime)
        assert edge.created_utc.tzinfo == timezone.utc

    # Test invalid datetime formats
    invalid_dates = ["not-a-date", "2024-99-99", {"date": "2024-01-01"}]

    for date in invalid_dates:
        with pytest.raises(ValidationError):
            EdgeModel(
                GUID=str(uuid.uuid4()), GraphGUID=str(uuid.uuid4()), CreatedUtc=date
            )


def test_model_export():
    """Test model serialization."""
    test_data = {
        "guid": str(uuid.uuid4()),
        "graph_guid": str(uuid.uuid4()),
        "name": "Test Edge",
        "from_node_guid": str(uuid.uuid4()),
        "to_node_guid": str(uuid.uuid4()),
        "cost": 100,
        "data": {"key": "value"},
    }

    edge = EdgeModel(**test_data)
    exported = edge.model_dump(by_alias=True)

    assert exported["GUID"] == test_data["guid"]
    assert exported["GraphGUID"] == test_data["graph_guid"]
    assert exported["Name"] == test_data["name"]
    assert exported["From"] == test_data["from_node_guid"]
    assert exported["To"] == test_data["to_node_guid"]
    assert exported["Cost"] == test_data["cost"]
    assert exported["Data"] == test_data["data"]
    assert "CreatedUtc" in exported


@pytest.mark.parametrize(
    "field,value,valid",
    [
        pytest.param("guid", str(uuid.uuid4()), True, id="valid_guid"),
        pytest.param("graph_guid", str(uuid.uuid4()), True, id="valid_graph_guid"),
        pytest.param("name", "Test Edge", True, id="valid_name"),
        pytest.param("name", None, True, id="null_name"),
        pytest.param("from_node_guid", str(uuid.uuid4()), True, id="valid_from_node"),
        pytest.param("to_node_guid", str(uuid.uuid4()), True, id="valid_to_node"),
        pytest.param("cost", 100, True, id="valid_cost"),
        pytest.param("cost", "invalid", False, id="invalid_cost"),
        pytest.param("data", {"key": "value"}, True, id="valid_data"),
        pytest.param("data", None, True, id="null_data"),
    ],
)
def test_field_validation(field, value, valid):
    """Test field validation with various inputs."""
    test_data = {"guid": str(uuid.uuid4()), "graph_guid": str(uuid.uuid4())}
    test_data[field] = value

    if valid:
        edge = EdgeModel(**test_data)
        assert getattr(edge, field) == value
    else:
        with pytest.raises(ValidationError):
            EdgeModel(**test_data)


def test_model_config():
    """Test model configuration."""
    test_guid = str(uuid.uuid4())
    test_graph_guid = str(uuid.uuid4())

    # Test using Python attribute names
    edge = EdgeModel(
        **{"guid": test_guid, "graph_guid": test_graph_guid, "name": "Test Edge"}
    )

    assert edge.guid == test_guid
    assert edge.graph_guid == test_graph_guid
    assert edge.name == "Test Edge"

    # Test serialization with aliases
    exported = edge.model_dump(by_alias=True)
    assert "GUID" in exported
    assert "GraphGUID" in exported
    assert "Name" in exported


def test_edge_enumerate_with_query(mock_client):
    """Test enumerating edges with a query."""
    mock_response = {
        "Success": True,
        "MaxResults": 25,
        "IterationsRequired": 1,
        "ContinuationToken": None,
        "EndOfResults": True,
        "TotalRecords": 2,
        "RecordsRemaining": 0,
        "Objects": [
            {
                "GUID": "edge1", 
                "Name": "Edge 1", 
                "TenantGUID": "tenant1", 
                "GraphGUID": "graph1",
                "From": "node1",
                "To": "node2"
            },
            {
                "GUID": "edge2", 
                "Name": "Edge 2", 
                "TenantGUID": "tenant1", 
                "GraphGUID": "graph1",
                "From": "node2",
                "To": "node3"
            }
        ],
        "Timestamp": {
            "Start": "2023-01-01T00:00:00Z",
            "End": "2023-01-01T00:00:01Z",
            "TotalMS": 300.0,
            "Messages": {},
            "Metadata": None
        }
    }
    mock_client.request.return_value = mock_response
    
    from litegraph.models.expression import ExprModel
    from litegraph.enums.operator_enum import Opertator_Enum
    
    result = Edge.enumerate_with_query(
        max_results=25,
        include_data=True,
        labels=["EdgeLabel"],
        expr=ExprModel(Left="field", Operator=Opertator_Enum.Equals, Right="value")
    )
    
    assert isinstance(result, EnumerationResultModel)
    assert result.success is True
    assert result.total_records == 2
    assert len(result.objects) == 2
    assert result.max_results == 25
    mock_client.request.assert_called_once()


def test_edge_enumerate_with_query_pagination(mock_client):
    """Test edge enumeration with pagination."""
    mock_response = {
        "Success": True,
        "MaxResults": 1,
        "IterationsRequired": 1,
        "ContinuationToken": "next_page_token",
        "EndOfResults": False,
        "TotalRecords": 5,
        "RecordsRemaining": 4,
        "Objects": [
            {
                "GUID": "edge1", 
                "Name": "Edge 1", 
                "TenantGUID": "tenant1", 
                "GraphGUID": "graph1",
                "From": "node1",
                "To": "node2"
            }
        ],
        "Timestamp": {
            "Start": "2023-01-01T00:00:00Z",
            "End": "2023-01-01T00:00:01Z",
            "TotalMS": 150.0,
            "Messages": {},
            "Metadata": None
        }
    }
    mock_client.request.return_value = mock_response
    
    from litegraph.models.expression import ExprModel
    from litegraph.enums.operator_enum import Opertator_Enum
    
    result = Edge.enumerate_with_query(
        max_results=1,
        expr=ExprModel(Left="field", Operator=Opertator_Enum.Equals, Right="value")
    )
    
    assert isinstance(result, EnumerationResultModel)
    assert result.success is True
    assert result.total_records == 5
    assert result.records_remaining == 4
    assert result.continuation_token == "next_page_token"
    assert result.end_of_results is False
    assert len(result.objects) == 1
    mock_client.request.assert_called_once()
