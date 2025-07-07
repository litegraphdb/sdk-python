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
