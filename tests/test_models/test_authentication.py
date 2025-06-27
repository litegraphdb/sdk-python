import pytest
from unittest.mock import Mock
from uuid import UUID

from litegraph.models.authentication_token import AuthenticationTokenModel
from litegraph.models.tenant_metadata import TenantMetadataModel
from litegraph.resources.authentication import Authentication
from pydantic import ValidationError


@pytest.fixture
def mock_client(monkeypatch):
    """Create a mock client and configure it."""
    client = Mock()
    client.base_url = "http://test-api.com"
    monkeypatch.setattr("litegraph.configuration._client", client)
    return client


@pytest.fixture
def valid_tenant_data():
    """Fixture providing valid tenant metadata."""
    return {
        "GUID": "550e8400-e29b-41d4-a716-446655440000",
        "Name": "Test Tenant",
        "Active": True,
        "CreatedUtc": "2024-01-01T00:00:00Z",
        "LastUpdateUtc": "2024-01-01T00:00:00Z"
    }


@pytest.fixture
def valid_token_data():
    """Fixture providing valid authentication token data."""
    return {
        "Token": "test-token-123",
        "TenantGUID": "550e8400-e29b-41d4-a716-446655440000",
        "UserGUID": "550e8400-e29b-41d4-a716-446655440000",
        "ExpirationUtc": "2024-01-02T00:00:00Z"
    }


def test_retrieve_tenants_for_email(mock_client, valid_tenant_data):
    """Test retrieving tenants for an email address."""
    mock_client.request.return_value = [valid_tenant_data]
    email = "test@example.com"

    tenants = Authentication.retrieve_tenants_for_email(email)

    assert len(tenants) == 1
    assert isinstance(tenants[0], TenantMetadataModel)
    assert str(tenants[0].guid) == valid_tenant_data["GUID"]
    assert tenants[0].name == valid_tenant_data["Name"]
    assert tenants[0].active

    mock_client.request.assert_called_once_with(
        "GET",
        "v1.0/token/tenants",
        headers={"x-email": email}
    )


def test_retrieve_tenants_empty_email():
    """Test retrieving tenants with empty email raises error."""
    with pytest.raises(ValueError, match="email cannot be None or empty"):
        Authentication.retrieve_tenants_for_email("")


def test_generate_authentication_token(mock_client, valid_token_data):
    """Test generating an authentication token."""
    mock_client.request.return_value = valid_token_data
    email = "test@example.com"
    password = "test-password"
    tenant_guid = "550e8400-e29b-41d4-a716-446655440000"

    token = Authentication.generate_authentication_token(email, password, tenant_guid)

    assert isinstance(token, AuthenticationTokenModel)
    assert token.token == valid_token_data["Token"]
    assert str(token.tenant_guid) == valid_token_data["TenantGUID"]
    assert token.user_guid == valid_token_data["UserGUID"]

    mock_client.request.assert_called_once_with(
        "GET",
        "v1.0/token",
        headers={
            "x-email": email,
            "x-password": password,
            "x-tenant-guid": tenant_guid
        }
    )


@pytest.mark.parametrize("email,password,tenant_guid", [
    ("", "password", "guid"),
    ("email", "", "guid"),
    ("email", "password", ""),
])
def test_generate_token_missing_params(email, password, tenant_guid):
    """Test generating token with missing parameters raises error."""
    with pytest.raises(ValueError):
        Authentication.generate_authentication_token(email, password, tenant_guid)


def test_retrieve_token_details(mock_client, valid_token_data):
    """Test retrieving token details."""
    mock_client.request.return_value = valid_token_data
    token = "test-token-123"

    token_details = Authentication.retrieve_token_details(token)

    assert isinstance(token_details, AuthenticationTokenModel)
    assert token_details.token == valid_token_data["Token"]
    assert str(token_details.tenant_guid) == valid_token_data["TenantGUID"]
    assert token_details.user_guid == valid_token_data["UserGUID"]

    mock_client.request.assert_called_once_with(
        "GET",
        "v1.0/token/details",
        headers={"x-token": token}
    )


def test_retrieve_token_details_empty_token():
    """Test retrieving token details with empty token raises error."""
    with pytest.raises(ValueError, match="token cannot be None or empty"):
        Authentication.retrieve_token_details("")


def test_token_model_validation():
    """Test validation of authentication token model."""
    invalid_data = {
        "Token": "test-token",
        "TenantGUID": "invalid-guid",  # Invalid UUID format
        "UserGUID": "invalid-guid",  # Invalid UUID format
        "ExpirationUtc": "invalid-date"  # Invalid date format
    }

    with pytest.raises(ValidationError):
        AuthenticationTokenModel(**invalid_data)


def test_tenant_model_validation():
    """Test validation of tenant metadata model."""
    invalid_data = {
        "GUID": "invalid-guid",  # Invalid UUID format
        "Name": "",  # Empty name
        "Active": True,
        "CreatedUtc": "invalid-date",  # Invalid date format
        "LastUpdateUtc": "invalid-date"  # Invalid date format
    }

    with pytest.raises(ValidationError):
        TenantMetadataModel(**invalid_data) 