from ..configuration import get_client
from ..mixins import (
    AllRetrievableAPIResource,
    CreateableAPIResource,
    CreateableMultipleAPIResource,
    DeletableAllEndpointMixin,
    DeletableAPIResource,
    DeleteAllAPIResource,
    DeleteMultipleAPIResource,
    EnumerableAPIResource,
    EnumerableAPIResourceWithData,
    ExistsAPIResource,
    RetrievableAllEndpointMixin,
    RetrievableAPIResource,
    RetrievableFirstMixin,
    RetrievableManyMixin,
    SearchableAPIResource,
    UpdatableAPIResource,
)
from ..models.enumeration_result import EnumerationResultModel
from ..models.node import NodeModel
from ..models.search_node_edge import SearchRequest, SearchResult
from ..utils.url_helper import _get_url_v1


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
    RetrievableAllEndpointMixin,
    DeletableAllEndpointMixin,
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

    @classmethod
    def delete_all_tenant_nodes(cls, tenant_guid: str) -> None:
        """
        Delete all nodes for a tenant.

        Endpoint:
            /v1.0/tenants/{tenant}/nodes/all

        Args:
            tenant_guid: The tenant GUID.
        """
        return super().delete_all_tenant(tenant_guid)

    @classmethod
    def retrieve_all_tenant_nodes(
        cls, tenant_guid: str | None = None
    ) -> list[NodeModel]:
        """
        Retrieve all nodes for a tenant.
        """
        return super().retrieve_all_tenant(tenant_guid)

    @classmethod
    def retrieve_all_graph_nodes(
        cls, tenant_guid: str, graph_guid: str
    ) -> list[NodeModel]:
        """
        Retrieve all nodes for a graph.
        """
        return super().retrieve_all_graph(tenant_guid, graph_guid)

    @classmethod
    def retrieve_most_connected_nodes(
        cls, tenant_guid: str, graph_guid: str
    ) -> list[NodeModel]:
        """
        Retrieve the most connected nodes in a graph.

        Endpoint:
            /v1.0/tenants/{tenant}/graphs/{graph}/nodes/mostconnected

        Args:
            tenant_guid: The tenant GUID.
            graph_guid: The graph GUID.

        Returns:
            List of NodeModel instances with connection statistics (EdgesIn, EdgesOut, EdgesTotal).
        """
        client = get_client()

        # Build URL: v1.0/tenants/{tenant}/graphs/{graph}/nodes/mostconnected
        url = _get_url_v1(cls, tenant_guid, graph_guid, "mostconnected")

        instance = client.request("GET", url)

        return (
            [cls.MODEL.model_validate(item) for item in instance]
            if getattr(cls, "MODEL", None)
            else instance
        )

    @classmethod
    def retrieve_least_connected_nodes(
        cls, tenant_guid: str, graph_guid: str
    ) -> list[NodeModel]:
        """
        Retrieve the least connected nodes in a graph.

        Endpoint:
            /v1.0/tenants/{tenant}/graphs/{graph}/nodes/leastconnected

        Args:
            tenant_guid: The tenant GUID.
            graph_guid: The graph GUID.

        Returns:
            List of NodeModel instances with connection statistics (EdgesIn, EdgesOut, EdgesTotal).
        """
        client = get_client()

        # Build URL: v1.0/tenants/{tenant}/graphs/{graph}/nodes/leastconnected
        url = _get_url_v1(cls, tenant_guid, graph_guid, "leastconnected")

        instance = client.request("GET", url)

        return (
            [cls.MODEL.model_validate(item) for item in instance]
            if getattr(cls, "MODEL", None)
            else instance
        )
