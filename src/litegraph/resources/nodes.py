from ..mixins import (
    AllRetrievableAPIResource,
    CreateableAPIResource,
    CreateableMultipleAPIResource,
    DeletableAPIResource,
    ExistsAPIResource,
    RetrievableAPIResource,
    SearchableAPIResource,
    UpdatableAPIResource,
    DeleteMultipleAPIResource,
    DeleteAllAPIResource
)
from ..configuration import get_client
from ..models.node import NodeModel
from ..models.search_node_edge import SearchRequest, SearchResult
from ..utils.url_helper import _get_url

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
):
    """
    Node resource class.
    """

    RESOURCE_NAME: str = "nodes"
    MODEL = NodeModel
    SEARCH_MODELS = SearchRequest, SearchResult
    REQUIRE_TENANT = True
    REQUIRE_GRAPH_GUID = True

    @classmethod
    def read_first(cls, graph_guid: str, **kwargs) -> NodeModel:
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
