from datetime import datetime, timezone
from typing import Dict, Optional

from pydantic import BaseModel, ConfigDict, Field, computed_field


class TimestampModel(BaseModel):
    start: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), alias="Start"
    )
    end: Optional[datetime] = Field(None, alias="End")
    messages: Dict[datetime, str] = Field(default_factory=dict, alias="Messages")
    metadata: Optional[object] = Field(None, alias="Metadata")

    @computed_field(alias="TotalMS")
    def total_ms(self) -> float:
        if self.end is None:
            return round(
                (datetime.now(timezone.utc) - self.start).total_seconds() * 1000, 2
            )
        return round((self.end - self.start).total_seconds() * 1000, 2)

    def add_message(self, msg: str) -> None:
        if not msg:
            raise ValueError("Message cannot be empty.")
        self.messages[datetime.now(timezone.utc)] = msg

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
