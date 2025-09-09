import uuid
from typing import Dict

from pydantic import BaseModel, ConfigDict, Field


class VectorIndexManagerModel(BaseModel):
    """
    Python model mirroring LiteGraph.Indexing.Vector.VectorIndexManager state.
    """

    guid: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="GUID")

    # Directory where index files are stored
    storage_directory: str = Field(..., alias="StorageDirectory")

    # Active index IDs (Graph GUIDs) mapped to index GUIDs or names
    indexes: Dict[str, str] = Field(default_factory=dict, alias="Indexes")

    # Whether manager has been disposed
    disposed: bool = Field(default=False, alias="Disposed")

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)
