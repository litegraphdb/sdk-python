from datetime import datetime

from pydantic import BaseModel, Field


class BackupModel(BaseModel):
    """
    Backup of a graph.
    """

    filename: str = Field(alias="Filename")
    length: int = Field(alias="Length")
    md5_hash: str = Field(alias="MD5Hash")
    sha1_hash: str = Field(alias="SHA1Hash")
    sha256_hash: str = Field(alias="SHA256Hash")
    created_utc: datetime = Field(alias="CreatedUtc")
    last_update_utc: datetime = Field(alias="LastUpdateUtc")
    last_access_utc: datetime = Field(alias="LastAccessUtc")
