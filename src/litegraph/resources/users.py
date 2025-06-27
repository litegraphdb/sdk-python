from ..mixins import (
    AllRetrievableAPIResource,
    CreateableAPIResource,
    DeletableAPIResource,
    EnumerableAPIResource,
    EnumerableAPIResourceWithData,
    ExistsAPIResource,
    RetrievableAPIResource,
    UpdatableAPIResource,
)
from ..models.enumeration_result import EnumerationResultModel
from ..models.user_master import UserMasterModel


class User(
    ExistsAPIResource,
    RetrievableAPIResource,
    AllRetrievableAPIResource,
    CreateableAPIResource,
    UpdatableAPIResource,
    DeletableAPIResource,
    EnumerableAPIResource,
    EnumerableAPIResourceWithData,
):
    """Users resource."""

    REQUIRE_GRAPH_GUID = False
    RESOURCE_NAME = "users"
    MODEL = UserMasterModel

    @classmethod
    def enumerate_with_query(cls, **kwargs) -> EnumerationResultModel:
        """
        Enumerate users with a query.
        """
        return super().enumerate_with_query(_data=kwargs)
