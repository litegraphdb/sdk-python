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
    RetrievableManyMixin,
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

    @classmethod
    def retrieve(cls, guid: str, **kwargs) -> UserMasterModel:
        """
        Retrieve a user by its GUID.
        """
        return super().retrieve(guid, **kwargs)
    
    @classmethod
    def retrieve_multiple(cls, guids: list[str], **kwargs) -> list[UserMasterModel]:
        """
        Retrieve multiple users by their GUIDs.
        """
        return super().retrieve_many(guids, **kwargs)
    
    @classmethod
    def retrieve_all(cls, **kwargs) -> list[UserMasterModel]:
        """
        Retrieve all users.
        """
        return super().retrieve_all(**kwargs)