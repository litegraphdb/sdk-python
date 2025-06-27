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
    SearchableAPIResource,
    UpdatableAPIResource,
)
from ..models.edge import EdgeModel
from ..models.enumeration_result import EnumerationResultModel
from ..models.search_node_edge import SearchRequest, SearchResultEdge


class Edge(
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
):
    """
    Edge resource class.
    """

    RESOURCE_NAME: str = "edges"
    MODEL = EdgeModel
    SEARCH_MODELS = SearchRequest, SearchResultEdge

    @classmethod
    def enumerate_with_query(cls, **kwargs) -> EnumerationResultModel:
        """
        Enumerate edges with a query.
        """
        return super().enumerate_with_query(_data=kwargs)

    @classmethod
    def retrieve_first(
        cls, graph_id: str | None = None, **kwargs: SearchRequest
    ) -> EdgeModel:
        """
        Retrieve the first edge.
        """
        graph_id = graph_id or kwargs.get("graph_guid")
        return super().retrieve_first(graph_id=graph_id, **kwargs)
