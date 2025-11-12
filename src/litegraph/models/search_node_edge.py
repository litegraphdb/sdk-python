from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enums.enumeration_order_enum import EnumerationOrder_Enum
from ..models.edge import EdgeModel
from ..models.expression import ExprModel
from ..models.graphs import GraphModel
from ..models.node import NodeModel


class SearchRequest(BaseModel):
    """
    Search request for nodes and edges.
    """

    graph_guid: Optional[str] = Field(default=None, alias="GraphGUID")
    ordering: EnumerationOrder_Enum = Field(
        EnumerationOrder_Enum.CreatedDescending, alias="Ordering"
    )
    max_results: int = Field(default=5, ge=1, le=1000, alias="MaxResults")
    skip: int = Field(default=0, ge=0, alias="Skip")
    include_data: Optional[bool] = Field(default=False, alias="IncludeData")
    include_subordinates: Optional[bool] = Field(
        default=False, alias="IncludeSubordinates"
    )
    expr: Optional[ExprModel] = Field(None, alias="Expr")
    name: Optional[str] = Field(None, alias="Name")
    labels: Optional[List] = Field(None, alias="Labels")
    tags: Optional[Dict[str, str]] = Field(default_factory=dict, alias="Tags")
    model_config = ConfigDict(populate_by_name=True, populate_by_alias=True)


class SearchResult(BaseModel):
    """
    Search result for nodes.
    """

    nodes: Optional[List[NodeModel]] = Field(None, alias="Nodes")
    model_config = ConfigDict(populate_by_name=True)


class SearchResultEdge(BaseModel):
    """
    Search result for edges.
    """

    edges: Optional[List[EdgeModel]] = Field(None, alias="Edges")
    graphs: Optional[List[GraphModel]] = Field(None, alias="Graphs")
    nodes: Optional[List[NodeModel]] = Field(None, alias="Nodes")
    model_config = ConfigDict(populate_by_name=True)
