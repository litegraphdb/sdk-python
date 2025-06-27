from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, Field


class TenantMetadataModel(BaseModel):
    """
    Tenant metadata.
    """

    guid: str | None = Field(default=None, alias="GUID")
    name: str | None = Field(default=None, alias="Name")
    active: bool = Field(default=True, alias="Active")
    created_utc: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), alias="CreatedUtc"
    )
    last_update_utc: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), alias="LastUpdateUtc"
    )

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)
