import uuid
from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from ..enums.vector_index_type_enum import Vector_Index_Type_Enum


class HnswLiteVectorIndexModel(BaseModel):
    """
    Python model mirroring LiteGraph.Indexing.Vector.HnswLiteVectorIndex
    configuration and runtime state.
    """

    guid: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="GUID")
    graph_guid: Optional[str] = Field(default=None, alias="GraphGUID")
    vector_dimensionality: int = Field(default=0, alias="VectorDimensionality")
    vector_index_type: Vector_Index_Type_Enum = Field(default=Vector_Index_Type_Enum.HnswSqlite, alias="VectorIndexType")  # HnswRam, HnswSqlite
    vector_index_file: Optional[str] = Field(default=None, alias="VectorIndexFile")
    m: int = Field(default=16, alias="M")
    ef_construction: int = Field(default=200, alias="EfConstruction")
    default_ef: int = Field(default=50, alias="DefaultEf")
    distance_metric: str = Field(default="Cosine", alias="DistanceMetric")

    # Runtime statistics / state
    vector_count: int = Field(default=0, alias="VectorCount")
    index_file_size_bytes: Optional[int] = Field(default=None, alias="IndexFileSizeBytes")
    estimated_memory_bytes: Optional[int] = Field(default=None, alias="EstimatedMemoryBytes")

    last_rebuild_utc: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc), alias="LastRebuildUtc"
    )
    last_add_utc: Optional[datetime] = Field(default=None, alias="LastAddUtc")
    last_remove_utc: Optional[datetime] = Field(default=None, alias="LastRemoveUtc")
    last_search_utc: Optional[datetime] = Field(default=None, alias="LastSearchUtc")
    is_loaded: bool = Field(default=False, alias="IsLoaded")

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)
