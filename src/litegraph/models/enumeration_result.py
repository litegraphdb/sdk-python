from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .timestamp import TimestampModel

T = TypeVar("T")


class EnumerationResultModel(BaseModel, Generic[T]):
    """Object returned as the result of an enumeration."""

    success: bool = Field(
        default=True,
        alias="Success",
        description="Indicates if the enumeration operation was successful",
    )

    timestamp: TimestampModel = Field(
        default=TimestampModel(),
        alias="Timestamp",
        description="Timestamp of the enumeration",
    )

    max_results: int = Field(
        default=1000,
        alias="MaxResults",
        description="Maximum number of results to retrieve",
        ge=1,
    )

    iterations_required: int = Field(
        default=0, alias="IterationsRequired", description="Iterations required", ge=0
    )

    continuation_token: Optional[str] = Field(
        default=None,
        alias="ContinuationToken",
        description="Continuation token for pagination",
    )

    end_of_results: bool = Field(
        default=True,
        alias="EndOfResults",
        description="Boolean indicating end of results",
    )

    total_records: int = Field(
        default=0, alias="TotalRecords", description="Total number of records", ge=0
    )

    records_remaining: int = Field(
        default=0,
        alias="RecordsRemaining",
        description="Number of candidate records remaining in the enumeration",
        ge=0,
    )

    objects: List[T] = Field(
        default_factory=list, alias="Objects", description="List of enumerated objects"
    )

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("objects", mode="before")
    def validate_objects(cls, v: Optional[List[T]]) -> List[T]:
        """Ensure objects is never None."""
        return v or []
