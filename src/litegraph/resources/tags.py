from ..mixins import (
    AllRetrievableAPIResource,
    CreateableAPIResource,
    CreateableMultipleAPIResource,
    DeletableAPIResource,
    EnumerableAPIResource,
    EnumerableAPIResourceWithData,
    ExistsAPIResource,
    RetrievableAPIResource,
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
    EnumerableAPIResource,
    EnumerableAPIResourceWithData,
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
