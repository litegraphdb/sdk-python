from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class ReadFirstRequest(BaseModel):
    ordering: Optional[str] = Field(alias="Ordering")
    labels: Optional[List[str]] = Field(alias="Labels")
    tags: Optional[Dict[str, str]] = Field(alias="Tags")
    expr: Optional[Dict[str, str]] = Field(alias="Expr")
