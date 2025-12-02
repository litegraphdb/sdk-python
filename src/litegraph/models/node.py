import uuid
from datetime import datetime, timezone
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..models.vector_metadata import VectorMetadataModel


class NodeModel(BaseModel):
    """
    Node in a graph.
    """

    guid: str = Field(
        default_factory=lambda: str(uuid.uuid4()), alias="GUID", strict=True
    )
    tenant_guid: str = Field(
        default_factory=lambda: str(uuid.uuid4()), alias="TenantGUID", strict=True
    )
    graph_guid: str = Field(
        default_factory=lambda: str(uuid.uuid4()), alias="GraphGUID", strict=True
    )
    name: Optional[str] = Field(default=None, alias="Name")
    data: Optional[dict] = Field(default=None, alias="Data")  # Object
    edges_in: Optional[int] = Field(default=None, alias="EdgesIn")
    edges_out: Optional[int] = Field(default=None, alias="EdgesOut")
    edges_total: Optional[int] = Field(default=None, alias="EdgesTotal")
    created_utc: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), alias="CreatedUtc"
    )
    last_update_utc: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), alias="LastUpdateUtc"
    )
    labels: Optional[list] = Field(default_factory=list, alias="Labels")
    tags: Optional[dict] = Field(default_factory=dict, alias="Tags")
    vectors: Optional[List[VectorMetadataModel]] = Field(
        default_factory=list, alias="Vectors"
    )
    model_config = ConfigDict(populate_by_name=True)
