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
from ..models.label import LabelModel


class Label(
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
    """Labels resource."""

    REQUIRE_GRAPH_GUID = False
    RESOURCE_NAME = "labels"
    MODEL = LabelModel

    @classmethod
    def enumerate_with_query(cls, **kwargs) -> EnumerationResultModel:
        """
        Enumerate labels with a query.
        """
        return super().enumerate_with_query(_data=kwargs)
