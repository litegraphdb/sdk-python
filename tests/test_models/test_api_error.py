import pytest
from litegraph.enums.api_error_enum import ERROR_DESCRIPTIONS, ApiError_Enum
from litegraph.models.api_error import ApiErrorResponseModel
from pydantic import ValidationError
from litegraph.resources.credentials import Credential
from litegraph.resources.users import User
from litegraph.resources.labels import Label
from litegraph.resources.tags import Tag
from litegraph.resources.vectors import Vector
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
def valid_error_data():
    """Fixture providing valid error response data."""
    return {
        "Error": ApiError_Enum.not_found,
        "Context": "Resource ID: 123",
        "Description": "The requested resource was not found.",
    }


@pytest.fixture
def minimal_error_data():
    """Fixture providing minimal valid error response data."""
    return {"Error": ApiError_Enum.bad_request}


def test_valid_error_creation(valid_error_data):
    """Test creating an error response with all valid fields."""
    error = ApiErrorResponseModel(**valid_error_data)
    assert error.error == valid_error_data["Error"]
    assert error.context == valid_error_data["Context"]
    assert error.description == valid_error_data["Description"]


def test_minimal_error_creation(minimal_error_data):
    """Test creating an error response with only required fields."""
    error = ApiErrorResponseModel(**minimal_error_data)
    assert error.error == minimal_error_data["Error"]
    assert error.context is None
    assert error.description is None


def test_error_aliases():
    """Test that field aliases work correctly."""
    data = {
        "error": ApiError_Enum.bad_request,
        "context": "Test context",
        "description": "Test description",
    }
    error = ApiErrorResponseModel(**data)

    # Test model dump with aliases
    dumped = error.model_dump(by_alias=True)
    assert "Error" in dumped
    assert "Context" in dumped
    assert "Description" in dumped

    # Test values
    assert dumped["Error"] == data["error"]
    assert dumped["Context"] == data["context"]
    assert dumped["Description"] == data["description"]


def test_invalid_error_enum():
    """Test that invalid error enum values are rejected."""
    with pytest.raises(ValidationError):
        ApiErrorResponseModel(Error="INVALID_ERROR")


@pytest.mark.parametrize("error_enum", list(ApiError_Enum))
def test_all_error_enums(error_enum):
    """Test model creation with all possible error enum values."""
    error = ApiErrorResponseModel(Error=error_enum)
    assert error.error == error_enum
    assert error.error in ApiError_Enum


def test_optional_fields():
    """Test handling of optional fields."""
    # Test different combinations of optional fields
    test_cases = [
        {"Error": ApiError_Enum.not_found, "Context": "Test context"},
        {"Error": ApiError_Enum.not_found, "Description": "Test description"},
        {"Error": ApiError_Enum.not_found},
        {"Error": ApiError_Enum.not_found, "Context": None, "Description": None},
    ]

    for test_data in test_cases:
        error = ApiErrorResponseModel(**test_data)
        assert error.error == test_data["Error"]
        assert error.context == test_data.get("Context")
        assert error.description == test_data.get("Description")


def test_error_descriptions_mapping():
    """Test that error enums map to correct descriptions in ERROR_DESCRIPTIONS."""
    for error_enum in ApiError_Enum:
        assert error_enum in ERROR_DESCRIPTIONS
        assert isinstance(ERROR_DESCRIPTIONS[error_enum], str)
        assert len(ERROR_DESCRIPTIONS[error_enum]) > 0


def test_model_config():
    """Test model configuration options."""
    # Test that populate_by_name works with both alias and field names
    alias_data = {"Error": ApiError_Enum.bad_request, "Context": "Test context"}
    field_data = {"error": ApiError_Enum.bad_request, "context": "Test context"}

    error1 = ApiErrorResponseModel(**alias_data)
    error2 = ApiErrorResponseModel(**field_data)

    assert error1.error == error2.error
    assert error1.context == error2.context


def test_string_type_validation():
    """Test validation of string fields."""
    invalid_types = [
        {"Error": ApiError_Enum.not_found, "Context": 123},
        {"Error": ApiError_Enum.not_found, "Description": 123},
        {"Error": ApiError_Enum.not_found, "Context": True},
        {"Error": ApiError_Enum.not_found, "Description": []},
    ]

    for invalid_data in invalid_types:
        with pytest.raises(ValidationError):
            ApiErrorResponseModel(**invalid_data)


def test_model_serialization():
    """Test model serialization and deserialization."""
    original_data = {
        "Error": ApiError_Enum.not_found,
        "Context": "Test context",
        "Description": "Test description",
    }

    # Create model
    error = ApiErrorResponseModel(**original_data)

    # Serialize to dict
    serialized = error.model_dump(by_alias=True)

    # Create new model from serialized data
    new_error = ApiErrorResponseModel(**serialized)

    # Verify all fields match
    assert new_error.error == error.error
    assert new_error.context == error.context
    assert new_error.description == error.description


def test_empty_string_handling():
    """Test handling of empty strings in optional fields."""
    test_data = {"Error": ApiError_Enum.not_found, "Context": "", "Description": ""}

    error = ApiErrorResponseModel(**test_data)
    assert error.context == ""
    assert error.description == ""


@pytest.mark.parametrize(
    "error_enum,expected_description",
    [
        (ApiError_Enum.not_found, "The requested resource was not found."),
        (
            ApiError_Enum.bad_request,
            "We were unable to discern your request. Please check your URL, query, and request body.",
        ),
        (
            ApiError_Enum.authorization_failed,
            "Your authentication material was accepted, but you are not authorized to perform this request.",
        ),
    ],
)
def test_error_descriptions_content(error_enum, expected_description):
    """Test specific error descriptions content."""
    assert ERROR_DESCRIPTIONS[error_enum] == expected_description


def test_credential_enumerate_with_query(mock_client):
    """Test enumerating credentials with a query."""
    mock_response = {
        "Success": True,
        "MaxResults": 20,
        "IterationsRequired": 1,
        "ContinuationToken": None,
        "EndOfResults": True,
        "TotalRecords": 1,
        "RecordsRemaining": 0,
        "Objects": [
            {
                "GUID": "cred1",
                "TenantGUID": "tenant1",
                "UserGUID": "user1",
                "Name": "Test Credential"
            }
        ],
        "Timestamp": {
            "Start": "2023-01-01T00:00:00Z",
            "End": "2023-01-01T00:00:01Z",
            "TotalMS": 200.0,
            "Messages": {},
            "Metadata": None
        }
    }
    mock_client.request.return_value = mock_response
    
    from litegraph.models.expression import ExprModel
    from litegraph.enums.operator_enum import Opertator_Enum
    
    result = Credential.enumerate_with_query(
        max_results=20,
        expr=ExprModel(Left="field", Operator=Opertator_Enum.Equals, Right="value")
    )
    
    assert isinstance(result, EnumerationResultModel)
    assert result.success is True
    assert result.total_records == 1
    assert len(result.objects) == 1
    mock_client.request.assert_called_once()


def test_user_enumerate_with_query(mock_client):
    """Test enumerating users with a query."""
    mock_response = {
        "Success": True,
        "MaxResults": 15,
        "IterationsRequired": 1,
        "ContinuationToken": None,
        "EndOfResults": True,
        "TotalRecords": 2,
        "RecordsRemaining": 0,
        "Objects": [
            {"GUID": "user1", "TenantGUID": "tenant1", "Name": "User 1", "Email": "user1@test.com"},
            {"GUID": "user2", "TenantGUID": "tenant1", "Name": "User 2", "Email": "user2@test.com"}
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
    
    result = User.enumerate_with_query(
        max_results=15,
        expr=ExprModel(Left="field", Operator=Opertator_Enum.Equals, Right="value")
    )
    
    assert isinstance(result, EnumerationResultModel)
    assert result.success is True
    assert result.total_records == 2
    assert len(result.objects) == 2
    mock_client.request.assert_called_once()


def test_label_enumerate_with_query(mock_client):
    """Test enumerating labels with a query."""
    mock_response = {
        "Success": True,
        "MaxResults": 30,
        "IterationsRequired": 1,
        "ContinuationToken": None,
        "EndOfResults": True,
        "TotalRecords": 3,
        "RecordsRemaining": 0,
        "Objects": [
            {"GUID": "label1", "TenantGUID": "tenant1", "Name": "Label 1"},
            {"GUID": "label2", "TenantGUID": "tenant1", "Name": "Label 2"},
            {"GUID": "label3", "TenantGUID": "tenant1", "Name": "Label 3"}
        ],
        "Timestamp": {
            "Start": "2023-01-01T00:00:00Z",
            "End": "2023-01-01T00:00:01Z",
            "TotalMS": 250.0,
            "Messages": {},
            "Metadata": None
        }
    }
    mock_client.request.return_value = mock_response
    
    from litegraph.models.expression import ExprModel
    from litegraph.enums.operator_enum import Opertator_Enum
    
    result = Label.enumerate_with_query(
        max_results=30,
        expr=ExprModel(Left="field", Operator=Opertator_Enum.Equals, Right="value")
    )
    
    assert isinstance(result, EnumerationResultModel)
    assert result.success is True
    assert result.total_records == 3
    assert len(result.objects) == 3
    mock_client.request.assert_called_once()


def test_tag_enumerate_with_query(mock_client):
    """Test enumerating tags with a query."""
    mock_response = {
        "Success": True,
        "MaxResults": 40,
        "IterationsRequired": 1,
        "ContinuationToken": None,
        "EndOfResults": True,
        "TotalRecords": 2,
        "RecordsRemaining": 0,
        "Objects": [
            {"GUID": "tag1", "TenantGUID": "tenant1", "Name": "Tag 1", "Value": "value1"},
            {"GUID": "tag2", "TenantGUID": "tenant1", "Name": "Tag 2", "Value": "value2"}
        ],
        "Timestamp": {
            "Start": "2023-01-01T00:00:00Z",
            "End": "2023-01-01T00:00:01Z",
            "TotalMS": 180.0,
            "Messages": {},
            "Metadata": None
        }
    }
    mock_client.request.return_value = mock_response
    
    from litegraph.models.expression import ExprModel
    from litegraph.enums.operator_enum import Opertator_Enum
    
    result = Tag.enumerate_with_query(
        max_results=40,
        expr=ExprModel(Left="field", Operator=Opertator_Enum.Equals, Right="value")
    )
    
    assert isinstance(result, EnumerationResultModel)
    assert result.success is True
    assert result.total_records == 2
    assert len(result.objects) == 2
    mock_client.request.assert_called_once()


def test_vector_enumerate_with_query(mock_client):
    """Test enumerating vectors with a query."""
    mock_response = {
        "Success": True,
        "MaxResults": 10,
        "IterationsRequired": 1,
        "ContinuationToken": None,
        "EndOfResults": True,
        "TotalRecords": 1,
        "RecordsRemaining": 0,
        "Objects": [
            {
                "GUID": "00000000-0000-0000-0000-000000000000",
                "TenantGUID": "00000000-0000-0000-0000-000000000000",
                "NodeGUID": "00000000-0000-0000-0000-000000000000",
                "Name": "Vector 1",
                "Dimension": 128
            }
        ],
        "Timestamp": {
            "Start": "2023-01-01T00:00:00Z",
            "End": "2023-01-01T00:00:01Z",
            "TotalMS": 100.0,
            "Messages": {},
            "Metadata": None
        }
    }
    mock_client.request.return_value = mock_response
    
    from litegraph.models.expression import ExprModel
    from litegraph.enums.operator_enum import Opertator_Enum
    
    result = Vector.enumerate_with_query(
        max_results=10,
        expr=ExprModel(Left="field", Operator=Opertator_Enum.Equals, Right="value")
    )
    
    assert isinstance(result, EnumerationResultModel)
    assert result.success is True
    assert result.total_records == 1
    assert len(result.objects) == 1
    mock_client.request.assert_called_once()


def test_enumeration_error_handling(mock_client):
    """Test error handling in enumeration methods."""
    from litegraph.models.expression import ExprModel
    from litegraph.enums.operator_enum import Opertator_Enum
    from litegraph.exceptions import SdkException
    from unittest.mock import Mock
    
    # Test API error handling
    mock_client.request.side_effect = Exception("API connection error")
    
    with pytest.raises(Exception, match="API connection error"):
        Credential.enumerate_with_query(
            expr=ExprModel(Left="field", Operator=Opertator_Enum.Equals, Right="value")
        )


def test_enumeration_validation_errors(mock_client):
    """Test validation errors in enumeration."""
    from litegraph.models.expression import ExprModel
    from litegraph.enums.operator_enum import Opertator_Enum
    from pydantic import ValidationError
    
    # Test invalid max_results
    with pytest.raises(ValidationError):
        Credential.enumerate_with_query(
            max_results=0,  # Invalid: below minimum
            expr=ExprModel(Left="field", Operator=Opertator_Enum.Equals, Right="value")
        )
    
    with pytest.raises(ValidationError):
        Credential.enumerate_with_query(
            max_results=1001,  # Invalid: above maximum
            expr=ExprModel(Left="field", Operator=Opertator_Enum.Equals, Right="value")
        )


def test_enumeration_tenant_requirement_error(monkeypatch):
    """Test tenant GUID requirement error."""
    from litegraph.configuration import get_client
    from unittest.mock import Mock
    
    # Mock a client without tenant_guid
    mock_client = Mock()
    mock_client.tenant_guid = None
    mock_client.graph_guid = "test-graph"
    
    monkeypatch.setattr("litegraph.configuration._client", mock_client)
    
    from litegraph.models.expression import ExprModel
    from litegraph.enums.operator_enum import Opertator_Enum
    
    # All these resources require tenant GUID
    with pytest.raises(ValueError, match="Tenant GUID is required"):
        Credential.enumerate_with_query(
            expr=ExprModel(Left="field", Operator=Opertator_Enum.Equals, Right="value")
        )
    
    with pytest.raises(ValueError, match="Tenant GUID is required"):
        User.enumerate_with_query(
            expr=ExprModel(Left="field", Operator=Opertator_Enum.Equals, Right="value")
        )


def test_enumeration_with_continuation_token(mock_client):
    """Test enumeration with continuation token for pagination."""
    mock_response = {
        "Success": True,
        "MaxResults": 5,
        "IterationsRequired": 2,
        "ContinuationToken": "next_page_token_123",
        "EndOfResults": False,
        "TotalRecords": 25,
        "RecordsRemaining": 20,
        "Objects": [
            {"GUID": f"tag{i}", "TenantGUID": "tenant1", "Name": f"Tag {i}", "Value": f"value{i}"}
            for i in range(5)
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
    
    result = Tag.enumerate_with_query(
        max_results=5,
        continuation_token="previous_token_456",
        expr=ExprModel(Left="field", Operator=Opertator_Enum.Equals, Right="value")
    )
    
    assert isinstance(result, EnumerationResultModel)
    assert result.continuation_token == "next_page_token_123"
    assert result.end_of_results is False
    assert result.total_records == 25
    assert result.records_remaining == 20
    assert len(result.objects) == 5


def test_enumeration_with_empty_and_none_filters(mock_client):
    """Test enumeration with empty and None filter values."""
    mock_response = {
        "Success": True,
        "MaxResults": 10,
        "IterationsRequired": 1,
        "ContinuationToken": None,
        "EndOfResults": True,
        "TotalRecords": 1,
        "RecordsRemaining": 0,
        "Objects": [
            {"GUID": "00000000-0000-0000-0000-000000000000", "TenantGUID": "00000000-0000-0000-0000-000000000000", "NodeGUID": "00000000-0000-0000-0000-000000000000", "Name": "Vector 1", "Dimension": 128}
        ],
        "Timestamp": {
            "Start": "2023-01-01T00:00:00Z",
            "End": "2023-01-01T00:00:01Z",
            "TotalMS": 100.0,
            "Messages": {},
            "Metadata": None
        }
    }
    mock_client.request.return_value = mock_response
    
    from litegraph.models.expression import ExprModel
    from litegraph.enums.operator_enum import Opertator_Enum
    
    # Test with empty filters
    result = Vector.enumerate_with_query(
        max_results=10,
        labels=[],  # Empty list
        tags={},    # Empty dict
        expr=ExprModel(Left="field", Operator=Opertator_Enum.Equals, Right="value")
    )
    
    assert isinstance(result, EnumerationResultModel)
    assert result.success is True
    assert len(result.objects) == 1
    mock_client.request.assert_called_once()


def test_enumeration_serialization_consistency(mock_client):
    """Test that enumeration query serialization works consistently."""
    from litegraph.models.enumeration_query import EnumerationQueryModel
    from litegraph.models.expression import ExprModel
    from litegraph.enums.operator_enum import Opertator_Enum
    from litegraph.enums.enumeration_order_enum import EnumerationOrder_Enum
    
    mock_response = {
        "Success": True,
        "MaxResults": 25,
        "IterationsRequired": 1,
        "ContinuationToken": None,
        "EndOfResults": True,
        "TotalRecords": 1,
        "RecordsRemaining": 0,
        "Objects": [
            {"GUID": "label1", "TenantGUID": "tenant1", "Name": "Label 1"}
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
    
    # Test with various serialization scenarios
    result = Label.enumerate_with_query(
        ordering=EnumerationOrder_Enum.NameAscending,
        include_data=True,
        include_subordinates=True,
        max_results=25,
        labels=["test_label"],
        tags={"category": "test"},
        expr=ExprModel(Left="name", Operator=Opertator_Enum.Equals, Right="test")
    )
    
    assert isinstance(result, EnumerationResultModel)
    assert result.success is True
    
    # Verify the request was made with proper serialization
    mock_client.request.assert_called_once()
    call_args = mock_client.request.call_args
    assert call_args[0][0] == "POST"  # Method
    assert "json" in call_args[1]  # JSON data was sent
