from ..mixins import (
    AllRetrievableAPIResource,
    CreateableAPIResource,
    CreateableMultipleAPIResource,
    DeletableAPIResource,
    DeleteAllAPIResource,
    DeleteMultipleAPIResource,
    ExistsAPIResource,
    RetrievableAPIResource,
    SearchableAPIResource,
    UpdatableAPIResource,
)
from ..models.edge import EdgeModel
from ..models.search_node_edge import SearchRequest, SearchResultEdge
from ..configuration import get_client
from ..utils.url_helper import _get_url


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
):
    """
    Edge resource class.
    """

    RESOURCE_NAME: str = "edges"
    MODEL = EdgeModel
    SEARCH_MODELS = SearchRequest, SearchResultEdge
    REQUIRE_TENANT = True
    REQUIRE_GRAPH_GUID = True

    @classmethod
    def read_first(cls, graph_guid: str, **kwargs) -> EdgeModel:
        """
        Read the first resource.

        Args:
            readFirstRequest: Additional keyword arguments to pass to the request.

        Returns:
            The first resource.
        """
        client = get_client()

        url = _get_url(cls, client.tenant_guid, graph_guid, "first")
        response = client.request("POST", url, json=kwargs)
        return cls.MODEL.model_validate(response)
