from ..mixins import (
    AllRetrievableAPIResource,
    CreateableAPIResource,
    CreateableMultipleAPIResource,
    DeletableAllEndpointMixin,
    DeletableAPIResource,
    DeletableEdgeResourceMixin,
    DeletableGraphResourceMixin,
    DeletableNodeResourceMixin,
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
from ..models.label import LabelModel


class Label(
    ExistsAPIResource,
    RetrievableAPIResource,
    AllRetrievableAPIResource,
    CreateableAPIResource,
    CreateableMultipleAPIResource,
    UpdatableAPIResource,
    DeletableAPIResource,
    DeletableAllEndpointMixin,
    DeletableEdgeResourceMixin,
    DeletableGraphResourceMixin,
    DeletableNodeResourceMixin,
    EnumerableAPIResource,
    EnumerableAPIResourceWithData,
    RetrievableAllEndpointMixin,
    RetrievableEdgeResourceMixin,
    RetrievableManyMixin,
    RetrievableNodeResourceMixin,
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

    @classmethod
    def retrieve_all_tenant_labels(
        cls, tenant_guid: str | None = None
    ) -> list[LabelModel]:
        """
        Retrieve all labels for a tenant.
        Endpoint:
            /v1.0/tenants/{tenant}/labels/all
        """
        return super().retrieve_all_tenant(tenant_guid)

    @classmethod
    def retrieve_all_graph_labels(
        cls, tenant_guid: str, graph_guid: str
    ) -> list[LabelModel]:
        """
        Retrieve all labels for a graph.
        Endpoint:
            /v1.0/tenants/{tenant}/graphs/{graph}/labels/all
        """
        return super().retrieve_all_graph(tenant_guid, graph_guid)

    @classmethod
    def retrieve_graph_labels(
        cls,
        tenant_guid: str | None = None,
        graph_guid: str | None = None,
        include_data: bool = False,
        include_subordinates: bool = False,
    ) -> list[LabelModel]:
        """
        Retrieve labels for a specific graph.

        Endpoint:
            /v1.0/tenants/{tenant}/graphs/{graph}/labels

        Args:
            tenant_guid: The tenant GUID. If not provided, uses client.tenant_guid.
            graph_guid: The graph GUID. If not provided, uses client.graph_guid.
            include_data: Whether to include data in the response.
            include_subordinates: Whether to include subordinates in the response.

        Returns:
            List of LabelModel instances.
        """
        return super().retrieve_for_graph(
            tenant_guid, graph_guid, include_data, include_subordinates
        )

    @classmethod
    def retrieve_node_labels(
        cls, tenant_guid: str, graph_guid: str, node_guid: str
    ) -> list[LabelModel]:
        """
        Retrieve labels for a specific node.
        Endpoint:
            /v1.0/tenants/{tenant}/graphs/{graph}/nodes/{node}/labels

        Args:
            tenant_guid: The tenant GUID.
            graph_guid: The graph GUID.
            node_guid: The node GUID.

        Returns:
            List of LabelModel instances.
        """
        return super().retrieve_for_node(node_guid, tenant_guid, graph_guid)

    @classmethod
    def retrieve_edge_labels(
        cls, tenant_guid: str, graph_guid: str, edge_guid: str
    ) -> list[LabelModel]:
        """
        Retrieve labels for a specific edge.
        Endpoint:
            /v1.0/tenants/{tenant}/graphs/{graph}/edges/{edge}/labels

        Args:
            tenant_guid: The tenant GUID.
            graph_guid: The graph GUID.
            edge_guid: The edge GUID.

        Returns:
            List of LabelModel instances.
        """
        return super().retrieve_for_edge(edge_guid, tenant_guid, graph_guid)

    @classmethod
    def delete_all_tenant_labels(cls, tenant_guid: str) -> None:
        """
        Delete all labels for a tenant.
        Endpoint:
            /v1.0/tenants/{tenant}/labels/all
        """
        return super().delete_all_tenant(tenant_guid)

    @classmethod
    def delete_all_graph_labels(cls, tenant_guid: str, graph_guid: str) -> None:
        """
        Delete all labels for a graph.
        Endpoint:
            /v1.0/tenants/{tenant}/graphs/{graph}/labels/all
        """
        return super().delete_all_graph(tenant_guid, graph_guid)

    @classmethod
    def delete_graph_labels(cls, tenant_guid: str, graph_guid: str) -> None:
        """
        Delete labels for a specific graph.
        Endpoint:
            /v1.0/tenants/{tenant}/graphs/{graph}/labels

        Args:
            tenant_guid: The tenant GUID.
            graph_guid: The graph GUID.
        """
        return super().delete_for_graph(tenant_guid, graph_guid)

    @classmethod
    def delete_node_labels(
        cls, tenant_guid: str, graph_guid: str, node_guid: str
    ) -> None:
        """
        Delete labels for a specific node.
        Endpoint:
            /v1.0/tenants/{tenant}/graphs/{graph}/nodes/{node}/labels

        Args:
            tenant_guid: The tenant GUID.
            graph_guid: The graph GUID.
            node_guid: The node GUID.
        """
        return super().delete_for_node(node_guid, tenant_guid, graph_guid)

    @classmethod
    def delete_edge_labels(
        cls, tenant_guid: str, graph_guid: str, edge_guid: str
    ) -> None:
        """
        Delete labels for a specific edge.
        Endpoint:
            /v1.0/tenants/{tenant}/graphs/{graph}/edges/{edge}/labels

        Args:
            tenant_guid: The tenant GUID.
            graph_guid: The graph GUID.
            edge_guid: The edge GUID.
        """
        return super().delete_for_edge(edge_guid, tenant_guid, graph_guid)
