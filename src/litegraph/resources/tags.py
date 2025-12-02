from ..mixins import (
    AllRetrievableAPIResource,
    CreateableAPIResource,
    CreateableMultipleAPIResource,
    DeletableAllEndpointMixin,
    DeletableAPIResource,
    DeletableEdgeResourceMixin,
    DeletableGraphResourceMixin,
    DeletableNodeResourceMixin,
    DeleteMultipleAPIResource,
    EnumerableAPIResource,
    EnumerableAPIResourceWithData,
    ExistsAPIResource,
    RetrievableAllEndpointMixin,
    RetrievableAPIResource,
    RetrievableEdgeResourceMixin,
    RetrievableManyMixin,
    RetrievableNodeResourceMixin,
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
    DeletableAllEndpointMixin,
    DeletableGraphResourceMixin,
    DeletableNodeResourceMixin,
    DeletableEdgeResourceMixin,
    DeleteMultipleAPIResource,
    EnumerableAPIResource,
    EnumerableAPIResourceWithData,
    RetrievableAllEndpointMixin,
    RetrievableEdgeResourceMixin,
    RetrievableManyMixin,
    RetrievableNodeResourceMixin,
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

    @classmethod
    def retrieve_all_tenant_tags(cls, tenant_guid: str | None = None) -> list[TagModel]:
        """
        Retrieve all tags for a tenant.
        Endpoint:
            /v1.0/tenants/{tenant}/tags/all
        """
        return super().retrieve_all_tenant(tenant_guid)

    @classmethod
    def retrieve_all_graph_tags(
        cls, tenant_guid: str, graph_guid: str
    ) -> list[TagModel]:
        """
        Retrieve all tags for a graph.
        Endpoint:
            /v1.0/tenants/{tenant}/graphs/{graph}/tags/all
        """
        return super().retrieve_all_graph(tenant_guid, graph_guid)

    @classmethod
    def retrieve_node_tags(
        cls, tenant_guid: str, graph_guid: str, node_guid: str
    ) -> list[TagModel]:
        """
        Retrieve tags for a specific node.
        Endpoint:
            /v1.0/tenants/{tenant}/graphs/{graph}/nodes/{node}/tags

        Args:
            tenant_guid: The tenant GUID.
            graph_guid: The graph GUID.
            node_guid: The node GUID.

        Returns:
            List of TagModel instances.
        """
        return super().retrieve_for_node(node_guid, tenant_guid, graph_guid)

    @classmethod
    def retrieve_edge_tags(
        cls, tenant_guid: str, graph_guid: str, edge_guid: str
    ) -> list[TagModel]:
        """
        Retrieve tags for a specific edge.
        Endpoint:
            /v1.0/tenants/{tenant}/graphs/{graph}/edges/{edge}/tags

        Args:
            tenant_guid: The tenant GUID.
            graph_guid: The graph GUID.
            edge_guid: The edge GUID.

        Returns:
            List of TagModel instances.
        """
        return super().retrieve_for_edge(edge_guid, tenant_guid, graph_guid)

    @classmethod
    def delete_all_tenant_tags(cls, tenant_guid: str) -> None:
        """
        Delete all tags for a tenant.
        Endpoint:
            /v1.0/tenants/{tenant}/tags/all
        """
        return super().delete_all_tenant(tenant_guid)

    @classmethod
    def delete_all_graph_tags(cls, tenant_guid: str, graph_guid: str) -> None:
        """
        Delete all tags for a graph.
        Endpoint:
            /v1.0/tenants/{tenant}/graphs/{graph}/tags/all
        """
        return super().delete_all_graph(tenant_guid, graph_guid)

    @classmethod
    def delete_graph_tags(cls, tenant_guid: str, graph_guid: str) -> None:
        """
        Delete tags for a specific graph.
        Endpoint:
            /v1.0/tenants/{tenant}/graphs/{graph}/tags

        Args:
            tenant_guid: The tenant GUID.
            graph_guid: The graph GUID.
        """
        return super().delete_for_graph(tenant_guid, graph_guid)

    @classmethod
    def delete_node_tags(
        cls, tenant_guid: str, graph_guid: str, node_guid: str
    ) -> None:
        """
        Delete tags for a specific node.
        Endpoint:
            /v1.0/tenants/{tenant}/graphs/{graph}/nodes/{node}/tags
        """
        return super().delete_for_node(node_guid, tenant_guid, graph_guid)

    @classmethod
    def delete_edge_tags(
        cls, tenant_guid: str, graph_guid: str, edge_guid: str
    ) -> None:
        """
        Delete tags for a specific edge.
        Endpoint:
            /v1.0/tenants/{tenant}/graphs/{graph}/edges/{edge}/tags
        """
        return super().delete_for_edge(edge_guid, tenant_guid, graph_guid)
