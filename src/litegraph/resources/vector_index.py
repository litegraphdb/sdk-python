from ..configuration import get_client
from ..mixins import (
    CreateableAPIResource,
    DeletableAPIResource,
    RetrievableAPIResource,
    RetrievableStatisticsMixin,
)
from ..models.hnsw_lite_vector_index import HnswLiteVectorIndexModel
from ..models.vector_index_statistics import VectorIndexStatisticsModel
from ..utils.url_helper import _get_url_v1, _get_url_v2


class VectorIndex(
    RetrievableAPIResource,
    RetrievableStatisticsMixin,
    CreateableAPIResource,
    DeletableAPIResource,
):
    """
    Vector Index resource class for managing vector indexes on graphs.

    This resource provides methods to:
    - Read vector index configuration
    - Read vector index statistics
    - Enable/configure vector index
    - Rebuild vector index
    - Delete vector index
    """

    RESOURCE_NAME: str = "vectorindex"
    REQUIRE_GRAPH_GUID: bool = True
    REQUIRE_TENANT: bool = True
    MODEL = HnswLiteVectorIndexModel
    STATS_MODEL = VectorIndexStatisticsModel

    @classmethod
    def get_config(cls, graph_guid: str) -> HnswLiteVectorIndexModel:
        """
        Read vector index configuration for a specific graph.

        Args:
            graph_guid: The GUID of the graph to get vector index config for

        Returns:
            HnswLiteVectorIndexModel: The vector index configuration

        Raises:
            ValueError: If tenant GUID or graph GUID is not provided
        """
        client = get_client()

        if client.tenant_guid is None:
            raise ValueError("Tenant GUID is required for this resource.")

        if not graph_guid:
            raise ValueError("Graph GUID is required for this resource.")

        url = _get_url_v1(cls, client.tenant_guid, graph_guid, "config")

        response = client.request("GET", url)
        return cls.MODEL(**response)

    @classmethod
    def get_stats(cls, graph_guid: str) -> VectorIndexStatisticsModel:
        """
        Read vector index statistics for a specific graph.

        Args:
            graph_guid: The GUID of the graph to get vector index stats for

        Returns:
            VectorIndexStatisticsModel: The vector index statistics

        Raises:
            ValueError: If tenant GUID or graph GUID is not provided
        """
        client = get_client()

        if client.tenant_guid is None:
            raise ValueError("Tenant GUID is required for this resource.")

        if not graph_guid:
            raise ValueError("Graph GUID is required for this resource.")

        url = _get_url_v1(cls, client.tenant_guid, graph_guid, "stats")

        response = client.request("GET", url)
        return cls.STATS_MODEL(**response)

    @classmethod
    def enable(
        cls, graph_guid: str, config: HnswLiteVectorIndexModel
    ) -> HnswLiteVectorIndexModel:
        """
        Enable vector index for a specific graph with the provided configuration.

        Args:
            graph_guid: The GUID of the graph to enable vector index for
            config: The vector index configuration

        Returns:
            HnswLiteVectorIndexModel: The enabled vector index configuration

        Raises:
            ValueError: If tenant GUID or graph GUID is not provided
            TypeError: If config is not an instance of HnswLiteVectorIndexModel
        """
        client = get_client()

        if client.tenant_guid is None:
            raise ValueError("Tenant GUID is required for this resource.")

        if not graph_guid:
            raise ValueError("Graph GUID is required for this resource.")

        if not isinstance(config, cls.MODEL):
            raise TypeError(f"Config must be an instance of {cls.MODEL.__name__}")

        url = _get_url_v2(cls, client.tenant_guid, graph_guid, "enable")

        # Prepare request data
        data = config.model_dump(mode="json", by_alias=True, exclude_unset=True)

        response = client.request("PUT", url, json=data)
        return cls.MODEL(**response)

    @classmethod
    def rebuild(cls, graph_guid: str) -> None:
        """
        Rebuild vector index for a specific graph.

        Args:
            graph_guid: The GUID of the graph to rebuild vector index for

        Raises:
            ValueError: If tenant GUID or graph GUID is not provided
        """
        client = get_client()

        if client.tenant_guid is None:
            raise ValueError("Tenant GUID is required for this resource.")

        if not graph_guid:
            raise ValueError("Graph GUID is required for this resource.")

        url = _get_url_v2(cls, client.tenant_guid, graph_guid, "rebuild")

        client.request("POST", url)

    @classmethod
    def delete(cls, graph_guid: str) -> None:
        """
        Delete vector index for a specific graph.

        Args:
            graph_guid: The GUID of the graph to delete vector index for

        Raises:
            ValueError: If tenant GUID or graph GUID is not provided
        """
        client = get_client()

        if client.tenant_guid is None:
            raise ValueError("Tenant GUID is required for this resource.")

        if not graph_guid:
            raise ValueError("Graph GUID is required for this resource.")

        url = _get_url_v2(cls, client.tenant_guid, graph_guid)

        client.request("DELETE", url)

    @classmethod
    def create_from_dict(
        cls, graph_guid: str, config_dict: dict
    ) -> HnswLiteVectorIndexModel:
        """
        Enable vector index for a specific graph using a dictionary configuration.

        This is a convenience method that creates a HnswLiteVectorIndexModel
        from a dictionary and then enables the vector index.

        Args:
            graph_guid: The GUID of the graph to enable vector index for
            config_dict: Dictionary containing vector index configuration
                        (e.g., VectorIndexType, VectorDimensionality, etc.)

        Returns:
            HnswLiteVectorIndexModel: The enabled vector index configuration

        Raises:
            ValueError: If tenant GUID or graph GUID is not provided
        """
        config = cls.MODEL(**config_dict)
        return cls.enable(graph_guid, config)
