from ..mixins import (
    AllRetrievableAPIResource,
    CreateableAPIResource,
    CreateableMultipleAPIResource,
    DeletableAPIResource,
    DeleteMultipleAPIResource,
    EnumerableAPIResource,
    EnumerableAPIResourceWithData,
    ExistsAPIResource,
    RetrievableAPIResource,
    RetrievableManyMixin,
    UpdatableAPIResource,
)
from ..models.enumeration_result import EnumerationResultModel
from ..models.tag import TagModel


class Tag(
    ExistsAPIResource,
    RetrievableAPIResource,
    AllRetrievableAPIResource,
    CreateableAPIResource,
    CreateableMultipleAPIResource,
    UpdatableAPIResource,
    DeletableAPIResource,
    DeleteMultipleAPIResource,
    EnumerableAPIResource,
    EnumerableAPIResourceWithData,
    RetrievableManyMixin,
):
    """Tags resource."""

    REQUIRE_GRAPH_GUID = False
    RESOURCE_NAME = "tags"
    MODEL = TagModel

    @classmethod
    def enumerate_with_query(cls, **kwargs) -> EnumerationResultModel:
        """
        Enumerate tags with a query.
        """
        return super().enumerate_with_query(_data=kwargs)
