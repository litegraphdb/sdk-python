from pydantic import BaseModel, ConfigDict, Field, NonNegativeInt


class TenantStatisticsModel(BaseModel):
    """
    Tenant statistics model.
    """

    graphs: NonNegativeInt = Field(default=0, alias="Graphs")
    nodes: NonNegativeInt = Field(default=0, alias="Nodes")
    edges: NonNegativeInt = Field(default=0, alias="Edges")
    labels: NonNegativeInt = Field(default=0, alias="Labels")
    tags: NonNegativeInt = Field(default=0, alias="Tags")
    vectors: NonNegativeInt = Field(default=0, alias="Vectors")

    model_config = ConfigDict(populate_by_name=True)
