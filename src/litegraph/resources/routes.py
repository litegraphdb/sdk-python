from ..configuration import get_client
from ..models.route_request import RouteRequestModel
from ..models.route_response import RouteResultModel
from ..utils.url_helper import _get_url_v1


class Routes:
    """
    Route resource class.
    """

    RESOURCE_NAME: str = "routes"
    MODEL = RouteRequestModel
    RESPONSE_MODEL = RouteResultModel
    REQUIRE_GRAPH_GUID = True
    REQUIRE_TENANT = True

    @classmethod
    def routes(cls, graph_guid: str, **kwargs):
        """
        Routes
        """
        headers = {"Content-Type": "application/json"}
        client = get_client()
        tenant = client.tenant_guid if cls.REQUIRE_TENANT else None
        tenant = kwargs.pop("tenant_guid", tenant)
        graph_id = client.graph_guid if cls.REQUIRE_GRAPH_GUID else None

        # Create the request model with the correct field mappings
        model_data = {}
        if "from_guid" in kwargs:
            model_data["from_node"] = kwargs["from_guid"]
        if "to_guid" in kwargs:
            model_data["to_node"] = kwargs["to_guid"]
        if "edge_filter" in kwargs:
            model_data["edge_filter"] = kwargs["edge_filter"]
        if "node_filter" in kwargs:
            model_data["node_filter"] = kwargs["node_filter"]
        
        request_model = cls.MODEL(graph=graph_guid, **model_data)
        
        # Convert to dict using by_alias=True to get the correct field names (From, To, Graph)
        request_data = request_model.model_dump(by_alias=True)

        url = _get_url_v1(cls, tenant, graph_id) if graph_id else _get_url_v1(cls, tenant, graph_guid)
        instance = client.request("POST", url, json=request_data, headers=headers)
        return cls.RESPONSE_MODEL.model_validate(instance) if cls.MODEL else instance
