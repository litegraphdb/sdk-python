from typing import Any

from ..configuration import get_client
from ..mixins import (
    AllRetrievableAPIResource,
    CreateableAPIResource,
    DeletableAPIResource,
    EnumerableAPIResource,
    EnumerableAPIResourceWithData,
    ExistsAPIResource,
    RetrievableAPIResource,
    RetrievableManyMixin,
    UpdatableAPIResource,
)
from ..models.credential import CredentialModel
from ..models.enumeration_result import EnumerationResultModel
from ..utils.url_helper import _get_url_v1


class Credential(
    ExistsAPIResource,
    RetrievableAPIResource,
    AllRetrievableAPIResource,
    CreateableAPIResource,
    UpdatableAPIResource,
    DeletableAPIResource,
    EnumerableAPIResource,
    EnumerableAPIResourceWithData,
    RetrievableManyMixin,
):
    """Credentials resource."""

    REQUIRE_GRAPH_GUID = False
    RESOURCE_NAME = "credentials"
    MODEL = CredentialModel

    @classmethod
    def enumerate_with_query(cls, **kwargs) -> EnumerationResultModel:
        """
        Enumerate credentials with a query.
        """
        return super().enumerate_with_query(_data=kwargs)

    @classmethod
    def get_bearer_credentials(cls, bearer_token: str) -> Any:
        """
        Get credential details for a bearer token.

        Calls:
            /v1.0/credentials/bearer/{bearerToken}

        Args:
            bearer_token: The bearer token to look up.

        Returns:
            Parsed response using MODEL if cls.MODEL is defined,
            otherwise the raw response from the client.
        """
        client = get_client()

        # Build URL manually: v1.0/credentials/bearer/{bearer_token}
        # This endpoint doesn't follow the tenant/graph/resource pattern
        url = f"v1.0/{cls.RESOURCE_NAME}/bearer/{bearer_token}"

        instance = client.request("GET", url)

        return (
            cls.MODEL.model_validate(instance)
            if getattr(cls, "MODEL", None)
            else instance
        )

    @classmethod
    def delete_all_tenant_credentials(cls, tenant_guid: str) -> None:
        """
        Delete credentials for the given tenant.

        Calls:
            /v1.0/tenants/{tenant_guid}/credentials

        Args:
            tenant_guid: The tenant GUID whose credentials should be deleted.
        """
        client = get_client()

        # Build URL: v1.0/tenants/{tenant}/credentials
        url = _get_url_v1(cls, tenant_guid)

        # Perform DELETE request
        client.request("DELETE", url)

    @classmethod
    def delete_user_credentials(cls, tenant_guid: str, user_guid: str) -> None:
        """
        Delete credentials for a specific user under a tenant.

        Calls:
            /v1.0/tenants/{tenant_guid}/users/{user_guid}/credentials

        Args:
            tenant_guid: Tenant GUID.
            user_guid:   User GUID whose credentials will be deleted.
        """
        client = get_client()

        # Build:
        # v1.0/tenants/{tenant}/users/{user_guid}/credentials
        url = _get_url_v1(cls, tenant_guid, user_guid, "credentials")

        client.request("DELETE", url)
