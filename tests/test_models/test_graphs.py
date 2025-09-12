import uuid
from datetime import datetime, timezone
from unittest.mock import Mock, patch

import pytest
from litegraph.models.existence_request import ExistenceRequestModel
from litegraph.models.existence_result import ExistenceResultModel
from litegraph.models.graphs import GraphModel
from litegraph.resources.graphs import Graph
from pydantic import ValidationError
from litegraph.models.graph_statistics import GraphStatisticsModel


@pytest.fixture
def mock_client(monkeypatch):
    """Create a mock client and configure it."""
    client = Mock()
    client.graph_guid = "test-graph-guid"
    client.base_url = "http://test-api.com"
    monkeypatch.setattr("litegraph.configuration._client", client)
    return client


@pytest.fixture
def valid_graph_data():
    """Fixture providing valid graph data."""
    return {
        "GUID": str(uuid.uuid4()),
        "Name": "Test Graph",
        "CreatedUtc": datetime.now(timezone.utc).isoformat(),
        "Data": {"key": "value"},
    }


@pytest.fixture
def minimal_graph_data():
    """Fixture providing minimal valid graph data."""
    return {"GUID": str(uuid.uuid4())}


def test_valid_graph_creation(valid_graph_data):
    """Test creating a graph with valid data."""
    graph = GraphModel(**valid_graph_data)
    assert graph.guid == valid_graph_data["GUID"]
    assert graph.name == valid_graph_data["Name"]
    assert isinstance(graph.created_utc, datetime)
    assert graph.data == valid_graph_data["Data"]


def test_minimal_graph_creation(minimal_graph_data):
    """Test creating a graph with minimal required data."""
    graph = GraphModel(**minimal_graph_data)
    assert graph.guid == minimal_graph_data["GUID"]
    assert graph.name is None
    assert isinstance(graph.created_utc, datetime)
    assert graph.data is None


def test_auto_generated_guid():
    """Test that GUID is auto-generated if not provided."""
    graph = GraphModel()
    assert graph.guid is not None
    assert isinstance(graph.guid, str)

    uuid.UUID(graph.guid)


def test_auto_generated_created_utc():
    """Test that CreatedUtc is auto-generated if not provided."""
    graph = GraphModel()
    assert isinstance(graph.created_utc, datetime)
    assert graph.created_utc.tzinfo == timezone.utc


def test_strict_type_validation():
    """Test that strict type validation works for GUID."""
    with pytest.raises(ValidationError):
        GraphModel(GUID=123)  # Should fail because strict=True requires string


def test_data_validation():
    """Test validation of the Data field."""
    valid_data_cases = [
        {"key": "value"},
        {"numbers": [1, 2, 3]},
        {"nested": {"key": "value"}},
        None,
    ]

    for data in valid_data_cases:
        graph = GraphModel(GUID=str(uuid.uuid4()), Data=data)
        assert graph.data == data


def test_name_validation():
    """Test validation of the Name field."""
    valid_names = ["Test Graph", "Graph 123", None, ""]

    for name in valid_names:
        graph = GraphModel(GUID=str(uuid.uuid4()), Name=name)
        assert graph.name == name


def test_model_export():
    """Test exporting the model to dict/json."""
    test_guid = str(uuid.uuid4())
    graph = GraphModel(
        **{"GUID": test_guid, "Name": "Test Graph", "Data": {"key": "value"}}
    )

    exported = graph.model_dump(by_alias=True)
    assert exported["GUID"] == test_guid
    assert exported["Name"] == "Test Graph"
    assert exported["Data"] == {"key": "value"}
    assert "CreatedUtc" in exported


def test_created_utc_format():
    """Test CreatedUtc field format and validation."""
    test_dates = [datetime.now(timezone.utc), datetime.now(timezone.utc).isoformat()]

    for date in test_dates:
        graph = GraphModel(GUID=str(uuid.uuid4()), CreatedUtc=date)
        assert isinstance(graph.created_utc, datetime)
        assert graph.created_utc.tzinfo == timezone.utc


def test_invalid_created_utc():
    """Test that invalid CreatedUtc format raises validation error."""
    invalid_dates = [
        "not-a-date",
        "2024-99-99",  # Invalid date
        {"date": "2024-01-01"},  # Wrong type
    ]

    for date in invalid_dates:
        with pytest.raises(ValidationError):
            GraphModel(GUID=str(uuid.uuid4()), CreatedUtc=date)


def test_model_config():
    """Test model configuration options."""
    test_guid = str(uuid.uuid4())
    graph = GraphModel(
        **{
            "guid": test_guid,  # Using Python attribute name
            "name": "Test Graph",
        }
    )

    # Test that populate_by_name works
    assert graph.guid == test_guid
    assert graph.name == "Test Graph"

    # Test serialization with aliases
    exported = graph.model_dump(by_alias=True)
    assert "GUID" in exported
    assert "Name" in exported


@pytest.mark.parametrize(
    "field,value,valid",
    [
        pytest.param("GUID", str(uuid.uuid4()), True, id="valid_guid"),
        pytest.param("GUID", 123, False, id="invalid_guid_type"),
        pytest.param("Name", "Valid Name", True, id="valid_name"),
        pytest.param("Name", None, True, id="null_name"),
        pytest.param("Data", {"key": "value"}, True, id="valid_data"),
        pytest.param("Data", None, True, id="null_data"),
    ],
)
def test_field_validation(field, value, valid):
    """Test field validation with various inputs."""
    test_data = {"GUID": str(uuid.uuid4())}
    if field != "GUID":
        test_data[field] = value
    else:
        test_data["GUID"] = value

    if valid:
        graph = GraphModel(**test_data)
        assert getattr(graph, field.lower()) == value
    else:
        with pytest.raises(ValidationError):
            GraphModel(**test_data)


# def test_delete_graph_resource(mock_client):
#     """Test delete method of the Graph class."""
#     mock_client.request.side_effect = None

#     # Test successful deletion
#     graph_id = "test-resource-id"
#     Graph.delete(resource_id=graph_id)
#     mock_client.request.assert_called_once()
#     called_args = mock_client.request.call_args
#     assert called_args[0][0] == "DELETE"
#     assert graph_id in called_args[0][1]

#     # Test deletion with force flag
#     mock_client.request.reset_mock()
#     Graph.delete(resource_id=graph_id, force=True)
#     mock_client.request.assert_called_once()
#     called_args = mock_client.request.call_args
#     assert called_args[0][0] == "DELETE"
#     assert graph_id in called_args[0][1]

#     # Test without graph_guid when required
#     mock_client.request.reset_mock()
#     Graph.REQUIRE_GRAPH_GUID = True
#     mock_client.graph_guid = None
#     with pytest.raises(ValueError, match="Graph GUID is required for this resource"):
#         Graph.delete(resource_id=graph_id)
#     Graph.REQUIRE_GRAPH_GUID = False  # Reset the flag after the test


def test_batch_existence(mock_client):
    """Test batch_existence method of the Graph class."""
    mock_client.request.side_effect = None

    # Test with a valid request
    valid_request = Mock(spec=ExistenceRequestModel)
    valid_request.contains_existence_request.return_value = True
    mock_client.request.return_value = {}

    graph_guid = "550e8400-e29b-41d4-a716-446655440000"
    with patch("litegraph.configuration._client", mock_client):
        response = Graph.batch_existence(graph_guid=graph_guid, request=valid_request)
    assert isinstance(response, ExistenceResultModel)

    # Test with None request (expect ValueError)
    with pytest.raises(ValueError, match="Request cannot be None"):
        Graph.batch_existence(graph_guid=graph_guid, request=None)

    # Test with invalid request type (expect TypeError)
    invalid_request = Mock()  # Not an instance of ExistenceRequestModel
    with pytest.raises(
        TypeError, match="Request must be an instance of ExistenceRequestModel"
    ):
        Graph.batch_existence(graph_guid=graph_guid, request=invalid_request)

    # Test with request missing existence checks (expect ValueError)
    valid_request.contains_existence_request.return_value = False
    with pytest.raises(
        ValueError, match="Request must contain at least one existence check"
    ):
        Graph.batch_existence(graph_guid=graph_guid, request=valid_request)


def test_graph_statistics_model_defaults():
    stats = GraphStatisticsModel()
    assert stats.nodes == 0
    assert stats.edges == 0
    assert stats.labels == 0
    assert stats.tags == 0
    assert stats.vectors == 0


def test_graph_statistics_model_custom_values():
    stats = GraphStatisticsModel(nodes=5, edges=10, labels=2, tags=3, vectors=7)
    assert stats.nodes == 5
    assert stats.edges == 10
    assert stats.labels == 2
    assert stats.tags == 3
    assert stats.vectors == 7


def test_graph_retrieve_statistics_single(mock_client):
    """Test retrieving statistics for a single graph."""
    mock_response = {
        "Nodes": 10,
        "Edges": 15,
        "Labels": 3,
        "Tags": 5,
        "Vectors": 2
    }
    mock_client.request.return_value = mock_response
    
    result = Graph.retrieve_statistics("test-graph-guid")
    
    assert isinstance(result, GraphStatisticsModel)
    assert result.nodes == 10
    assert result.edges == 15
    assert result.labels == 3
    assert result.tags == 5
    assert result.vectors == 2
    mock_client.request.assert_called_once()


def test_graph_retrieve_statistics_all(mock_client):
    """Test retrieving statistics for all graphs."""
    mock_response = {
        "graph1": {"Nodes": 10, "Edges": 15, "Labels": 3, "Tags": 5, "Vectors": 2},
        "graph2": {"Nodes": 5, "Edges": 8, "Labels": 1, "Tags": 2, "Vectors": 1}
    }
    mock_client.request.return_value = mock_response
    
    result = Graph.retrieve_statistics()
    
    assert isinstance(result, dict)
    assert len(result) == 2
    assert isinstance(result["graph1"], GraphStatisticsModel)
    assert isinstance(result["graph2"], GraphStatisticsModel)
    assert result["graph1"].nodes == 10
    assert result["graph2"].nodes == 5
    mock_client.request.assert_called_once()
