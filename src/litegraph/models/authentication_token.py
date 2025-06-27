from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, computed_field


class AuthenticationTokenModel(BaseModel):
    """Authentication token details."""

    timestamp_utc: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), alias="TimestampUtc"
    )
    expiration_utc: datetime | None = Field(default=None, alias="ExpirationUtc")
    administrator_guid: Optional[str] = Field(default=None, alias="AdministratorGUID")
    tenant_guid: Optional[str] = Field(default=None, alias="TenantGUID")
    user_guid: Optional[str] = Field(default=None, alias="UserGUID")
    token: Optional[str] = Field(default=None, alias="Token")
    valid: bool = Field(default=True, alias="Valid")

    model_config = ConfigDict(populate_by_name=True)

    @computed_field
    def is_expired(self) -> bool:
        """Boolean to indicate if the token is expired."""
        if self.expiration_utc is None:
            return False
        return self.timestamp_utc > self.expiration_utc
