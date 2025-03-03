from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from ..models.edge import EdgeModel
from ..models.graphs import GraphModel
from ..models.node import NodeModel


class VectorSearchResultModel(BaseModel):
    """
    Vector search result.
    """

    score: Optional[float] = Field(default=None, alias="Score")
    distance: Optional[float] = Field(default=None, alias="Distance")
    inner_product: Optional[float] = Field(default=None, alias="InnerProduct")
    graph: Optional[GraphModel] = Field(default=None, alias="Graph")
    node: Optional[NodeModel] = Field(default=None, alias="Node")
    edge: Optional[EdgeModel] = Field(default=None, alias="Edge")

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)
