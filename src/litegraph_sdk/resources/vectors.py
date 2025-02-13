from uuid import UUID

from ..enums.vector_search_domain_enum import VectorSearchDomainEnum
from ..mixins import (
    AllRetrievableAPIResource,
    CreateableAPIResource,
    DeletableAPIResource,
    ExistsAPIResource,
    RetrievableAPIResource,
    SearchableAPIResource,
    UpdatableAPIResource,
)
from ..models.vector_metadata import VectorMetadataModel
from ..models.vector_search_request import VectorSearchRequestModel
from ..models.vector_search_response import VectorSearchResultModel


class Vector(
    ExistsAPIResource,
    CreateableAPIResource,
    RetrievableAPIResource,
    AllRetrievableAPIResource,
    UpdatableAPIResource,
    DeletableAPIResource,
    SearchableAPIResource,
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

        search_request = VectorSearchRequestModel(
            Domain=domain,
            Embeddings=embeddings,
            TenantGUID=tenant_guid,
            GraphGUID=graph_guid,
            Labels=labels or [],
            Tags=tags or {},
            Expr=filter_expr,
        )

        return cls.search(**search_request.model_dump(by_alias=True, mode="json"))
