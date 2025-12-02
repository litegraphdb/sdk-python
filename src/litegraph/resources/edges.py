from ..configuration import get_client
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
    RetrievableAllEndpointMixin,
    RetrievableAPIResource,
    RetrievableFirstMixin,
    RetrievableManyMixin,
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
    RetrievableAllEndpointMixin,
    RetrievableFirstMixin,
    RetrievableManyMixin,
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

    @classmethod
    def retrieve_all(cls, **kwargs) -> list[EdgeModel]:
        """
        Retrieve all edges.
        """
        return super().retrieve_all(**kwargs)

    @classmethod
    def retrieve_all_graph_edges(
        cls, tenant_guid: str, graph_guid: str
    ) -> list[EdgeModel]:
        """
        Get all edges for a graph inside a tenant.

        Calls:
            /v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/edges/all

        Args:
            tenant_guid: The tenant GUID.
            graph_guid:  The graph GUID.

        Returns:
            List of EdgeModel instances or raw response if MODEL is not defined.
        """
        return super().retrieve_all_graph(tenant_guid, graph_guid)

    @classmethod
    def retrieve_all_tenant_edges(
        cls, tenant_guid: str | None = None
    ) -> list[EdgeModel]:
        """
        Retrieve all edges for a tenant (no graph required).
        Endpoint:
            /v1.0/tenants/{tenant}/edges/all
        """
        return super().retrieve_all_tenant(tenant_guid)

    @classmethod
    def delete_all_tenant_edges(cls, tenant_guid: str):
        """
        Retrieve all edges for a tenant (no graph required).
        Endpoint:
            /v1.0/tenants/{tenant}/edges/all
        """
        client = get_client()

        # Construct URL manually because this endpoint does NOT use graph_guid
        url = f"v1.0/tenants/{tenant_guid}/edges/all"

        instance = client.request("DELETE", url)

        return instance

    @classmethod
    def delete_node_edges(cls, tenant_guid: str, graph_guid: str, node_guid: str):
        """
        Delete all edges for a specific node inside a graph.

        Calls:
            /v1.0/tenants/{tenant}/graphs/{graph}/nodes/{node_guid}/edges

        Args:
            tenant_guid: Tenant GUID.
            graph_guid:  Graph GUID.
            node_guid:   Node GUID whose edges will be deleted.

        Returns:
            Raw API response.
        """
        client = get_client()

        # Construct URL manually (because this is node → edges, not edge → nodes)
        url = f"v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/nodes/{node_guid}/edges"

        instance = client.request("DELETE", url)

        return instance

    @classmethod
    def delete_node_edges_bulk(
        cls, tenant_guid: str, graph_guid: str, node_guids: list[str]
    ):
        """
        Bulk delete edges for multiple nodes inside a graph.

        Calls:
            DELETE /v1.0/tenants/{tenant}/graphs/{graph}/nodes/edges/bulk

        Args:
            tenant_guid: Tenant GUID.
            graph_guid:  Graph GUID.
            node_guids:  List of node GUIDs whose edges will be deleted.

        Returns:
            Raw response from the API.
        """
        client = get_client()

        # Construct URL manually
        url = f"v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/nodes/edges/bulk"

        instance = client.request("DELETE", url, json=node_guids)
        return instance
