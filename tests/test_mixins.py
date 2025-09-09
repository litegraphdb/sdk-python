import uuid
from typing import Optional
from unittest.mock import Mock, patch
from datetime import datetime, timezone

import pytest
from litegraph.base import BaseClient
from litegraph.mixins import (
    AllRetrievableAPIResource,
    CreateableAPIResource,
    CreateableMultipleAPIResource,
    DeletableAPIResource,
    DeleteAllAPIResource,
    DeleteMultipleAPIResource,
    ExistsAPIResource,
    RetrievableAPIResource,
    SearchableAPIResource,
    UpdatableAPIResource,
    ExportGexfMixin,
    EnumerableAPIResourceWithData,
    EnumerableAPIResource,
    RetrievableStatisticsMixin,
    RetrievableFirstMixin,
    RetrievableManyMixin,
)
from pydantic import BaseModel
from litegraph.exceptions import SdkException


# Test Models
class MockModel(BaseModel):
    id: str
    name: Optional[str] = None
    data: Optional[dict] = None


class MockRequestModel(BaseModel):
    query: str


class MockResponseModel(BaseModel):
    results: list[MockModel]


# Test Resource Classes
class TestBaseResource:
    RESOURCE_NAME = "test-resources"
    MODEL = MockModel
    SEARCH_MODELS = (MockRequestModel, MockResponseModel)
    REQUIRE_GRAPH_GUID = True


class ResourceModel(
    TestBaseResource,
    ExistsAPIResource,
    CreateableAPIResource,
    CreateableMultipleAPIResource,  # Added new mixin
    RetrievableAPIResource,
    UpdatableAPIResource,
    DeletableAPIResource,
    DeleteAllAPIResource,  # Added new mixin
    DeleteMultipleAPIResource,  # Added new mixin
    AllRetrievableAPIResource,
    SearchableAPIResource,
):
    pass


class TestResourceNoGraphGuid(ResourceModel):
    REQUIRE_GRAPH_GUID = False


class TestExportGexf(TestBaseResource, ExportGexfMixin):
    pass


@pytest.fixture
def mock_client(monkeypatch):
    """Create a mock client and configure it."""
    client = Mock(spec=BaseClient)
    client.tenant_guid = "test-tenant-guid"
    client.graph_guid = "test-graph-guid"
    client.base_url = "http://test-api.com"
    monkeypatch.setattr("litegraph.configuration._client", client)
    return client


def test_exists_resource(mock_client):
    """Test ExistsAPIResource mixin."""
    # Test resource exists
    mock_client.request.return_value = None
    assert ResourceModel.exists("test-id") is True

    # Test resource doesn't exist
    mock_client.request.side_effect = Exception("Not found")
    assert ResourceModel.exists("test-id") is False

    # Test with no graph_guid
    mock_client.graph_guid = None
    assert TestResourceNoGraphGuid.exists("test-id") is False


def test_create_resource(mock_client):
    """Test CreateableAPIResource mixin."""
    test_data = {"id": "test-id", "name": "Test Resource", "data": {"key": "value"}}
    mock_client.request.return_value = test_data
    mock_client.request.side_effect = None  # Reset any previous side effects

    # Test successful creation
    result = ResourceModel.create(**test_data)
    assert isinstance(result, MockModel)
    assert result.id == test_data["id"]
    assert result.name == test_data["name"]
    assert result.data == test_data["data"]

    # Test creation without graph_guid
    mock_client.graph_guid = None
    result = TestResourceNoGraphGuid.create(**test_data)
    assert isinstance(result, MockModel)

    # Test minimal data
    minimal_data = {"id": "test-id"}
    mock_client.graph_guid = "test-graph-guid"
    mock_client.request.return_value = minimal_data
    result = ResourceModel.create(**minimal_data)
    assert isinstance(result, MockModel)
    assert result.name is None
    assert result.data is None


def test_retrieve_resource(mock_client):
    """Test RetrievableAPIResource mixin."""
    test_data = {"id": "test-id", "name": "Test Resource", "data": {"key": "value"}}
    mock_client.request.return_value = test_data
    mock_client.request.side_effect = None

    # Test successful retrieval
    result = ResourceModel.retrieve("test-id")
    assert isinstance(result, MockModel)
    assert result.id == test_data["id"]
    assert result.name == test_data["name"]
    assert result.data == test_data["data"]

    # Test retrieval without graph_guid when required
    mock_client.graph_guid = None
    with pytest.raises(ValueError, match="Graph GUID is required for this resource"):
        ResourceModel.retrieve("test-id")

    # Test retrieval without graph_guid when not required
    mock_client.request.return_value = test_data
    result = TestResourceNoGraphGuid.retrieve("test-id")
    assert isinstance(result, MockModel)


def test_update_resource(mock_client):
    """Test UpdatableAPIResource mixin."""
    test_data = {
        "id": "test-id",
        "name": "Updated Resource",
        "data": {"key": "new-value"},
    }
    mock_client.request.return_value = test_data
    mock_client.request.side_effect = None

    # Test successful update
    result = ResourceModel.update("test-id", **test_data)
    assert isinstance(result, MockModel)
    assert result.id == test_data["id"]
    assert result.name == test_data["name"]
    assert result.data == test_data["data"]

    # Test update without graph_guid when required
    mock_client.graph_guid = None
    with pytest.raises(ValueError, match="Graph GUID is required for this resource"):
        ResourceModel.update("test-id", **test_data)

    # Test update without graph_guid when not required
    mock_client.request.return_value = test_data
    result = TestResourceNoGraphGuid.update("test-id", **test_data)
    assert isinstance(result, MockModel)


def test_delete_resource(mock_client):
    """Test DeletableAPIResource mixin."""
    mock_client.request.side_effect = None

    # Test successful deletion
    ResourceModel.delete("test-id")
    mock_client.request.assert_called_once()
    assert mock_client.request.call_args[0][0] == "DELETE"

    # Test deletion without graph_guid when required
    mock_client.request.reset_mock()
    mock_client.graph_guid = None
    with pytest.raises(ValueError, match="Graph GUID is required for this resource"):
        ResourceModel.delete("test-id")

    # Test deletion without graph_guid when not required
    mock_client.request.reset_mock()
    TestResourceNoGraphGuid.delete("test-id")
    mock_client.request.assert_called_once()


def test_retrieve_all_resources(mock_client):
    """Test AllRetrievableAPIResource mixin."""
    test_data = [
        {"id": "test-id-1", "name": "Resource 1", "data": {"key": "value1"}},
        {"id": "test-id-2", "name": "Resource 2", "data": {"key": "value2"}},
    ]
    mock_client.request.return_value = test_data
    mock_client.request.side_effect = None

    # Test successful retrieval of all resources
    results = ResourceModel.retrieve_all()
    assert isinstance(results, list)
    assert all(isinstance(item, MockModel) for item in results)
    assert len(results) == 2

    # Test retrieve all without graph_guid when required
    mock_client.graph_guid = None
    with pytest.raises(ValueError, match="Graph GUID is required for this resource."):
        ResourceModel.retrieve_all()

    # Test retrieve all without graph_guid when not required
    mock_client.request.return_value = test_data
    results = TestResourceNoGraphGuid.retrieve_all()
    assert isinstance(results, list)
    assert len(results) == 2


def test_search_resources(mock_client):
    """Test SearchableAPIResource mixin."""
    search_response = {
        "results": [
            {"id": "test-id-1", "name": "Resource 1", "data": {"key": "value1"}},
            {"id": "test-id-2", "name": "Resource 2", "data": {"key": "value2"}},
        ]
    }
    mock_client.request.return_value = search_response
    mock_client.request.side_effect = None

    # Test basic search
    search_params = {"query": "test"}
    result = ResourceModel.search(graph_id="test-graph", **search_params)
    assert isinstance(result, MockResponseModel)
    assert len(result.results) == 2

    # Test search with empty results
    mock_client.request.return_value = {"results": []}
    result = ResourceModel.search(graph_id="test-graph", query="nonexistent")
    assert isinstance(result, MockResponseModel)
    assert len(result.results) == 0


def test_model_validation(mock_client):
    """Test model validation in mixins."""
    mock_client.request.side_effect = None

    # Test invalid create data
    invalid_data = {"invalid_field": "value"}
    mock_client.request.return_value = invalid_data
    with pytest.raises(ValueError):
        ResourceModel.create(**invalid_data)

    # Test invalid search response
    mock_client.request.return_value = {"invalid_field": "value"}
    with pytest.raises(ValueError):
        ResourceModel.search(graph_id="test-graph", query="test")


def test_error_handling(mock_client):
    """Test error handling in mixins."""
    api_error = Exception("API Error")
    mock_client.request.side_effect = api_error

    with pytest.raises(Exception):
        ResourceModel.create(id="test-id")

    with pytest.raises(Exception):
        ResourceModel.retrieve("test-id")

    with pytest.raises(Exception):
        ResourceModel.update("test-id", id="test-id")

    with pytest.raises(Exception):
        ResourceModel.delete("test-id")

    with pytest.raises(Exception):
        ResourceModel.retrieve_all()

    with pytest.raises(Exception):
        ResourceModel.search(graph_id="test-graph", query="test")


def test_create_multiple_resources(mock_client):
    """Test CreateableMultipleAPIResource mixin."""
    test_data = [
        {"id": "test-id-1", "name": "Test Resource 1", "data": {"key": "value1"}},
        {"id": "test-id-2", "name": "Test Resource 2", "data": {"key": "value2"}},
    ]
    mock_client.request.return_value = test_data
    mock_client.request.side_effect = None

    # Test successful multiple creation
    result = ResourceModel.create_multiple(test_data)
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(item, MockModel) for item in result)
    assert result[0].id == test_data[0]["id"]
    assert result[1].id == test_data[1]["id"]

    # Test with empty list
    assert ResourceModel.create_multiple([]) == []

    # Test with None
    with pytest.raises(TypeError, match="Nodes parameter cannot be None"):
        ResourceModel.create_multiple(None)

    # Verify request parameters
    mock_client.request.assert_called()
    called_args = mock_client.request.call_args
    assert called_args[0][0] == "PUT"
    assert "bulk" in called_args[0][1]


def test_delete_all_resources(mock_client):
    """Test DeleteAllAPIResource mixin."""
    mock_client.request.side_effect = None

    # Test successful deletion of all resources with a valid UUID
    valid_uuid = "550e8400-e29b-41d4-a716-446655440000"
    mock_client.graph_guid = valid_uuid  # Valid UUID string
    ResourceModel.delete_all()
    mock_client.request.assert_called_once()
    called_args = mock_client.request.call_args
    assert called_args[0][0] == "DELETE"
    assert "all" in called_args[0][1]
    assert called_args[1]["headers"] == {"Content-Type": "application/json"}

    # Test without graph_guid when required (expect ValueError)
    mock_client.request.reset_mock()
    mock_client.graph_guid = None
    with pytest.raises(ValueError) as exc_info:
        ResourceModel.delete_all()

    # Match the expected error message
    assert "badly formed hexadecimal UUID string" in str(exc_info.value)

    # Test with invalid UUID format (expect ValueError due to invalid UUID string)
    mock_client.request.reset_mock()
    invalid_uuid = "invalid-uuid"
    mock_client.graph_guid = invalid_uuid
    with pytest.raises(ValueError) as exc_info:
        ResourceModel.delete_all()

    # Match the expected error message
    assert "badly formed hexadecimal UUID string" in str(exc_info.value)

    mock_client.request.reset_mock()
    mock_client.graph_guid = None
    with patch("uuid.UUID", side_effect=lambda x: x if x is not None else valid_uuid):
        TestResourceNoGraphGuid.delete_all()
    mock_client.request.assert_called_once()
    called_args = mock_client.request.call_args
    assert called_args[0][0] == "DELETE"
    assert "all" in called_args[0][1]
    assert called_args[1]["headers"] == {"Content-Type": "application/json"}


def test_delete_multiple_resources(mock_client):
    """Test DeleteMultipleAPIResource mixin."""
    mock_client.request.side_effect = None

    # Test successful multiple deletion
    resource_ids = ["test-id-1", "test-id-2"]
    ResourceModel.delete_multiple(resource_ids)
    mock_client.request.assert_called_once()
    called_args = mock_client.request.call_args
    assert called_args[0][0] == "DELETE"
    assert "bulk" in called_args[0][1]
    assert called_args[1]["headers"] == {"Content-Type": "application/json"}
    assert called_args[1]["json"] == resource_ids

    # Test with empty list
    mock_client.request.reset_mock()
    ResourceModel.delete_multiple([])
    mock_client.request.assert_not_called()

    # Test with None
    with pytest.raises(TypeError, match="Input must be a list of IDs"):
        ResourceModel.delete_multiple(None)

    # Test with invalid input type
    with pytest.raises(TypeError, match="Input must be a list of IDs"):
        ResourceModel.delete_multiple("not-a-list")

    # Test without graph_guid when required
    mock_client.request.reset_mock()
    mock_client.graph_guid = None
    with pytest.raises(ValueError, match="Graph GUID is required for this resource."):
        ResourceModel.delete_multiple(resource_ids)


def test_model_validation_for_create_multiple(mock_client):
    """Test model validation in create_multiple."""
    mock_client.request.side_effect = None

    # Test with valid data
    valid_data = [{"id": "test-id", "name": "Test Resource"}]
    mock_client.request.return_value = valid_data
    result = ResourceModel.create_multiple(valid_data)
    assert isinstance(result, list)
    assert all(isinstance(item, MockModel) for item in result)

    # Test with invalid data
    invalid_data = [{"invalid_field": "value"}]
    mock_client.request.return_value = invalid_data
    with pytest.raises(ValueError):
        ResourceModel.create_multiple(invalid_data)

    # Test with mixed valid/invalid data
    mixed_data = [
        {"id": "test-id-1"},  # valid
        {"invalid_field": "value"},  # invalid
    ]
    mock_client.request.return_value = mixed_data
    with pytest.raises(ValueError):
        ResourceModel.create_multiple(mixed_data)


def test_export_gexf_success(mock_client):
    """Test successful GEXF export."""
    # Mock successful GEXF export response
    mock_gexf_content = b'<?xml version="1.0" encoding="UTF-8"?><gexf>...</gexf>'
    mock_client.request.return_value = mock_gexf_content
    mock_client.request.side_effect = None

    # Test basic export
    result = TestExportGexf.export_gexf("test-graph-id")
    assert isinstance(result, str)
    assert "<?xml" in result
    assert "<gexf>" in result

    # Verify the request was made correctly
    mock_client.request.assert_called_once()
    called_args = mock_client.request.call_args
    assert called_args[0][0] == "GET"
    assert "export" in called_args[0][1]
    assert "gexf" in called_args[0][1]


def test_export_gexf_with_params(mock_client):
    """Test GEXF export with additional parameters."""
    mock_gexf_content = b'<?xml version="1.0" encoding="UTF-8"?><gexf>...</gexf>'
    mock_client.request.return_value = mock_gexf_content

    # Test export with additional parameters
    params = {"format": "pretty", "version": "1.2"}
    result = TestExportGexf.export_gexf("test-graph-id", **params)
    assert isinstance(result, str)

    # Verify parameters were included in the URL
    called_args = mock_client.request.call_args
    assert "format=pretty" in called_args[0][1]
    assert "version=1.2" in called_args[0][1]


def test_export_gexf_error_handling(mock_client):
    """Test error handling during GEXF export."""
    # Test with invalid UTF-8 response
    mock_client.request.return_value = b'\x80invalid'

    with pytest.raises(SdkException, match="Error exporting GEXF"):
        TestExportGexf.export_gexf("test-graph-id")

    # Test with missing tenant GUID
    mock_client.tenant_guid = None
    with pytest.raises(ValueError, match="Tenant GUID is required for this resource"):
        TestExportGexf.export_gexf("test-graph-id")


def test_exists_resource_exception_handling(mock_client):
    """Test ExistsAPIResource exception handling for better coverage."""
    # Test when client.request raises an exception
    mock_client.request.side_effect = Exception("Network error")
    assert ResourceModel.exists("test-id") is False

    # Test when client.request raises different types of exceptions
    mock_client.request.side_effect = ValueError("Invalid URL")
    assert ResourceModel.exists("test-id") is False

    mock_client.request.side_effect = RuntimeError("Connection failed")
    assert ResourceModel.exists("test-id") is False


def test_create_resource_exception_handling(mock_client):
    """Test CreateableAPIResource exception handling."""
    test_data = {"id": "test-id", "name": "Test Resource"}
    
    # Test when client.request raises an exception
    mock_client.request.side_effect = Exception("API Error")
    with pytest.raises(Exception, match="API Error"):
        ResourceModel.create(**test_data)

    # Test with different exception types
    mock_client.request.side_effect = ValueError("Validation Error")
    with pytest.raises(ValueError, match="Validation Error"):
        ResourceModel.create(**test_data)


def test_create_multiple_exception_handling(mock_client):
    """Test CreateableMultipleAPIResource exception handling."""
    test_data = [{"id": "test-id-1"}, {"id": "test-id-2"}]
    
    # Test when client.request raises an exception
    mock_client.request.side_effect = Exception("Bulk creation failed")
    with pytest.raises(Exception, match="Bulk creation failed"):
        ResourceModel.create_multiple(test_data)

    # Test with different exception types
    mock_client.request.side_effect = RuntimeError("Server error")
    with pytest.raises(RuntimeError, match="Server error"):
        ResourceModel.create_multiple(test_data)


def test_retrieve_resource_exception_handling(mock_client):
    """Test RetrievableAPIResource exception handling."""
    # Test when client.request raises an exception
    mock_client.request.side_effect = Exception("Retrieval failed")
    with pytest.raises(Exception, match="Retrieval failed"):
        ResourceModel.retrieve("test-id")

    # Test with different exception types
    mock_client.request.side_effect = ValueError("Invalid ID")
    with pytest.raises(ValueError, match="Invalid ID"):
        ResourceModel.retrieve("test-id")


def test_update_resource_exception_handling(mock_client):
    """Test UpdatableAPIResource exception handling."""
    test_data = {"id": "test-id", "name": "Updated Resource"}
    
    # Test when client.request raises an exception
    mock_client.request.side_effect = Exception("Update failed")
    with pytest.raises(Exception, match="Update failed"):
        ResourceModel.update("test-id", **test_data)

    # Test with different exception types
    mock_client.request.side_effect = RuntimeError("Server error")
    with pytest.raises(RuntimeError, match="Server error"):
        ResourceModel.update("test-id", **test_data)


def test_delete_resource_exception_handling(mock_client):
    """Test DeletableAPIResource exception handling."""
    # Test when client.request raises an exception
    mock_client.request.side_effect = Exception("Delete failed")
    with pytest.raises(Exception, match="Delete failed"):
        ResourceModel.delete("test-id")

    # Test with different exception types
    mock_client.request.side_effect = ValueError("Invalid resource")
    with pytest.raises(ValueError, match="Invalid resource"):
        ResourceModel.delete("test-id")


def test_delete_multiple_exception_handling(mock_client):
    """Test DeleteMultipleAPIResource exception handling."""
    resource_ids = ["test-id-1", "test-id-2"]
    
    # Test when client.request raises an exception
    mock_client.request.side_effect = Exception("Bulk delete failed")
    with pytest.raises(Exception, match="Bulk delete failed"):
        ResourceModel.delete_multiple(resource_ids)

    # Test with different exception types
    mock_client.request.side_effect = RuntimeError("Server error")
    with pytest.raises(RuntimeError, match="Server error"):
        ResourceModel.delete_multiple(resource_ids)


def test_delete_all_exception_handling(mock_client):
    """Test DeleteAllAPIResource exception handling."""
    valid_uuid = "550e8400-e29b-41d4-a716-446655440000"
    mock_client.graph_guid = valid_uuid
    
    # Test when client.request raises an exception
    mock_client.request.side_effect = Exception("Delete all failed")
    with pytest.raises(Exception, match="Delete all failed"):
        ResourceModel.delete_all()

    # Test with different exception types
    mock_client.request.side_effect = ValueError("Invalid operation")
    with pytest.raises(ValueError, match="Invalid operation"):
        ResourceModel.delete_all()


def test_retrieve_all_exception_handling(mock_client):
    """Test AllRetrievableAPIResource exception handling."""
    # Test when client.request raises an exception
    mock_client.request.side_effect = Exception("Retrieve all failed")
    with pytest.raises(Exception, match="Retrieve all failed"):
        ResourceModel.retrieve_all()

    # Test with different exception types
    mock_client.request.side_effect = RuntimeError("Server error")
    with pytest.raises(RuntimeError, match="Server error"):
        ResourceModel.retrieve_all()


def test_search_exception_handling(mock_client):
    """Test SearchableAPIResource exception handling."""
    search_params = {"query": "test"}
    
    # Test when client.request raises an exception
    mock_client.request.side_effect = Exception("Search failed")
    with pytest.raises(Exception, match="Search failed"):
        ResourceModel.search(graph_id="test-graph", **search_params)

    # Test with different exception types
    mock_client.request.side_effect = ValueError("Invalid search parameters")
    with pytest.raises(ValueError, match="Invalid search parameters"):
        ResourceModel.search(graph_id="test-graph", **search_params)


def test_export_gexf_exception_handling_detailed(mock_client):
    """Test ExportGexfMixin detailed exception handling."""
    # Test when client.request raises an exception
    mock_client.request.side_effect = Exception("Export failed")
    with pytest.raises(Exception, match="Export failed"):
        TestExportGexf.export_gexf("test-graph-id")

    # Test with different exception types
    mock_client.request.side_effect = ValueError("Invalid graph ID")
    with pytest.raises(ValueError, match="Invalid graph ID"):
        TestExportGexf.export_gexf("test-graph-id")

    # Test with RuntimeError
    mock_client.request.side_effect = RuntimeError("Server error")
    with pytest.raises(RuntimeError, match="Server error"):
        TestExportGexf.export_gexf("test-graph-id")


def test_create_resource_with_headers(mock_client):
    """Test CreateableAPIResource with custom headers."""
    test_data = {"id": "test-id", "name": "Test Resource"}
    mock_client.request.return_value = test_data
    mock_client.request.side_effect = None

    # Test creation with custom headers
    custom_headers = {"X-Custom-Header": "custom-value"}
    result = ResourceModel.create(**test_data, headers=custom_headers)
    assert isinstance(result, MockModel)

    # Verify headers were passed correctly
    mock_client.request.assert_called_once()
    called_args = mock_client.request.call_args
    assert "headers" in called_args[1]
    assert called_args[1]["headers"]["X-Custom-Header"] == "custom-value"


def test_create_resource_with_data_parameter(mock_client):
    """Test CreateableAPIResource with _data parameter."""
    test_data = {"id": "test-id", "name": "Test Resource"}
    mock_client.request.return_value = test_data
    mock_client.request.side_effect = None

    # Test creation with _data parameter
    result = ResourceModel.create(_data=test_data)
    assert isinstance(result, MockModel)
    assert result.id == test_data["id"]


def test_create_multiple_with_none_data(mock_client):
    """Test CreateableMultipleAPIResource with None data."""
    # Test with None data
    with pytest.raises(TypeError, match="Nodes parameter cannot be None"):
        ResourceModel.create_multiple(None)


def test_create_multiple_with_empty_list(mock_client):
    """Test CreateableMultipleAPIResource with empty list."""
    # Test with empty list - should return empty list without making request
    result = ResourceModel.create_multiple([])
    assert result == []
    mock_client.request.assert_not_called()


def test_retrieve_with_include_parameters(mock_client):
    """Test RetrievableAPIResource with include parameters."""
    test_data = {"id": "test-id", "name": "Test Resource"}
    mock_client.request.return_value = test_data
    mock_client.request.side_effect = None

    # Test retrieval with include_data
    result = ResourceModel.retrieve("test-id", include_data=True)
    assert isinstance(result, MockModel)

    # Test retrieval with include_subordinates
    result = ResourceModel.retrieve("test-id", include_subordinates=True)
    assert isinstance(result, MockModel)

    # Test retrieval with both include parameters
    result = ResourceModel.retrieve("test-id", include_data=True, include_subordinates=True)
    assert isinstance(result, MockModel)


def test_retrieve_all_with_include_parameters(mock_client):
    """Test AllRetrievableAPIResource with include parameters."""
    test_data = [{"id": "test-id-1"}, {"id": "test-id-2"}]
    mock_client.request.return_value = test_data
    mock_client.request.side_effect = None

    # Test retrieve all with include_data
    result = ResourceModel.retrieve_all(include_data=True)
    assert isinstance(result, list)
    assert len(result) == 2

    # Test retrieve all with include_subordinates
    result = ResourceModel.retrieve_all(include_subordinates=True)
    assert isinstance(result, list)
    assert len(result) == 2

    # Test retrieve all with both include parameters
    result = ResourceModel.retrieve_all(include_data=True, include_subordinates=True)
    assert isinstance(result, list)
    assert len(result) == 2


def test_search_with_include_parameters(mock_client):
    """Test SearchableAPIResource with include parameters."""
    search_response = {"results": [{"id": "test-id-1", "name": "Resource 1"}]}
    mock_client.request.return_value = search_response
    mock_client.request.side_effect = None

    # Test search with include_data
    result = ResourceModel.search(graph_id="test-graph", query="test", include_data=True)
    assert isinstance(result, MockResponseModel)

    # Test search with include_subordinates
    result = ResourceModel.search(graph_id="test-graph", query="test", include_subordinates=True)
    assert isinstance(result, MockResponseModel)

    # Test search with both include parameters
    result = ResourceModel.search(graph_id="test-graph", query="test", include_data=True, include_subordinates=True)
    assert isinstance(result, MockResponseModel)


def test_model_validation_edge_cases(mock_client):
    """Test model validation edge cases in mixins."""
    mock_client.request.side_effect = None

    # Test create with None MODEL
    class ResourceWithoutModel(TestBaseResource, CreateableAPIResource):
        MODEL = None

    test_data = {"id": "test-id"}
    mock_client.request.return_value = test_data
    result = ResourceWithoutModel.create(**test_data)
    assert result == test_data  # Should return raw data when MODEL is None

    # Test retrieve_all with None MODEL
    class ResourceWithoutModelAll(TestBaseResource, AllRetrievableAPIResource):
        MODEL = None

    test_data_list = [{"id": "test-id-1"}, {"id": "test-id-2"}]
    mock_client.request.return_value = test_data_list
    result = ResourceWithoutModelAll.retrieve_all()
    assert result == test_data_list  # Should return raw data when MODEL is None

    # Test search with None SEARCH_MODELS
    class ResourceWithoutSearchModels(TestBaseResource, SearchableAPIResource):
        SEARCH_MODELS = None

    search_response = {"results": [{"id": "test-id-1"}]}
    mock_client.request.return_value = search_response
    with pytest.raises(TypeError):  # Should fail when SEARCH_MODELS is None
        ResourceWithoutSearchModels.search(graph_id="test-graph", query="test")


def test_url_construction_edge_cases(mock_client):
    """Test URL construction edge cases in mixins."""
    # Test with special characters in parameters
    test_data = {"id": "test-id", "name": "Test Resource"}
    mock_client.request.return_value = test_data
    mock_client.request.side_effect = None

    # Test with special characters in graph_guid
    mock_client.graph_guid = "test-graph-guid-with-special-chars-123"
    result = ResourceModel.create(**test_data)
    assert isinstance(result, MockModel)

    # Test with empty string graph_guid
    mock_client.graph_guid = ""
    with pytest.raises(ValueError, match="Graph GUID is required for this resource"):
        ResourceModel.create(**test_data)

    # Test with None graph_guid when required
    mock_client.graph_guid = None
    with pytest.raises(ValueError, match="Graph GUID is required for this resource"):
        ResourceModel.create(**test_data)


def test_tenant_required_error_coverage(mock_client):
    """Test tenant required error coverage for all mixins."""
    # Set tenant_guid to None to trigger TENANT_REQUIRED_ERROR
    mock_client.tenant_guid = None

    # Test ExistsAPIResource
    with pytest.raises(ValueError, match="Tenant GUID is required for this resource"):
        ResourceModel.exists("test-id")

    # Test CreateableAPIResource
    test_data = {"id": "test-id", "name": "Test Resource"}
    with pytest.raises(ValueError, match="Tenant GUID is required for this resource"):
        ResourceModel.create(**test_data)

    # Test CreateableMultipleAPIResource
    test_data_list = [{"id": "test-id-1"}, {"id": "test-id-2"}]
    with pytest.raises(ValueError, match="Tenant GUID is required for this resource"):
        ResourceModel.create_multiple(test_data_list)

    # Test RetrievableAPIResource
    with pytest.raises(ValueError, match="Tenant GUID is required for this resource"):
        ResourceModel.retrieve("test-id")

    # Test UpdatableAPIResource
    with pytest.raises(ValueError, match="Tenant GUID is required for this resource"):
        ResourceModel.update("test-id", **test_data)

    # Test DeletableAPIResource
    with pytest.raises(ValueError, match="Tenant GUID is required for this resource"):
        ResourceModel.delete("test-id")

    # Test DeleteMultipleAPIResource
    resource_ids = ["test-id-1", "test-id-2"]
    with pytest.raises(ValueError, match="Tenant GUID is required for this resource"):
        ResourceModel.delete_multiple(resource_ids)

    # Test AllRetrievableAPIResource
    with pytest.raises(ValueError, match="Tenant GUID is required for this resource"):
        ResourceModel.retrieve_all()

    # Test SearchableAPIResource
    with pytest.raises(ValueError, match="Tenant GUID is required for this resource"):
        ResourceModel.search(graph_id="test-graph", query="test")

    # Test ExportGexfMixin
    with pytest.raises(ValueError, match="Tenant GUID is required for this resource"):
        TestExportGexf.export_gexf("test-graph-id")


# def test_graph_guid_required_error_coverage(mock_client):
#     """Test graph GUID required error coverage for mixins that require it."""
#     # Set graph_guid to None to trigger GRAPH_REQUIRED_ERROR
#     mock_client.graph_guid = None
    
#     # Test CreateableAPIResource
#     test_data = {"id": "test-id", "name": "Test Resource"}
#     with pytest.raises(ValueError, match="Graph GUID is required for this resource"):
#         ResourceModel.create(**test_data)
    
#     # Test CreateableMultipleAPIResource - this doesn't validate graph_guid the same way
#     # It only uses it for URL construction, so we need to mock the response
#     test_data_list = [{"id": "test-id-1"}, {"id": "test-id-2"}]
#     mock_client.request.return_value = [{"id": "test-id-1"}, {"id": "test-id-2"}]
    
#     result = ResourceModel.create_multiple(test_data_list)
#     assert isinstance(result, list)
#     assert len(result) == 2
#     assert all(isinstance(item, MockModel) for item in result)
    
#     # Test RetrievableAPIResource
#     with pytest.raises(ValueError, match="Graph GUID is required for this resource"):
#         ResourceModel.retrieve("test-id")
    
#     # Test UpdatableAPIResource
#     with pytest.raises(ValueError, match="Graph GUID is required for this resource"):
#         ResourceModel.update("test-id", **test_data)
    
#     # Test DeletableAPIResource
#     with pytest.raises(ValueError, match="Graph GUID is required for this resource"):
#         ResourceModel.delete("test-id")
    
#     # Test DeleteMultipleAPIResource
#     with pytest.raises(ValueError, match="Graph GUID is required for this resource"):
#         ResourceModel.delete_multiple(["test-id-1", "test-id-2"])
    
#     # Test DeleteAllAPIResource
#     with pytest.raises(ValueError, match="badly formed hexadecimal UUID string"):
#         ResourceModel.delete_all()
    
#     # Test AllRetrievableAPIResource
#     with pytest.raises(ValueError, match="Graph GUID is required for this resource"):
#         ResourceModel.retrieve_all()
    
#     # Test SearchableAPIResource
#     with pytest.raises(ValueError, match="Graph GUID is required for this resource"):
#         ResourceModel.search("test-graph-id")
    
#     # Test RetrievableFirstMixin
#     with pytest.raises(ValueError, match="Graph GUID is required for this resource"):
#         ResourceModel.retrieve_first("test-graph-id")
    
#     # Test RetrievableManyMixin
#     with pytest.raises(ValueError, match="Graph GUID is required for this resource"):
#         ResourceModel.retrieve_many(["test-id-1", "test-id-2"], "test-graph-id")


def test_tenant_not_required_mixins(mock_client):
    """Test mixins that don't require tenant GUID."""
    # Create a resource class that doesn't require tenant
    class ResourceNoTenant(TestBaseResource, CreateableAPIResource, RetrievableAPIResource):
        REQUIRE_TENANT = False
        REQUIRE_GRAPH_GUID = False

    # Set tenant_guid to None
    mock_client.tenant_guid = None
    mock_client.graph_guid = None

    # These should not raise TENANT_REQUIRED_ERROR
    test_data = {"id": "test-id", "name": "Test Resource"}
    mock_client.request.return_value = test_data
    mock_client.request.side_effect = None

    # Test create without tenant requirement
    result = ResourceNoTenant.create(**test_data)
    assert isinstance(result, MockModel)

    # Test retrieve without tenant requirement
    result = ResourceNoTenant.retrieve("test-id")
    assert isinstance(result, MockModel)


def test_graph_guid_not_required_mixins(mock_client):
    """Test mixins that don't require graph GUID."""
    # Create a resource class that doesn't require graph GUID
    class ResourceNoGraph(TestBaseResource, CreateableAPIResource, RetrievableAPIResource):
        REQUIRE_GRAPH_GUID = False

    # Set graph_guid to None
    mock_client.graph_guid = None

    # These should not raise GRAPH_REQUIRED_ERROR
    test_data = {"id": "test-id", "name": "Test Resource"}
    mock_client.request.return_value = test_data
    mock_client.request.side_effect = None

    # Test create without graph GUID requirement
    result = ResourceNoGraph.create(**test_data)
    assert isinstance(result, MockModel)

    # Test retrieve without graph GUID requirement
    result = ResourceNoGraph.retrieve("test-id")
    assert isinstance(result, MockModel)


def test_empty_graph_guid_validation(mock_client):
    """Test validation with empty string graph GUID."""
    # Set graph_guid to empty string
    mock_client.graph_guid = ""

    test_data = {"id": "test-id", "name": "Test Resource"}

    # Test CreateableAPIResource with empty graph_guid
    with pytest.raises(ValueError, match="Graph GUID is required for this resource"):
        ResourceModel.create(**test_data)

    # Test RetrievableAPIResource with empty graph_guid
    with pytest.raises(ValueError, match="Graph GUID is required for this resource"):
        ResourceModel.retrieve("test-id")

    # Test UpdatableAPIResource with empty graph_guid
    with pytest.raises(ValueError, match="Graph GUID is required for this resource"):
        ResourceModel.update("test-id", **test_data)

    # Test DeletableAPIResource with empty graph_guid
    with pytest.raises(ValueError, match="Graph GUID is required for this resource"):
        ResourceModel.delete("test-id")


def test_tenant_guid_validation_edge_cases(mock_client):
    """Test tenant GUID validation edge cases."""
    # Test with None tenant_guid (should raise ValueError)
    mock_client.tenant_guid = None
    
    test_data = {"id": "test-id", "name": "Test Resource"}
    
    # Test CreateableAPIResource with None tenant_guid
    with pytest.raises(ValueError, match="Tenant GUID is required for this resource"):
        ResourceModel.create(**test_data)
    
    # Test with valid tenant_guid
    mock_client.tenant_guid = "valid-tenant-guid"
    mock_client.request.return_value = {"id": "test-id", "name": "Test Resource"}
    
    result = ResourceModel.create(**test_data)
    assert isinstance(result, MockModel)


def test_enumerable_api_resource_with_data_coverage(mock_client):
    """Test EnumerableAPIResourceWithData coverage for missing blocks."""
    # Test with REQUIRE_TENANT = False
    class ResourceWithoutTenant(TestBaseResource, EnumerableAPIResourceWithData):
        REQUIRE_TENANT = False
        MODEL = MockModel
        ENUMERABLE_REQUEST_MODEL = MockModel  # Use MockModel instead of EnumerationQueryModel
    
    mock_client.request.return_value = {"items": [], "total": 0}
    
    # Pass required field 'id' for MockModel
    result = ResourceWithoutTenant.enumerate_with_query(id="test-id")
    assert result
    
    # Test with MODEL = None
    class ResourceWithoutModel(TestBaseResource, EnumerableAPIResourceWithData):
        REQUIRE_TENANT = False
        MODEL = None
        ENUMERABLE_REQUEST_MODEL = MockModel
    
    result = ResourceWithoutModel.enumerate_with_query(id="test-id")
    assert result
    
    # Test with include_data and include_subordinates (provide them as True)
    result = ResourceWithoutTenant.enumerate_with_query(
        id="test-id",
        include_data=True, 
        include_subordinates=True
    )
    assert result


def test_retrievable_statistics_mixin_coverage(mock_client):
    """Test RetrievableStatisticsMixin coverage for missing blocks."""
    # Test with REQUIRE_TENANT = False
    class ResourceWithoutTenant(TestBaseResource, RetrievableStatisticsMixin):
        REQUIRE_TENANT = False
    
    mock_client.request.return_value = {"stats": "data"}
    
    result = ResourceWithoutTenant.retrieve_statistics("test-guid")
    assert result == {"stats": "data"}
    
    # Test without resource_guid
    result = ResourceWithoutTenant.retrieve_statistics()
    assert result == {"stats": "data"}
    
    # Test with REQUIRE_TENANT = True but valid tenant
    class ResourceWithTenant(TestBaseResource, RetrievableStatisticsMixin):
        REQUIRE_TENANT = True
    
    mock_client.tenant_guid = "valid-tenant"
    result = ResourceWithTenant.retrieve_statistics("test-guid")
    assert result == {"stats": "data"}


def test_export_gexf_mixin_coverage(mock_client):
    """Test ExportGexfMixin coverage for missing blocks."""
    # Test with REQUIRE_TENANT = False
    class ResourceWithoutTenant(TestBaseResource, ExportGexfMixin):
        REQUIRE_TENANT = False
    
    mock_client.request.return_value = b"gexf content"
    
    result = ResourceWithoutTenant.export_gexf("test-graph-id")
    assert result == "gexf content"
    
    # Test with REQUIRE_TENANT = True but valid tenant
    class ResourceWithTenant(TestBaseResource, ExportGexfMixin):
        REQUIRE_TENANT = True
    
    mock_client.tenant_guid = "valid-tenant"
    result = ResourceWithTenant.export_gexf("test-graph-id")
    assert result == "gexf content"


def test_enumerable_api_resource_coverage(mock_client):
    class ResourceWithoutTenant(TestBaseResource, EnumerableAPIResource):
        REQUIRE_TENANT = False
        MODEL = MockModel
    
    mock_client.request.return_value = {
        "Objects": [
            {
                "id": "mock-id-1",
                "name": "Mock Name",
                "data": None,
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
    
    result = ResourceWithoutTenant.enumerate()
    result_dict = result.model_dump()
    assert len(result_dict["objects"]) == 1
    assert result_dict["total_records"] == 1
    assert result_dict["success"] is True
    
    class ResourceWithoutModel(TestBaseResource, EnumerableAPIResource):
        REQUIRE_TENANT = False
        MODEL = None
    
    mock_client.request.return_value = {"items": [], "total": 0}
    
    result = ResourceWithoutModel.enumerate()
    assert result == {"items": [], "total": 0}
    
    result = ResourceWithoutTenant.enumerate(
        include_data=True,
        include_subordinates=True,
    )
    result_dict = result.model_dump()
    assert isinstance(result_dict["objects"], list)


def test_retrievable_first_mixin_coverage(mock_client):
    """Test RetrievableFirstMixin coverage for missing blocks."""
    # Test with REQUIRE_TENANT = False
    class ResourceWithoutTenant(TestBaseResource, RetrievableFirstMixin):
        REQUIRE_TENANT = False
        REQUIRE_GRAPH_GUID = True
        MODEL = MockModel
        SEARCH_MODELS = (MockModel, MockModel)
    
    mock_client.request.return_value = {"id": "test-id", "name": "Test Resource"}
    
    # Pass required field 'id' for MockModel
    result = ResourceWithoutTenant.retrieve_first("test-graph-id", id="test-id")
    assert isinstance(result, MockModel)
    assert result.id == "test-id"
    
    # Test without graph_id (should use else URL path)
    result = ResourceWithoutTenant.retrieve_first(id="test-id")
    assert isinstance(result, MockModel)
    assert result.id == "test-id"
    
    # Test with MODEL = None
    class ResourceWithoutModel(TestBaseResource, RetrievableFirstMixin):
        REQUIRE_TENANT = False
        REQUIRE_GRAPH_GUID = True
        MODEL = None
        SEARCH_MODELS = (MockModel, MockModel)
    
    result = ResourceWithoutModel.retrieve_first("test-graph-id", id="test-id")
    assert result == {"id": "test-id", "name": "Test Resource"}
    
    # Test with include_data and include_subordinates (provide them as True)
    result = ResourceWithoutTenant.retrieve_first(
        "test-graph-id",
        id="test-id",
        include_data=True,
        include_subordinates=True
    )
    assert isinstance(result, MockModel)
    assert result.id == "test-id"
    
    # Test with REQUIRE_GRAPH_GUID = False
    class ResourceWithoutGraphGuid(TestBaseResource, RetrievableFirstMixin):
        REQUIRE_TENANT = False
        REQUIRE_GRAPH_GUID = False
        MODEL = MockModel
        SEARCH_MODELS = (MockModel, MockModel)
    
    result = ResourceWithoutGraphGuid.retrieve_first("test-graph-id", id="test-id")
    assert isinstance(result, MockModel)
    assert result.id == "test-id"
    
    # Test without graph_id when REQUIRE_GRAPH_GUID = False
    result = ResourceWithoutGraphGuid.retrieve_first(id="test-id")
    assert isinstance(result, MockModel)
    assert result.id == "test-id"


def test_retrievable_many_mixin_coverage(mock_client):
    """Test RetrievableManyMixin coverage for missing blocks."""
    # Test with REQUIRE_TENANT = False
    class ResourceWithoutTenant(TestBaseResource, RetrievableManyMixin):
        REQUIRE_TENANT = False
        REQUIRE_GRAPH_GUID = True
        MODEL = MockModel
    
    mock_client.request.return_value = [
        {"id": "test-id-1", "name": "Test Resource 1"},
        {"id": "test-id-2", "name": "Test Resource 2"}
    ]
    
    # Test with graph_guid (should use first URL path)
    result = ResourceWithoutTenant.retrieve_many(["test-id-1", "test-id-2"], "test-graph-guid")
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(item, MockModel) for item in result)
    
    # Test without graph_guid (should use else URL path)
    result = ResourceWithoutTenant.retrieve_many(["test-id-1", "test-id-2"])
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(item, MockModel) for item in result)
    
    # Test with MODEL = None
    class ResourceWithoutModel(TestBaseResource, RetrievableManyMixin):
        REQUIRE_TENANT = False
        REQUIRE_GRAPH_GUID = True
        MODEL = None
    
    result = ResourceWithoutModel.retrieve_many(["test-id-1", "test-id-2"], "test-graph-guid")
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(item, dict) for item in result)
    
    # Test with REQUIRE_GRAPH_GUID = False
    class ResourceWithoutGraphGuid(TestBaseResource, RetrievableManyMixin):
        REQUIRE_TENANT = False
        REQUIRE_GRAPH_GUID = False
        MODEL = MockModel
    
    result = ResourceWithoutGraphGuid.retrieve_many(["test-id-1", "test-id-2"], "test-graph-guid")
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(item, MockModel) for item in result)
