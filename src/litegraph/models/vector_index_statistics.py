from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enums.vector_index_type_enum import Vector_Index_Type_Enum


class VectorIndexStatisticsModel(BaseModel):
    """
    Python model equivalent of LiteGraph.Indexing.Vector.VectorIndexStatistics
    """

    vector_count: int = Field(default=0, alias="VectorCount")
    dimensions: int = Field(default=0, alias="Dimensions")
    index_type: Vector_Index_Type_Enum = Field(
        default=Vector_Index_Type_Enum.HnswSqlite, alias="IndexType"
    )  # e.g., HnswRam, HnswSqlite
    m: int = Field(default=16, alias="M")
    ef_construction: int = Field(default=200, alias="EfConstruction")
    default_ef: int = Field(default=50, alias="DefaultEf")
    index_file: Optional[str] = Field(default=None, alias="IndexFile")
    index_file_size_bytes: Optional[int] = Field(
        default=None, alias="IndexFileSizeBytes"
    )
    estimated_memory_bytes: int = Field(default=0, alias="EstimatedMemoryBytes")

    last_rebuild_utc: Optional[datetime] = Field(default=None, alias="LastRebuildUtc")
    last_add_utc: Optional[datetime] = Field(default=None, alias="LastAddUtc")
    last_remove_utc: Optional[datetime] = Field(default=None, alias="LastRemoveUtc")
    last_search_utc: Optional[datetime] = Field(default=None, alias="LastSearchUtc")

    is_loaded: bool = Field(default=False, alias="IsLoaded")
    distance_metric: str = Field(default="Cosine", alias="DistanceMetric")

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)
