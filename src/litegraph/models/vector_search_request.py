from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from ..enums.vector_search_domain_enum import VectorSearchDomainEnum
from ..enums.vector_search_type_enum import VectorSearchTypeEnum
from ..models.expression import ExprModel


class VectorSearchRequestModel(BaseModel):
    """
    Vector search request.
    """

    tenant_guid: UUID | None = Field(default=None, alias="TenantGUID")
    graph_guid: Optional[UUID] = Field(default=None, alias="GraphGUID")
    domain: VectorSearchDomainEnum | None = Field(
        default=VectorSearchDomainEnum.Node, alias="Domain"
    )
    search_type: VectorSearchTypeEnum | None = Field(
        default=VectorSearchTypeEnum.CosineSimilarity, alias="SearchType"
    )
    labels: List[str] = Field(default_factory=list, alias="Labels")
    tags: Dict[str, str] = Field(default_factory=dict, alias="Tags")
    expr: Optional[ExprModel] = Field(default=None, alias="Expr")
    embeddings: Optional[List[float]] = Field(default=None, alias="Embeddings")

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)
