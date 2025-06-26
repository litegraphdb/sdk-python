from typing import List

from ..configuration import get_client
from ..models.authentication_token import AuthenticationTokenModel
from ..models.tenant_metadata import TenantMetadataModel
from ..utils.url_helper import _get_url_v1


class Authentication:
    REQUIRE_TENANT = False
    REQUIRE_GRAPH_GUID = False
    RESOURCE_NAME = "token"

    @classmethod
    def retrieve_tenants_for_email(cls, email: str) -> List[TenantMetadataModel]:
        """
        Retrieves tenants associated with the given email.

        Args:
            email (str): The email address to retrieve tenants for.

        Returns:
            List[TenantMetadataModel]: The list of tenants associated with the email.
        """
        if not email:
            raise ValueError("email cannot be None or empty")

        client = get_client()
        headers = {"x-email": email}
        url = _get_url_v1(cls, "tenants")
        response = client.request("GET", url, headers=headers)
        return [TenantMetadataModel.model_validate(tenant) for tenant in response]

    @classmethod
    def generate_authentication_token(
        cls, email: str, password: str, tenant_guid: str
    ) -> AuthenticationTokenModel:
        """
        Generates an authentication token for the given email, password, and tenant GUID.

        Args:
            email (str): The email address.
            password (str): The password.
            tenant_guid (str): The tenant GUID.

        Returns:
            AuthenticationTokenModel: The authentication token model.
        """
        if not email:
            raise ValueError("email cannot be None or empty")
        if not password:
            raise ValueError("password cannot be None or empty")
        if not tenant_guid:
            raise ValueError("tenant_guid cannot be None or empty")

        client = get_client()
        headers = {
            "x-email": email,
            "x-password": password,
            "x-tenant-guid": tenant_guid,
        }
        url = _get_url_v1(cls)
        response = client.request("GET", url, headers=headers)
        return AuthenticationTokenModel.model_validate(response)

    @classmethod
    def retrieve_token_details(cls, token: str) -> AuthenticationTokenModel:
        """
        Retrieves details for the given authentication token.

        Args:
            token (str): The authentication token.

        Returns:
            AuthenticationTokenModel: The token details.
        """
        if not token:
            raise ValueError("token cannot be None or empty")

        client = get_client()
        headers = {"x-token": token}
        url = _get_url_v1(cls, "details")
        response = client.request("GET", url, headers=headers)
        return AuthenticationTokenModel.model_validate(response)
