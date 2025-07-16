from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..enums.enumeration_order_enum import EnumerationOrder_Enum
from .expression import ExprModel


class EnumerationQueryModel(BaseModel):
    ordering: EnumerationOrder_Enum = Field(
        default=EnumerationOrder_Enum.CreatedDescending, alias="Ordering"
    )
    include_data: Optional[bool] = Field(default=False, alias="IncludeData")
    include_subordinates: Optional[bool] = Field(
        default=False, alias="IncludeSubordinates"
    )
    max_results: int = Field(default=5, ge=1, le=1000, alias="MaxResults")
    continuation_token: Optional[str] = Field(None, alias="ContinuationToken")
    labels: List[str] = Field(default_factory=list, alias="Labels")
    tags: Dict[str, str] = Field(default_factory=dict, alias="Tags")
    expr: ExprModel = Field(default_factory=ExprModel, alias="Expr")

    model_config = ConfigDict(populate_by_name=True)
