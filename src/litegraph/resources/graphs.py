from typing import Type

from pydantic import BaseModel

from ..configuration import get_client
from ..mixins import (
    AllRetrievableAPIResource,
    CreateableAPIResource,
    DeletableAPIResource,
    EnumerableAPIResource,
    EnumerableAPIResourceWithData,
    ExistsAPIResource,
    ExportGexfMixin,
    RetrievableAPIResource,
    RetrievableFirstMixin,
    RetrievableManyMixin,
    RetrievableStatisticsMixin,
    SearchableAPIResource,
    UpdatableAPIResource,
)
from ..models.existence_request import ExistenceRequestModel
from ..models.existence_result import ExistenceResultModel
from ..models.graph_statistics import GraphStatisticsModel
from ..models.graphs import GraphModel
from ..models.search_graphs import SearchRequestGraph, SearchResultGraph
from ..utils.url_helper import _get_url_v1


class Graph(
    ExistsAPIResource,
    CreateableAPIResource,
    RetrievableAPIResource,
    AllRetrievableAPIResource,
    UpdatableAPIResource,
    DeletableAPIResource,
    ExportGexfMixin,
    SearchableAPIResource,
    EnumerableAPIResource,
    EnumerableAPIResourceWithData,
    RetrievableStatisticsMixin,
    RetrievableFirstMixin,
    RetrievableManyMixin,
):
    """
    Graph resource class.
    """

    RESOURCE_NAME: str = "graphs"
    REQUIRE_TENANT: bool = True
    REQUIRE_GRAPH_GUID: bool = False
    MODEL = GraphModel
    SEARCH_MODELS = SearchRequestGraph, SearchResultGraph
    EXISTENCE_REQUEST_MODEL: Type[BaseModel] = ExistenceRequestModel
    EXISTENCE_RESPONSE_MODEL: Type[BaseModel] = ExistenceResultModel
    STATS_MODEL = GraphStatisticsModel

    @classmethod
    def delete(cls, resource_id: str, force: bool = False) -> None:
        """
        Delete a resource by its ID.
        """
        client = get_client()
        
        if cls.REQUIRE_TENANT and client.tenant_guid is None:
            raise ValueError("Tenant GUID is required for this resource.")

        url = (
            _get_url_v1(cls, client.tenant_guid, resource_id, force=None)
            if force
            else _get_url_v1(cls, client.tenant_guid, resource_id)
        )
        client.request("DELETE", url)

    @classmethod
    def batch_existence(
        cls, graph_guid: str, request: ExistenceRequestModel
    ) -> ExistenceResultModel:
        """
        Execute a batch existence request.
        """
        if request is None:
            raise ValueError("Request cannot be None")

        if not isinstance(request, cls.EXISTENCE_REQUEST_MODEL):
            raise TypeError(
                f"Request must be an instance of {cls.EXISTENCE_REQUEST_MODEL.__name__}"
            )

        if not request.contains_existence_request():
            raise ValueError("Request must contain at least one existence check")

        client = get_client()

        # Construct URL
        url = _get_url_v1(cls, client.tenant_guid, graph_guid, "existence")

        # Prepare request data
        data = request.model_dump(mode="json", by_alias=True)

        # Make the request
        headers = {"Content-Type": "application/json"}
        response = client.request(method="POST", url=url, json=data, headers=headers)

        # Parse and validate response

        return cls.EXISTENCE_RESPONSE_MODEL.model_validate(response)

    @classmethod
    def export_gexf(cls, graph_id: str, include_data: bool = False) -> str:
        params = {}
        if include_data:
            params["incldata"] = None
        return super().export_gexf(graph_id, **params)

    @classmethod
    def retrieve_statistics(
        cls, graph_guid: str | None = None
    ) -> GraphStatisticsModel | dict[str, GraphStatisticsModel]:
        """
        Retrieves statistics for a given resource.
        """
        if graph_guid:
            response = super().retrieve_statistics(graph_guid)
            return GraphStatisticsModel.model_validate(response)
        else:
            response = super().retrieve_statistics()
            return {
                k: GraphStatisticsModel.model_validate(v) for k, v in response.items()
            }

    @classmethod
    def retrieve_first(
        cls, graph_id: str | None = None, **kwargs: SearchRequestGraph
    ) -> GraphModel:
        """
        Retrieve the first graph.
        """
        graph_id = graph_id or kwargs.get("graph_guid")
        return super().retrieve_first(graph_id=graph_id, **kwargs)
