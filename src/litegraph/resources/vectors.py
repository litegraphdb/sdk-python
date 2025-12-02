from uuid import UUID

from ..configuration import get_client
from ..enums.vector_search_domain_enum import VectorSearchDomainEnum
from ..mixins import (
    AllRetrievableAPIResource,
    CreateableAPIResource,
    CreateableMultipleAPIResource,
    DeletableAllEndpointMixin,
    DeletableAPIResource,
    DeletableEdgeResourceMixin,
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
from ..models.vector_metadata import VectorMetadataModel
from ..models.vector_search_request import VectorSearchRequestModel
from ..models.vector_search_response import VectorSearchResultModel
from ..utils.url_helper import _get_url_v1


class Vector(
    ExistsAPIResource,
    CreateableAPIResource,
    CreateableMultipleAPIResource,
    RetrievableAPIResource,
    RetrievableAllEndpointMixin,
    AllRetrievableAPIResource,
    UpdatableAPIResource,
    DeletableAPIResource,
    DeletableAllEndpointMixin,
    DeletableNodeResourceMixin,
    DeletableEdgeResourceMixin,
    EnumerableAPIResource,
    EnumerableAPIResourceWithData,
    RetrievableManyMixin,
    RetrievableNodeResourceMixin,
    RetrievableEdgeResourceMixin,
    DeleteMultipleAPIResource,
):
    """Vectors resource."""

    REQUIRE_GRAPH_GUID = False
    RESOURCE_NAME = "vectors"
    MODEL = VectorMetadataModel
    SEARCH_MODELS = (VectorSearchRequestModel, VectorSearchResultModel)

    @classmethod
    def search_vectors(
        cls,
        domain: VectorSearchDomainEnum,
        embeddings: list[float],
        tenant_guid: UUID,
        graph_guid: UUID = None,
        labels: list[str] = None,
        tags: dict = None,
        filter_expr: dict = None,
    ) -> VectorSearchResultModel:
        """
        Search vectors based on the provided criteria.

        Args:
            domain: Vector search domain (Graph, Node, Edge)
            embeddings: Vector embeddings to search with
            tenant_guid: Tenant GUID
            graph_guid: Optional Graph GUID
            labels: Optional list of labels to filter by
            tags: Optional dictionary of tags to filter by
            filter_expr: Optional filter expression

        Returns:
            VectorSearchResultModel containing search results
        """
        if not embeddings:
            raise ValueError(
                "The supplied vector list must include at least one value."
            )

        if (
            domain in [VectorSearchDomainEnum.Node, VectorSearchDomainEnum.Edge]
            and not graph_guid
        ):
            raise ValueError(
                "Graph GUID must be supplied when performing a node/edge vector search."
            )

        search_request = cls.SEARCH_MODELS[0](
            Domain=domain,
            Embeddings=embeddings,
            TenantGUID=tenant_guid,
            GraphGUID=graph_guid,
            Labels=labels or [],
            Tags=tags or {},
            Expr=filter_expr,
        )

        client = get_client()

        # Construct URL
        url = _get_url_v1(cls, graph_guid)

        # Prepare request data
        data = search_request.model_dump(mode="json", by_alias=True)

        # Make the request
        headers = {"Content-Type": "application/json"}
        responses = client.request(method="POST", url=url, json=data, headers=headers)

        # Parse and validate response

        return [cls.SEARCH_MODELS[1].model_validate(response) for response in responses]

    @classmethod
    def enumerate_with_query(cls, **kwargs) -> EnumerationResultModel:
        """
        Enumerate vectors with a query.
        """
        return super().enumerate_with_query(_data=kwargs)

    @classmethod
    def delete_all_tenant_vectors(cls, tenant_guid: str | None = None) -> None:
        """
        Delete all vectors for a tenant.
        """
        return super().delete_all_tenant(tenant_guid)

    @classmethod
    def delete_all_graph_vectors(
        cls, tenant_guid: str | None = None, graph_guid: str | None = None
    ) -> None:
        """
        Delete all vectors for a graph.

        Args:
            tenant_guid: The tenant GUID. If not provided, uses client.tenant_guid.
            graph_guid: The graph GUID. If not provided, uses client.graph_guid.
        """
        return super().delete_all_graph(tenant_guid, graph_guid)

    @classmethod
    def retrieve_all_tenant_vectors(
        cls, tenant_guid: str | None = None
    ) -> list[VectorMetadataModel]:
        """
        Retrieve all vectors for a tenant.
        """
        return super().retrieve_all_tenant(tenant_guid)

    @classmethod
    def retrieve_all_graph_vectors(
        cls, tenant_guid: str | None = None, graph_guid: str | None = None
    ) -> list[VectorMetadataModel]:
        """
        Retrieve all vectors for a graph.

        Args:
            tenant_guid: The tenant GUID. If not provided, uses client.tenant_guid.
            graph_guid: The graph GUID. If not provided, uses client.graph_guid.

        Returns:
            List of VectorMetadataModel instances.
        """
        return super().retrieve_all_graph(tenant_guid, graph_guid)

    @classmethod
    def retrieve_node_vectors(
        cls,
        node_guid: str,
        tenant_guid: str | None = None,
        graph_guid: str | None = None,
    ) -> list[VectorMetadataModel]:
        """
        Retrieve vectors for a specific node.

        Endpoint:
            /v1.0/tenants/{tenant}/graphs/{graph}/nodes/{node}/vectors

        Args:
            node_guid: The node GUID.
            tenant_guid: The tenant GUID. If not provided, uses client.tenant_guid.
            graph_guid: The graph GUID. If not provided, uses client.graph_guid.

        Returns:
            List of VectorMetadataModel instances.
        """
        return super().retrieve_for_node(node_guid, tenant_guid, graph_guid)

    @classmethod
    def retrieve_edge_vectors(
        cls,
        edge_guid: str,
        tenant_guid: str | None = None,
        graph_guid: str | None = None,
    ) -> list[VectorMetadataModel]:
        """
        Retrieve vectors for a specific edge.

        Endpoint:
            /v1.0/tenants/{tenant}/graphs/{graph}/edges/{edge}/vectors

        Args:
            edge_guid: The edge GUID.
            tenant_guid: The tenant GUID. If not provided, uses client.tenant_guid.
            graph_guid: The graph GUID. If not provided, uses client.graph_guid.

        Returns:
            List of VectorMetadataModel instances.
        """
        return super().retrieve_for_edge(edge_guid, tenant_guid, graph_guid)

    @classmethod
    def retrieve_graph_vectors(
        cls,
        tenant_guid: str | None = None,
        graph_guid: str | None = None,
        include_data: bool = False,
        include_subordinates: bool = False,
    ) -> list[VectorMetadataModel]:
        """
        Retrieve vectors for a specific graph.

        Endpoint:
            /v1.0/tenants/{tenant}/graphs/{graph}/vectors

        Args:
            tenant_guid: The tenant GUID. If not provided, uses client.tenant_guid.
            graph_guid: The graph GUID. If not provided, uses client.graph_guid.
            include_data: Whether to include data in the response.
            include_subordinates: Whether to include subordinates in the response.

        Returns:
            List of VectorMetadataModel instances.
        """
        return super().retrieve_for_graph(
            tenant_guid, graph_guid, include_data, include_subordinates
        )

    @classmethod
    def delete_graph_vectors(
        cls,
        tenant_guid: str | None = None,
        graph_guid: str | None = None,
    ) -> None:
        """
        Delete vectors for a specific graph.

        Endpoint:
            /v1.0/tenants/{tenant}/graphs/{graph}/vectors

        Args:
            tenant_guid: The tenant GUID. If not provided, uses client.tenant_guid.
            graph_guid: The graph GUID. If not provided, uses client.graph_guid.
        """
        return super().delete_for_graph(tenant_guid, graph_guid)

    @classmethod
    def delete_node_vectors(
        cls,
        node_guid: str,
        tenant_guid: str | None = None,
        graph_guid: str | None = None,
    ) -> None:
        """
        Delete vectors for a specific node.

        Endpoint:
            /v1.0/tenants/{tenant}/graphs/{graph}/nodes/{node}/vectors

        Args:
            node_guid: The node GUID.
            tenant_guid: The tenant GUID. If not provided, uses client.tenant_guid.
            graph_guid: The graph GUID. If not provided, uses client.graph_guid.
        """
        return super().delete_for_node(node_guid, tenant_guid, graph_guid)

    @classmethod
    def delete_edge_vectors(
        cls,
        edge_guid: str,
        tenant_guid: str | None = None,
        graph_guid: str | None = None,
    ) -> None:
        """
        Delete vectors for a specific edge.
        """
        return super().delete_for_edge(edge_guid, tenant_guid, graph_guid)
