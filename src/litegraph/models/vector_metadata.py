from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class VectorMetadataModel(BaseModel):
    """
    Vector metadata.
    """

    guid: Optional[UUID] = Field(default=None, alias="GUID")
    tenant_guid: Optional[UUID] = Field(default=None, alias="TenantGUID")
    graph_guid: Optional[UUID] = Field(default=None, alias="GraphGUID")
    node_guid: Optional[UUID] = Field(default=None, alias="NodeGUID")
    edge_guid: Optional[UUID] = Field(default=None, alias="EdgeGUID")
    model: Optional[str] = Field(default=None, alias="Model")
    dimensionality: int = Field(default=0, ge=0, alias="Dimensionality")
    content: str = Field(default="", alias="Content")
    vectors: Optional[List[float]] = Field(default=None, alias="Vectors")
    embeddings: Optional[List[float]] = Field(default=None, alias="Embeddings")
    created_utc: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), alias="CreatedUtc"
    )
    last_update_utc: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), alias="LastUpdateUtc"
    )

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)
