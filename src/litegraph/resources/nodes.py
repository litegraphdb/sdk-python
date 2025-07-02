from ..mixins import (
    AllRetrievableAPIResource,
    CreateableAPIResource,
    CreateableMultipleAPIResource,
    DeletableAPIResource,
    DeleteAllAPIResource,
    DeleteMultipleAPIResource,
    EnumerableAPIResource,
    EnumerableAPIResourceWithData,
    ExistsAPIResource,
    RetrievableAPIResource,
    RetrievableFirstMixin,
    RetrievableManyMixin,
    SearchableAPIResource,
    UpdatableAPIResource,
)
from ..models.enumeration_result import EnumerationResultModel
from ..models.node import NodeModel
from ..models.search_node_edge import SearchRequest, SearchResult


class Node(
    ExistsAPIResource,
    CreateableAPIResource,
    CreateableMultipleAPIResource,
    RetrievableAPIResource,
    AllRetrievableAPIResource,
    UpdatableAPIResource,
    DeletableAPIResource,
    SearchableAPIResource,
    DeleteMultipleAPIResource,
    DeleteAllAPIResource,
    EnumerableAPIResource,
    EnumerableAPIResourceWithData,
    RetrievableFirstMixin,
    RetrievableManyMixin,
):
    """
    Node resource class.
    """

    RESOURCE_NAME: str = "nodes"
    MODEL = NodeModel
    SEARCH_MODELS = SearchRequest, SearchResult

    @classmethod
    def enumerate_with_query(cls, **kwargs) -> EnumerationResultModel:
        """
        Enumerate nodes with a query.
        """
        return super().enumerate_with_query(_data=kwargs)

    @classmethod
    def retrieve_first(
        cls, graph_id: str | None = None, **kwargs: SearchRequest
    ) -> NodeModel:
        """
        Retrieve the first node.
        """
        graph_id = graph_id or kwargs.get("graph_guid")
        return super().retrieve_first(graph_id=graph_id, **kwargs)
