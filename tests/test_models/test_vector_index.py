from datetime import datetime, timezone
import pytest
from unittest.mock import Mock

from litegraph.enums.vector_index_type_enum import Vector_Index_Type_Enum
from litegraph.models.hnsw_lite_vector_index import HnswLiteVectorIndexModel
from litegraph.models.vector_index_statistics import VectorIndexStatisticsModel
from litegraph.resources.vector_index import VectorIndex


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
def valid_vector_index_config():
    """Fixture providing valid vector index configuration."""
    return {
        "GUID": "550e8400-e29b-41d4-a716-446655440000",
        "GraphGUID": "550e8400-e29b-41d4-a716-446655440002",
        "VectorDimensionality": 128,
        "VectorIndexType": Vector_Index_Type_Enum.HnswSqlite,
        "M": 16,
        "EfConstruction": 200,
        "DefaultEf": 50,
        "DistanceMetric": "Cosine",
        "VectorCount": 0,
        "IsLoaded": False,
    }


@pytest.fixture
def valid_vector_index_stats():
    """Fixture providing valid vector index statistics."""
    return {
        "VectorCount": 100,
        "Dimensions": 128,
        "IndexType": Vector_Index_Type_Enum.HnswSqlite,
        "M": 16,
        "EfConstruction": 200,
        "DefaultEf": 50,
        "IndexFile": "index.db",
        "IndexFileSizeBytes": 1024000,
        "EstimatedMemoryBytes": 512000,
        "IsLoaded": True,
        "DistanceMetric": "Cosine",
    }


def test_get_config(mock_client, valid_vector_index_config):
    """Test get_config method."""
    mock_client.request.return_value = valid_vector_index_config
    mock_client.request.side_effect = None

    result = VectorIndex.get_config("test-graph-guid")
    assert isinstance(result, HnswLiteVectorIndexModel)
    assert result.guid == valid_vector_index_config["GUID"]
    assert result.graph_guid == valid_vector_index_config["GraphGUID"]
    assert result.vector_dimensionality == valid_vector_index_config["VectorDimensionality"]
    assert result.m == valid_vector_index_config["M"]

    # Verify the request was made correctly
    mock_client.request.assert_called_once()
    called_args = mock_client.request.call_args
    assert called_args[0][0] == "GET"
    assert "vectorindex/config" in called_args[0][1]

    # Test without tenant_guid
    mock_client.tenant_guid = None
    with pytest.raises(ValueError, match="Tenant GUID is required for this resource"):
        VectorIndex.get_config("test-graph-guid")

    # Test without graph_guid
    mock_client.tenant_guid = "test-tenant-guid"
    with pytest.raises(ValueError, match="Graph GUID is required for this resource"):
        VectorIndex.get_config("")

    # Test with empty graph_guid
    with pytest.raises(ValueError, match="Graph GUID is required for this resource"):
        VectorIndex.get_config(None)


def test_get_stats(mock_client, valid_vector_index_stats):
    """Test get_stats method."""
    mock_client.request.return_value = valid_vector_index_stats
    mock_client.request.side_effect = None

    result = VectorIndex.get_stats("test-graph-guid")
    assert isinstance(result, VectorIndexStatisticsModel)
    assert result.vector_count == valid_vector_index_stats["VectorCount"]
    assert result.dimensions == valid_vector_index_stats["Dimensions"]
    assert result.index_type == valid_vector_index_stats["IndexType"]
    assert result.m == valid_vector_index_stats["M"]
    assert result.is_loaded == valid_vector_index_stats["IsLoaded"]

    # Verify the request was made correctly
    mock_client.request.assert_called_once()
    called_args = mock_client.request.call_args
    assert called_args[0][0] == "GET"
    assert "vectorindex/stats" in called_args[0][1]

    # Test without tenant_guid
    mock_client.tenant_guid = None
    with pytest.raises(ValueError, match="Tenant GUID is required for this resource"):
        VectorIndex.get_stats("test-graph-guid")

    # Test without graph_guid
    mock_client.tenant_guid = "test-tenant-guid"
    with pytest.raises(ValueError, match="Graph GUID is required for this resource"):
        VectorIndex.get_stats("")

    # Test with empty graph_guid
    with pytest.raises(ValueError, match="Graph GUID is required for this resource"):
        VectorIndex.get_stats(None)


def test_enable(mock_client, valid_vector_index_config):
    """Test enable method."""
    config = HnswLiteVectorIndexModel(**valid_vector_index_config)
    mock_client.request.return_value = valid_vector_index_config
    mock_client.request.side_effect = None

    result = VectorIndex.enable("test-graph-guid", config)
    assert isinstance(result, HnswLiteVectorIndexModel)
    assert result.guid == valid_vector_index_config["GUID"]
    assert result.vector_dimensionality == valid_vector_index_config["VectorDimensionality"]

    # Verify the request was made correctly
    mock_client.request.assert_called_once()
    called_args = mock_client.request.call_args
    assert called_args[0][0] == "PUT"
    assert "vectorindex/enable" in called_args[0][1]
    assert "json" in called_args[1]
    assert called_args[1]["json"]["VectorDimensionality"] == valid_vector_index_config["VectorDimensionality"]

    # Test without tenant_guid
    mock_client.tenant_guid = None
    with pytest.raises(ValueError, match="Tenant GUID is required for this resource"):
        VectorIndex.enable("test-graph-guid", config)

    # Test without graph_guid
    mock_client.tenant_guid = "test-tenant-guid"
    with pytest.raises(ValueError, match="Graph GUID is required for this resource"):
        VectorIndex.enable("", config)

    # Test with invalid config type
    with pytest.raises(TypeError, match="Config must be an instance of HnswLiteVectorIndexModel"):
        VectorIndex.enable("test-graph-guid", {"invalid": "config"})

    # Test with None config
    with pytest.raises(TypeError, match="Config must be an instance of HnswLiteVectorIndexModel"):
        VectorIndex.enable("test-graph-guid", None)


def test_rebuild(mock_client):
    """Test rebuild method."""
    mock_client.request.return_value = None
    mock_client.request.side_effect = None

    VectorIndex.rebuild("test-graph-guid")
    mock_client.request.assert_called_once()
    called_args = mock_client.request.call_args
    assert called_args[0][0] == "POST"
    assert "vectorindex/rebuild" in called_args[0][1]

    # Test without tenant_guid
    mock_client.request.reset_mock()
    mock_client.tenant_guid = None
    with pytest.raises(ValueError, match="Tenant GUID is required for this resource"):
        VectorIndex.rebuild("test-graph-guid")

    # Test without graph_guid
    mock_client.tenant_guid = "test-tenant-guid"
    with pytest.raises(ValueError, match="Graph GUID is required for this resource"):
        VectorIndex.rebuild("")

    # Test with empty graph_guid
    with pytest.raises(ValueError, match="Graph GUID is required for this resource"):
        VectorIndex.rebuild(None)


def test_delete(mock_client):
    """Test delete method."""
    mock_client.request.return_value = None
    mock_client.request.side_effect = None

    VectorIndex.delete("test-graph-guid")
    mock_client.request.assert_called_once()
    called_args = mock_client.request.call_args
    assert called_args[0][0] == "DELETE"
    assert "vectorindex" in called_args[0][1]

    # Test without tenant_guid
    mock_client.request.reset_mock()
    mock_client.tenant_guid = None
    with pytest.raises(ValueError, match="Tenant GUID is required for this resource"):
        VectorIndex.delete("test-graph-guid")

    # Test without graph_guid
    mock_client.tenant_guid = "test-tenant-guid"
    with pytest.raises(ValueError, match="Graph GUID is required for this resource"):
        VectorIndex.delete("")

    # Test with empty graph_guid
    with pytest.raises(ValueError, match="Graph GUID is required for this resource"):
        VectorIndex.delete(None)


def test_create_from_dict(mock_client, valid_vector_index_config):
    """Test create_from_dict method."""
    mock_client.request.return_value = valid_vector_index_config
    mock_client.request.side_effect = None

    result = VectorIndex.create_from_dict("test-graph-guid", valid_vector_index_config)
    assert isinstance(result, HnswLiteVectorIndexModel)
    assert result.guid == valid_vector_index_config["GUID"]
    assert result.vector_dimensionality == valid_vector_index_config["VectorDimensionality"]

    # Verify enable was called (which calls request)
    assert mock_client.request.call_count == 1
    called_args = mock_client.request.call_args
    assert called_args[0][0] == "PUT"
    assert "vectorindex/enable" in called_args[0][1]

    # Test without tenant_guid
    mock_client.tenant_guid = None
    with pytest.raises(ValueError, match="Tenant GUID is required for this resource"):
        VectorIndex.create_from_dict("test-graph-guid", valid_vector_index_config)

    # Test without graph_guid
    mock_client.tenant_guid = "test-tenant-guid"
    with pytest.raises(ValueError, match="Graph GUID is required for this resource"):
        VectorIndex.create_from_dict("", valid_vector_index_config)


def test_get_config_exception_handling(mock_client):
    """Test get_config exception handling."""
    # Test when client.request raises an exception
    mock_client.request.side_effect = Exception("API Error")
    with pytest.raises(Exception, match="API Error"):
        VectorIndex.get_config("test-graph-guid")

    # Test with different exception types
    mock_client.request.side_effect = ValueError("Invalid response")
    with pytest.raises(ValueError, match="Invalid response"):
        VectorIndex.get_config("test-graph-guid")


def test_get_stats_exception_handling(mock_client):
    """Test get_stats exception handling."""
    # Test when client.request raises an exception
    mock_client.request.side_effect = Exception("API Error")
    with pytest.raises(Exception, match="API Error"):
        VectorIndex.get_stats("test-graph-guid")

    # Test with different exception types
    mock_client.request.side_effect = ValueError("Invalid response")
    with pytest.raises(ValueError, match="Invalid response"):
        VectorIndex.get_stats("test-graph-guid")


def test_enable_exception_handling(mock_client, valid_vector_index_config):
    """Test enable exception handling."""
    config = HnswLiteVectorIndexModel(**valid_vector_index_config)

    # Test when client.request raises an exception
    mock_client.request.side_effect = Exception("API Error")
    with pytest.raises(Exception, match="API Error"):
        VectorIndex.enable("test-graph-guid", config)

    # Test with different exception types
    mock_client.request.side_effect = ValueError("Invalid response")
    with pytest.raises(ValueError, match="Invalid response"):
        VectorIndex.enable("test-graph-guid", config)


def test_rebuild_exception_handling(mock_client):
    """Test rebuild exception handling."""
    # Test when client.request raises an exception
    mock_client.request.side_effect = Exception("API Error")
    with pytest.raises(Exception, match="API Error"):
        VectorIndex.rebuild("test-graph-guid")

    # Test with different exception types
    mock_client.request.side_effect = ValueError("Invalid response")
    with pytest.raises(ValueError, match="Invalid response"):
        VectorIndex.rebuild("test-graph-guid")


def test_delete_exception_handling(mock_client):
    """Test delete exception handling."""
    # Test when client.request raises an exception
    mock_client.request.side_effect = Exception("API Error")
    with pytest.raises(Exception, match="API Error"):
        VectorIndex.delete("test-graph-guid")

    # Test with different exception types
    mock_client.request.side_effect = ValueError("Invalid response")
    with pytest.raises(ValueError, match="Invalid response"):
        VectorIndex.delete("test-graph-guid")


def test_create_from_dict_exception_handling(mock_client, valid_vector_index_config):
    """Test create_from_dict exception handling."""
    # Test when enable raises an exception
    mock_client.request.side_effect = Exception("API Error")
    with pytest.raises(Exception, match="API Error"):
        VectorIndex.create_from_dict("test-graph-guid", valid_vector_index_config)

    # Test with invalid config_dict
    with pytest.raises(Exception):  # Will raise ValidationError from Pydantic
        VectorIndex.create_from_dict("test-graph-guid", {"invalid": "config"})


def test_hnsw_lite_vector_index_model_validation(valid_vector_index_config):
    """Test HnswLiteVectorIndexModel validation."""
    model = HnswLiteVectorIndexModel(**valid_vector_index_config)
    assert isinstance(model.guid, str)
    assert model.graph_guid == valid_vector_index_config["GraphGUID"]
    assert model.vector_dimensionality == valid_vector_index_config["VectorDimensionality"]
    assert model.vector_index_type == valid_vector_index_config["VectorIndexType"]
    assert model.m == valid_vector_index_config["M"]
    assert model.ef_construction == valid_vector_index_config["EfConstruction"]
    assert model.default_ef == valid_vector_index_config["DefaultEf"]
    assert model.distance_metric == valid_vector_index_config["DistanceMetric"]


def test_vector_index_statistics_model_validation(valid_vector_index_stats):
    """Test VectorIndexStatisticsModel validation."""
    model = VectorIndexStatisticsModel(**valid_vector_index_stats)
    assert model.vector_count == valid_vector_index_stats["VectorCount"]
    assert model.dimensions == valid_vector_index_stats["Dimensions"]
    assert model.index_type == valid_vector_index_stats["IndexType"]
    assert model.m == valid_vector_index_stats["M"]
    assert model.ef_construction == valid_vector_index_stats["EfConstruction"]
    assert model.default_ef == valid_vector_index_stats["DefaultEf"]
    assert model.is_loaded == valid_vector_index_stats["IsLoaded"]
    assert model.distance_metric == valid_vector_index_stats["DistanceMetric"]
