import json
import uuid
from typing import Any, Dict, List, Optional, Type

from pydantic import BaseModel

from .configuration import get_client
from .enums.severity_enum import Severity_Enum
from .exceptions import GRAPH_REQUIRED_ERROR, TENANT_REQUIRED_ERROR, SdkException
from .models.enumeration_query import EnumerationQueryModel
from .models.enumeration_result import EnumerationResultModel
from .sdk_logging import log_error
from .utils.url_helper import _get_url_base, _get_url_v1, _get_url_v2

JSON_CONTENT_TYPE = {"Content-Type": "application/json"}


class ExistsAPIResource:
    """
    Mixin class for checking if a resource exists.
    If the resource exists, the method returns `True`, otherwise it returns `False`.
    """

    RESOURCE_NAME: str = ""
    REQUIRE_TENANT: bool = True

    @classmethod
    def exists(cls, guid: str) -> bool:
        client = get_client()
        if cls.REQUIRE_TENANT and client.tenant_guid is None:
            raise ValueError(TENANT_REQUIRED_ERROR)
        graph_id = client.graph_guid
        tenant = client.tenant_guid if cls.REQUIRE_TENANT else None
        url = (
            _get_url_v1(cls, tenant, graph_id, guid)
            if graph_id and cls.REQUIRE_GRAPH_GUID
            else _get_url_v1(cls, tenant, guid)
        )

        try:
            client.request("HEAD", url)
            return True
        except Exception:
            return False


class CreateableAPIResource:
    """
    A mixin class for creating resources.
    This class implements a generic creation pattern for resources using Pydantic models
    for data validation and serialization.
    """

    MODEL: Optional[Type[BaseModel]] = None
    RESOURCE_NAME: str = ""
    REQUIRE_TENANT: bool = True
    CREATE_METHOD: str = "PUT"

    @classmethod
    def create(cls, **kwargs) -> "BaseModel":
        """
        Creates a new resource.

        Args:
            **kwargs: Keyword arguments for the request, including the resource data.
                - headers (dict, optional): Additional headers for the request.
                - _data (dict, optional): The data to be sent in the request body.

        Returns:
            BaseModel: The created resource, validated against the MODEL if defined.

        Raises:
            ValueError: If tenant GUID or graph GUID is required but not provided.
        """
        client = get_client()
        headers = kwargs.pop("headers", {})

        if cls.REQUIRE_TENANT and client.tenant_guid is None:
            raise ValueError(TENANT_REQUIRED_ERROR)

        graph_id = kwargs.pop("graph_guid", None) or client.graph_guid
        if cls.REQUIRE_GRAPH_GUID and not graph_id:
            raise ValueError(GRAPH_REQUIRED_ERROR)

        # Extract data from kwargs
        _data = kwargs.pop("_data", kwargs.copy())

        # Build URL based on requirements
        tenant = client.tenant_guid if cls.REQUIRE_TENANT else None
        url = (
            _get_url_v1(cls, tenant, graph_id)
            if graph_id and cls.REQUIRE_GRAPH_GUID
            else _get_url_v1(cls, tenant)
        )
        if cls.MODEL is not None:
            data = cls.MODEL(**_data).model_dump(
                mode="json", by_alias=True, exclude_unset=True
            )
        else:
            data = _data

        # Make request and validate response
        instance = client.request(cls.CREATE_METHOD, url, json=data, headers=headers)
        return cls.MODEL.model_validate(instance) if cls.MODEL else instance


class CreateableMultipleAPIResource:
    """
    A mixin class for creating multiple resources at once.
    This class implements a generic creation pattern for multiple resources using Pydantic models
    for data validation and serialization.
    """

    MODEL: Optional[Type[BaseModel]] = None
    RESOURCE_NAME: str = ""
    REQUIRE_TENANT: bool = True

    @classmethod
    def create_multiple(cls, data: List[dict]) -> List[BaseModel]:
        """
        Creates multiple nodes or edges in a single request.
        """
        if data is None:
            raise TypeError("Nodes parameter cannot be None")

        if not data:
            return []

        client = get_client()
        if cls.REQUIRE_TENANT and client.tenant_guid is None:
            raise ValueError(TENANT_REQUIRED_ERROR)
        graph_id = client.graph_guid

        # Validate and serialize each node if MODEL is provided
        if cls.MODEL is not None:
            validated_nodes = [
                cls.MODEL(**node).model_dump(mode="json", by_alias=True)
                for node in data
            ]
        else:
            validated_nodes = data

        # Construct URL for multiple creation
        tenant = client.tenant_guid if cls.REQUIRE_TENANT else None
        url = (
            _get_url_v1(cls, tenant, graph_id, "bulk")
            if graph_id and cls.REQUIRE_GRAPH_GUID
            else _get_url_v1(cls, tenant, "bulk")
        )

        # Make the request
        instances = client.request("PUT", url, json=validated_nodes)

        # Validate response data if MODEL is provided
        if cls.MODEL is not None:
            return [cls.MODEL.model_validate(instance) for instance in instances]
        return instances


class RetrievableAPIResource:
    """
    A mixin class for retrieving resources.
    This class implements a generic retrieval pattern for resources using Pydantic models
    (for data validation and deserialization).
    """

    RESOURCE_NAME: str = ""
    REQUIRE_GRAPH_GUID: bool = True
    MODEL: Optional[Type[BaseModel]] = None
    REQUIRE_TENANT: bool = True

    @classmethod
    def retrieve(cls, guid: str, **kwargs) -> "BaseModel":
        """
        Retrieve a specific instance of the resource by its ID.
        """
        client = get_client()
        if cls.REQUIRE_TENANT and client.tenant_guid is None:
            raise ValueError(TENANT_REQUIRED_ERROR)
        graph_id = kwargs.pop("graph_guid", None) or client.graph_guid
        if cls.REQUIRE_GRAPH_GUID and not graph_id:
            raise ValueError(GRAPH_REQUIRED_ERROR)
        tenant = client.tenant_guid if cls.REQUIRE_TENANT else None
        include = {}
        if kwargs.get("include_data"):
            include["incldata"] = None
        if kwargs.get("include_subordinates"):
            include["inclsub"] = None

        url = (
            _get_url_v1(cls, tenant, graph_id, guid, **include)
            if graph_id and cls.REQUIRE_GRAPH_GUID
            else _get_url_v1(cls, tenant, guid, **include)
        )
        instance = client.request("GET", url)

        return cls.MODEL.model_validate(instance) if cls.MODEL else instance


class UpdatableAPIResource:
    """
    A mixin class for updating resources.
    This class implements a generic update pattern for resources using Pydantic models(for data validation and serialization).
    """

    RESOURCE_NAME: str = ""
    MODEL: Optional[Type[BaseModel]] = None
    REQUIRE_GRAPH_GUID: bool = True
    REQUIRE_TENANT: bool = True

    @classmethod
    def update(cls, guid: str, **kwargs) -> "BaseModel":
        """
        Update a specific instance of the resource by its ID.
        """
        client = get_client()
        if cls.REQUIRE_TENANT and client.tenant_guid is None:
            raise ValueError(TENANT_REQUIRED_ERROR)
        graph_id = client.graph_guid
        if cls.REQUIRE_GRAPH_GUID and not graph_id:
            raise ValueError(GRAPH_REQUIRED_ERROR)
        tenant = client.tenant_guid if cls.REQUIRE_TENANT else None
        url = (
            _get_url_v1(cls, tenant, graph_id, guid)
            if graph_id and cls.REQUIRE_GRAPH_GUID
            else _get_url_v1(cls, tenant, guid)
        )

        if cls.MODEL is not None:
            data = cls.MODEL(**kwargs).model_dump(
                mode="json", by_alias=True, exclude_unset=True, exclude_defaults=True
            )
        else:
            data = kwargs
        instance = client.request("PUT", url, json=data)

        return cls.MODEL.model_validate(instance) if cls.MODEL else instance


class DeletableAPIResource:
    """
    A mixin class for deleting resources.
    This class implements a generic delete pattern for resources for a specific resource.
    """

    RESOURCE_NAME: str = ""
    REQUIRE_GRAPH_GUID: bool = True
    REQUIRE_TENANT: bool = True

    @classmethod
    def delete(cls, guid: str, **kwargs) -> None:
        """
        Delete a resource by its ID.
        """
        client = get_client()
        if cls.REQUIRE_TENANT and client.tenant_guid is None:
            raise ValueError(TENANT_REQUIRED_ERROR)
        graph_id = client.graph_guid
        if cls.REQUIRE_GRAPH_GUID and not graph_id:
            raise ValueError(GRAPH_REQUIRED_ERROR)
        tenant = client.tenant_guid if cls.REQUIRE_TENANT else None
        url = (
            _get_url_v1(cls, tenant, graph_id, guid, **kwargs)
            if graph_id and cls.REQUIRE_GRAPH_GUID
            else _get_url_v1(cls, tenant, guid, **kwargs)
        )

        client.request("DELETE", url)


class DeleteMultipleAPIResource:
    """
    A mixin class for deleting multiple resources.
    This class implements a generic delete pattern for resources for a specific resource.
    """

    RESOURCE_NAME: str = ""
    REQUIRE_GRAPH_GUID: bool = True
    REQUIRE_TENANT: bool = True

    @classmethod
    def delete_multiple(cls, guid: List[str]) -> None:
        """
        Delete multiple resources by their IDs.
        """
        if not isinstance(guid, list):
            raise TypeError("Input must be a list of IDs")

        if not guid:
            return

        client = get_client()
        if cls.REQUIRE_TENANT and client.tenant_guid is None:
            raise ValueError(TENANT_REQUIRED_ERROR)
        graph_id = client.graph_guid if cls.REQUIRE_GRAPH_GUID else None

        if cls.REQUIRE_GRAPH_GUID and not graph_id:
            raise ValueError(GRAPH_REQUIRED_ERROR)

        tenant = client.tenant_guid if cls.REQUIRE_TENANT else None
        url = (
            _get_url_v1(cls, tenant, graph_id, "bulk")
            if graph_id and cls.REQUIRE_GRAPH_GUID
            else _get_url_v1(cls, tenant, "bulk")
        )

        client.request(
            "DELETE",
            url,
            json=guid,
            headers=JSON_CONTENT_TYPE,
        )


class DeleteAllAPIResource:
    """
    A mixin class for deleting all resources of a given type.
    This class implements a generic delete pattern for resources for a specific resource.
    """

    RESOURCE_NAME: str = ""
    REQUIRE_GRAPH_GUID: bool = True
    REQUIRE_TENANT: bool = True

    @classmethod
    def delete_all(cls) -> None:
        """
        Delete all resources of a given type.
        """
        client = get_client()
        if cls.REQUIRE_TENANT and client.tenant_guid is None:
            raise ValueError(TENANT_REQUIRED_ERROR)
        graph_id = client.graph_guid if cls.REQUIRE_GRAPH_GUID else None
        graph_id = str(uuid.UUID(str(graph_id))).lower()

        if cls.REQUIRE_GRAPH_GUID and not graph_id:
            raise ValueError(GRAPH_REQUIRED_ERROR)
        tenant = client.tenant_guid if cls.REQUIRE_TENANT else None
        url = (
            _get_url_v1(cls, tenant, graph_id, "all")
            if graph_id and cls.REQUIRE_GRAPH_GUID
            else _get_url_v1(cls, tenant, "all")
        )

        client.request("DELETE", url, headers=JSON_CONTENT_TYPE)


class AllRetrievableAPIResource:
    """
    A mixin class for retrieving all resources of a given type.
    This class implements a generic retrieval pattern for resources using Pydantic models(for data validation and deserialization).
    """

    RESOURCE_NAME: str = ""
    MODEL: Optional[Optional[Type[BaseModel]]] = None
    REQUIRE_GRAPH_GUID: bool = True
    REQUIRE_TENANT: bool = True

    @classmethod
    def retrieve_all(cls, **kwargs) -> list["BaseModel"]:
        """
        Retrieve all instances of the resource.
        """
        client = get_client()
        if cls.REQUIRE_TENANT and client.tenant_guid is None:
            raise ValueError(TENANT_REQUIRED_ERROR)

        # Extract graph_guid from kwargs if provided, otherwise use client.graph_guid
        graph_id = kwargs.pop("graph_guid", None) or client.graph_guid

        if cls.REQUIRE_GRAPH_GUID and not graph_id:
            raise ValueError(GRAPH_REQUIRED_ERROR)
        tenant = client.tenant_guid if cls.REQUIRE_TENANT else None
        include = {}
        if kwargs.get("include_data"):
            include["incldata"] = None
        if kwargs.get("include_subordinates"):
            include["inclsub"] = None

        url = (
            _get_url_v1(cls, tenant, graph_id, **include)
            if graph_id and cls.REQUIRE_GRAPH_GUID
            else _get_url_v1(cls, tenant, **include)
        )
        instances = client.request("GET", url)

        return (
            [cls.MODEL.model_validate(instance) for instance in instances]
            if cls.MODEL
            else instances
        )


class SearchableAPIResource:
    """
    Provides a search method to search for resources based on criteria.
    This class implements a flexible search pattern against resources
    using request/response models for validation and serialization.
    """

    RESOURCE_NAME: str = ""
    SEARCH_MODELS: Optional[
        tuple[Optional[type[BaseModel]], Optional[type[BaseModel]]]
    ] = None
    REQUIRE_TENANT: bool = True

    @classmethod
    def search(cls, graph_id: str | None = None, **data) -> BaseModel:
        """
        Search for resources based on the provided criteria.
        """
        client = get_client()
        if cls.REQUIRE_TENANT and client.tenant_guid is None:
            raise ValueError(TENANT_REQUIRED_ERROR)
        tenant = client.tenant_guid if cls.REQUIRE_TENANT else None
        if data.get("include_data"):
            data["IncludeData"] = True
        if data.get("include_subordinates"):
            data["IncludeSubordinates"] = True

        url = (
            _get_url_v1(cls, tenant, graph_id, "search")
            if graph_id and cls.REQUIRE_GRAPH_GUID
            else _get_url_v1(cls, tenant, "search")
        )
        result_model = cls.SEARCH_MODELS[1]

        instance = client.request(
            "POST", url, data=json.dumps(data).encode(), headers=JSON_CONTENT_TYPE
        )
        return result_model(**instance)


class ExportGexfMixin:
    """
    Export a graph to GEXF format.
    """

    RESOURCE_NAME: str = ""
    MODEL: Optional[Type[BaseModel]] = None
    REQUIRE_TENANT: bool = True

    @classmethod
    def export_gexf(cls, graph_id: str, **params: Dict[str, Any]) -> str:
        client = get_client()
        if cls.REQUIRE_TENANT and client.tenant_guid is None:
            raise ValueError(TENANT_REQUIRED_ERROR)
        tenant = client.tenant_guid if cls.REQUIRE_TENANT else None
        url = _get_url_v1(cls, tenant, graph_id, "export", "gexf", **params)
        response = client.request("GET", url)
        try:
            return response.decode("utf-8")
        except Exception as e:
            log_error(Severity_Enum.Error.value, f"Error exporting GEXF: {response}")
            raise SdkException("Error exporting GEXF") from e


class EnumerableAPIResource:
    """Mixin class for enumerating API resources."""

    REQUIRE_TENANT: bool = True

    @classmethod
    def enumerate(cls, **kwargs) -> "EnumerationResultModel":
        """
        Enumerates resources of a given type.

        Returns:
            EnumerationResultModel: The enumeration results containing the list of resources
                and any pagination metadata.

        Raises:
            ValueError: If tenant GUID is required but not provided.
        """
        client = get_client()

        if cls.REQUIRE_TENANT and client.tenant_guid is None:
            raise ValueError("Tenant GUID is required for this resource.")
        graph_id = kwargs.pop("graph_guid", None) or client.graph_guid
        if cls.REQUIRE_GRAPH_GUID and not graph_id:
            raise ValueError(GRAPH_REQUIRED_ERROR)

        if kwargs.pop("include_data", False):
            kwargs["incldata"] = None
        if kwargs.pop("include_subordinates", False):
            kwargs["inclsub"] = None

        if cls.REQUIRE_TENANT:
            if graph_id and cls.REQUIRE_GRAPH_GUID:
                url = _get_url_v2(cls, client.tenant_guid, graph_id, **kwargs)
            else:
                url = _get_url_v2(cls, client.tenant_guid, **kwargs)
        else:
            url = _get_url_v2(cls, **kwargs)

        response = client.request("GET", url)
        return (
            EnumerationResultModel[cls.MODEL].model_validate(response)
            if cls.MODEL
            else response
        )


class EnumerableAPIResourceWithData:
    """Mixin class for enumerating API resources with data using V1 URL helper."""

    ENUMERABLE_REQUEST_MODEL: Type[BaseModel] = EnumerationQueryModel
    REQUIRE_TENANT: bool = True

    @classmethod
    def enumerate_with_query(cls, **kwargs) -> "EnumerationResultModel":
        """
        Enumerates resources of a given type with data using a query model.

        This method supports advanced querying capabilities through the ENUMERABLE_REQUEST_MODEL,
        which defaults to EnumerationQueryModel.

        Args:
            **kwargs: Query parameters that conform to the ENUMERABLE_REQUEST_MODEL schema.
                These parameters will be validated against the model before making the request.

        Returns:
            EnumerationResultModel: The enumeration results containing the list of resources
                and any pagination metadata.

        Raises:
            ValueError: If tenant GUID is required but not provided.
            ValidationError: If the provided query parameters don't match the ENUMERABLE_REQUEST_MODEL schema.
        """
        client = get_client()

        data_dict = kwargs.pop(
            "_data", kwargs.copy()
        )  # Get 'data' if provided, else use kwargs

        if cls.REQUIRE_TENANT and client.tenant_guid is None:
            raise ValueError("Tenant GUID is required for this resource.")

        # Extract graph_guid from data_dict if provided, otherwise use client.graph_guid
        graph_id = data_dict.pop("graph_guid", None) or client.graph_guid
        if cls.REQUIRE_GRAPH_GUID and not graph_id:
            raise ValueError(GRAPH_REQUIRED_ERROR)

        if data_dict.pop("include_data", False):
            data_dict["IncludeData"] = True
        if data_dict.pop("include_subordinates", False):
            data_dict["IncludeSubordinates"] = True

        if cls.REQUIRE_TENANT:
            if graph_id and cls.REQUIRE_GRAPH_GUID:
                url = _get_url_v2(cls, client.tenant_guid, graph_id, **kwargs)
            else:
                url = _get_url_v2(cls, client.tenant_guid, **kwargs)
        else:
            url = _get_url_v2(cls, **kwargs)

        data = cls.ENUMERABLE_REQUEST_MODEL(**data_dict).model_dump(
            mode="json", by_alias=True, exclude_unset=True
        )

        response = client.request("POST", url, json=data)
        return (
            EnumerationResultModel[cls.MODEL].model_validate(response)
            if cls.MODEL
            else response
        )


class RetrievableStatisticsMixin:
    """Mixin class for retrieving statistics for a given resource."""

    STATS_MODEL: Optional[Type[BaseModel]] = None

    @classmethod
    def retrieve_statistics(cls, resource_guid: str | None = None, **kwargs):
        """
        Retrieves statistics for a given resource.

        Args:
            resource_guid (str): The unique identifier of the resource.
            **kwargs: Additional keyword arguments for the request.

        Returns:
            STATS_MODEL: The statistics data for the resource, validated against STATS_MODEL if defined.

        Raises:
            ValueError: If tenant GUID is required but not provided.
        """
        client = get_client()

        if cls.REQUIRE_TENANT and client.tenant_guid is None:
            raise ValueError("Tenant GUID is required for this resource.")

        if cls.REQUIRE_TENANT:
            url = _get_url_v1(cls, client.tenant_guid, resource_guid, "stats", **kwargs)
        else:
            url = _get_url_v1(cls, resource_guid, "stats", **kwargs)

        return client.request("GET", url)


class RetrievableFirstMixin:
    """Mixin class for retrieving the first resource of a given type."""

    SEARCH_MODELS: Optional[
        tuple[Optional[type[BaseModel]], Optional[type[BaseModel]]]
    ] = None
    MODEL: Optional[Type[BaseModel]] = None
    REQUIRE_TENANT: bool = True
    REQUIRE_GRAPH_GUID: bool = True

    @classmethod
    def retrieve_first(cls, graph_id: str | None = None, **kwargs) -> "BaseModel":
        """
        Retrieves the first resource of a given type.
        """
        client = get_client()
        if cls.REQUIRE_TENANT and client.tenant_guid is None:
            raise ValueError(TENANT_REQUIRED_ERROR)
        tenant = client.tenant_guid if cls.REQUIRE_TENANT else None

        if kwargs.pop("include_data", False):
            kwargs["IncludeData"] = True
        if kwargs.pop("include_subordinates", False):
            kwargs["IncludeSubordinates"] = True

        url = (
            _get_url_v1(cls, tenant, graph_id, "first")
            if graph_id and cls.REQUIRE_GRAPH_GUID
            else _get_url_v1(cls, tenant, "first")
        )

        data = cls.SEARCH_MODELS[0](**kwargs).model_dump(
            mode="json", by_alias=True, exclude_unset=True
        )
        instance = client.request(
            "POST",
            url,
            data=json.dumps(data).encode(),
            headers=JSON_CONTENT_TYPE,
            timeout=120,
        )
        return cls.MODEL.model_validate(instance) if cls.MODEL else instance


class RetrievableManyMixin:
    """Mixin class for retrieving many resources of a given type."""

    MODEL: Optional[Type[BaseModel]] = None
    REQUIRE_TENANT: bool = True
    REQUIRE_GRAPH_GUID: bool = True

    @classmethod
    def retrieve_many(
        cls, guids: list[str], graph_guid: str | None = None
    ) -> "BaseModel":
        """
        Retrieves many resources of a given type.
        """
        client = get_client()
        if cls.REQUIRE_TENANT and client.tenant_guid is None:
            raise ValueError(TENANT_REQUIRED_ERROR)
        tenant = client.tenant_guid if cls.REQUIRE_TENANT else None
        url = (
            _get_url_v1(cls, tenant, graph_guid, guids=",".join(guids))
            if graph_guid and cls.REQUIRE_GRAPH_GUID
            else _get_url_v1(cls, tenant, guids=",".join(guids))
        )
        instance = client.request(
            "GET",
            url,
            headers=JSON_CONTENT_TYPE,
        )
        return (
            [cls.MODEL.model_validate(item) for item in instance]
            if cls.MODEL
            else instance
        )


class RetrievableAllEndpointMixin:
    """
    Mixin class for retrieving all resources using the /all endpoint.
    Provides methods for both tenant-level and graph-level retrieval.
    """

    RESOURCE_NAME: str = ""
    MODEL: Optional[Type[BaseModel]] = None
    REQUIRE_TENANT: bool = True
    REQUIRE_GRAPH_GUID: bool = True

    @classmethod
    def retrieve_all_tenant(cls, tenant_guid: str | None = None) -> list["BaseModel"]:
        """
        Retrieve all resources for a tenant using the /all endpoint.

        Endpoint:
            /v1.0/tenants/{tenant}/{resource_name}/all

        Args:
            tenant_guid: The tenant GUID. If not provided, uses client.tenant_guid.

        Returns:
            List of resource instances validated against MODEL if defined.
        """
        client = get_client()

        # Use provided tenant_guid or fall back to client.tenant_guid
        tenant_guid = tenant_guid or client.tenant_guid

        if cls.REQUIRE_TENANT and tenant_guid is None:
            raise ValueError("Tenant GUID is required for this resource.")

        # Build URL: v1.0/tenants/{tenant}/{resource_name}/all
        # Manually construct URL to avoid graph_guid being inserted when REQUIRE_GRAPH_GUID is True
        url = f"v1.0/tenants/{tenant_guid}/{cls.RESOURCE_NAME}/all"

        instance = client.request("GET", url)

        return (
            [cls.MODEL.model_validate(item) for item in instance]
            if getattr(cls, "MODEL", None)
            else instance
        )

    @classmethod
    def retrieve_all_graph(
        cls, tenant_guid: str | None = None, graph_guid: str | None = None
    ) -> list["BaseModel"]:
        """
        Retrieve all resources for a graph using the /all endpoint.

        Endpoint:
            /v1.0/tenants/{tenant}/graphs/{graph}/{resource_name}/all

        Args:
            tenant_guid: The tenant GUID. If not provided, uses client.tenant_guid.
            graph_guid: The graph GUID. If not provided, uses client.graph_guid.

        Returns:
            List of resource instances validated against MODEL if defined.
        """
        client = get_client()

        # Use provided values or fall back to client values
        tenant_guid = tenant_guid or client.tenant_guid
        graph_guid = graph_guid or client.graph_guid

        if cls.REQUIRE_TENANT and tenant_guid is None:
            raise ValueError(TENANT_REQUIRED_ERROR)
        if cls.REQUIRE_GRAPH_GUID and not graph_guid:
            raise ValueError(GRAPH_REQUIRED_ERROR)

        # Build URL based on REQUIRE_GRAPH_GUID setting
        if cls.REQUIRE_GRAPH_GUID:
            # Use _get_url_v1 when REQUIRE_GRAPH_GUID is True
            url = _get_url_v1(cls, tenant_guid, graph_guid, "all")
        else:
            # Manually construct URL when REQUIRE_GRAPH_GUID is False
            # (can't use _get_url_v1 as it would place graph after resource name)
            url = f"v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/{cls.RESOURCE_NAME}/all"

        instance = client.request("GET", url)

        return (
            [cls.MODEL.model_validate(item) for item in instance]
            if getattr(cls, "MODEL", None)
            else instance
        )

    @classmethod
    def retrieve_for_graph(
        cls,
        tenant_guid: str | None = None,
        graph_guid: str | None = None,
        include_data: bool = False,
        include_subordinates: bool = False,
    ) -> list["BaseModel"]:
        """
        Retrieve resources for a specific graph.

        Endpoint:
            /v1.0/tenants/{tenant}/graphs/{graph}/{resource_name}

        Args:
            tenant_guid: The tenant GUID. If not provided, uses client.tenant_guid.
            graph_guid: The graph GUID. If not provided, uses client.graph_guid.
            include_data: Whether to include data in the response.
            include_subordinates: Whether to include subordinates in the response.

        Returns:
            List of resource instances validated against MODEL if defined.
        """
        client = get_client()

        # Use provided values or fall back to client values
        tenant_guid = tenant_guid or client.tenant_guid
        graph_guid = graph_guid or client.graph_guid

        if cls.REQUIRE_TENANT and tenant_guid is None:
            raise ValueError(TENANT_REQUIRED_ERROR)
        if not graph_guid:
            raise ValueError(GRAPH_REQUIRED_ERROR)

        # Build URL: v1.0/tenants/{tenant}/graphs/{graph}/{resource_name}
        # Use a temporary class with REQUIRE_GRAPH_GUID=True to get correct URL structure
        class _TempGraphClass:
            RESOURCE_NAME = cls.RESOURCE_NAME
            REQUIRE_TENANT = cls.REQUIRE_TENANT
            REQUIRE_GRAPH_GUID = True

        include = {}
        if include_data:
            include["incldata"] = None
        if include_subordinates:
            include["inclsub"] = None

        url = _get_url_v1(_TempGraphClass, tenant_guid, graph_guid, **include)

        instance = client.request("GET", url)

        return (
            [cls.MODEL.model_validate(item) for item in instance]
            if getattr(cls, "MODEL", None)
            else instance
        )


class DeletableAllEndpointMixin:
    """
    Mixin class for deleting all resources using the /all endpoint.
    Provides methods for both tenant-level and graph-level deletion.
    """

    RESOURCE_NAME: str = ""
    REQUIRE_TENANT: bool = True
    REQUIRE_GRAPH_GUID: bool = True

    @classmethod
    def delete_all_tenant(cls, tenant_guid: str | None = None) -> None:
        """
        Delete all resources for a tenant using the /all endpoint.

        Endpoint:
            /v1.0/tenants/{tenant}/{resource_name}/all

        Args:
            tenant_guid: The tenant GUID.
        """
        client = get_client()

        # Build URL: v1.0/tenants/{tenant}/{resource_name}/all
        # Manually construct URL to avoid graph_guid being inserted when REQUIRE_GRAPH_GUID is True
        tenant_guid = tenant_guid or client.tenant_guid
        if cls.REQUIRE_TENANT and tenant_guid is None:
            raise ValueError("Tenant GUID is required for this resource.")
        url = f"v1.0/tenants/{tenant_guid}/{cls.RESOURCE_NAME}/all"

        client.request("DELETE", url, headers=JSON_CONTENT_TYPE)

    @classmethod
    def delete_all_graph(
        cls, tenant_guid: str | None = None, graph_guid: str | None = None
    ) -> None:
        """
        Delete all resources for a graph using the /all endpoint.

        Endpoint:
            /v1.0/tenants/{tenant}/graphs/{graph}/{resource_name}/all

        Args:
            tenant_guid: The tenant GUID. If not provided, uses client.tenant_guid.
            graph_guid: The graph GUID. If not provided, uses client.graph_guid.
        """
        client = get_client()

        # Use provided values or fall back to client values
        tenant_guid = tenant_guid or client.tenant_guid
        graph_guid = graph_guid or client.graph_guid

        if cls.REQUIRE_TENANT and tenant_guid is None:
            raise ValueError(TENANT_REQUIRED_ERROR)
        if cls.REQUIRE_GRAPH_GUID and not graph_guid:
            raise ValueError(GRAPH_REQUIRED_ERROR)

        # Build URL based on REQUIRE_GRAPH_GUID setting
        if cls.REQUIRE_GRAPH_GUID:
            # Use _get_url_v1 when REQUIRE_GRAPH_GUID is True
            url = _get_url_v1(cls, tenant_guid, graph_guid, "all")
        else:
            # Manually construct URL when REQUIRE_GRAPH_GUID is False
            # (can't use _get_url_v1 as it would place graph after resource name)
            url = f"v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/{cls.RESOURCE_NAME}/all"

        client.request("DELETE", url, headers=JSON_CONTENT_TYPE)

    @classmethod
    def delete_for_graph(
        cls,
        tenant_guid: str | None = None,
        graph_guid: str | None = None,
    ) -> None:
        """
        Delete resources for a specific graph.

        Endpoint:
            /v1.0/tenants/{tenant}/graphs/{graph}/{resource_name}

        Args:
            tenant_guid: The tenant GUID. If not provided, uses client.tenant_guid.
            graph_guid: The graph GUID. If not provided, uses client.graph_guid.
        """
        client = get_client()

        # Use provided values or fall back to client values
        tenant_guid = tenant_guid or client.tenant_guid
        graph_guid = graph_guid or client.graph_guid

        if cls.REQUIRE_TENANT and tenant_guid is None:
            raise ValueError(TENANT_REQUIRED_ERROR)
        if not graph_guid:
            raise ValueError(GRAPH_REQUIRED_ERROR)

        # Build URL: v1.0/tenants/{tenant}/graphs/{graph}/{resource_name}
        # Use a temporary class with REQUIRE_GRAPH_GUID=True to get correct URL structure
        class _TempGraphClass:
            RESOURCE_NAME = cls.RESOURCE_NAME
            REQUIRE_TENANT = cls.REQUIRE_TENANT
            REQUIRE_GRAPH_GUID = True

        url = _get_url_v1(_TempGraphClass, tenant_guid, graph_guid)

        client.request("DELETE", url, headers=JSON_CONTENT_TYPE)


class RetrievableNodeResourceMixin:
    """
    Mixin class for retrieving resources associated with a specific node.
    Provides method for retrieving node-specific resources.

    Endpoint pattern:
        /v1.0/tenants/{tenant}/graphs/{graph}/nodes/{node}/{resource_name}
    """

    RESOURCE_NAME: str = ""
    MODEL: Optional[Type[BaseModel]] = None
    REQUIRE_TENANT: bool = True
    REQUIRE_GRAPH_GUID: bool = True

    @classmethod
    def retrieve_for_node(
        cls,
        node_guid: str,
        tenant_guid: str | None = None,
        graph_guid: str | None = None,
    ) -> list["BaseModel"]:
        """
        Retrieve resources for a specific node.

        Endpoint:
            /v1.0/tenants/{tenant}/graphs/{graph}/nodes/{node}/{resource_name}

        Args:
            node_guid: The node GUID.
            tenant_guid: The tenant GUID. If not provided, uses client.tenant_guid.
            graph_guid: The graph GUID. If not provided, uses client.graph_guid.

        Returns:
            List of resource instances validated against MODEL if defined.
        """
        client = get_client()

        # Use provided values or fall back to client values
        tenant_guid = tenant_guid or client.tenant_guid
        graph_guid = graph_guid or client.graph_guid

        if cls.REQUIRE_TENANT and tenant_guid is None:
            raise ValueError(TENANT_REQUIRED_ERROR)
        if cls.REQUIRE_GRAPH_GUID and not graph_guid:
            raise ValueError(GRAPH_REQUIRED_ERROR)

        # Build URL: v1.0/tenants/{tenant}/graphs/{graph}/nodes/{node}/{resource_name}
        # Use _get_url_base with a temporary class that has RESOURCE_NAME = "nodes"
        # to build the tenant/graph/nodes part, then append the actual resource name
        # Note: REQUIRE_GRAPH_GUID must be True to include graphs/{graph} in the path
        class _TempNodeClass:
            RESOURCE_NAME = "nodes"
            REQUIRE_TENANT = cls.REQUIRE_TENANT
            REQUIRE_GRAPH_GUID = (
                True  # Always True for node endpoints (they require graph)
            )

        # Build base path: tenants/{tenant}/graphs/{graph}/nodes/{node}
        base_path = _get_url_base(_TempNodeClass, tenant_guid, graph_guid, node_guid)
        # Append the actual resource name
        url = f"v1.0/{base_path}/{cls.RESOURCE_NAME}"

        instance = client.request("GET", url)

        return (
            [cls.MODEL.model_validate(item) for item in instance]
            if getattr(cls, "MODEL", None)
            else instance
        )


class RetrievableEdgeResourceMixin:
    """
    Mixin class for retrieving resources associated with a specific edge.
    Provides method for retrieving edge-specific resources.

    Endpoint pattern:
        /v1.0/tenants/{tenant}/graphs/{graph}/edges/{edge}/{resource_name}
    """

    RESOURCE_NAME: str = ""
    MODEL: Optional[Type[BaseModel]] = None
    REQUIRE_TENANT: bool = True
    REQUIRE_GRAPH_GUID: bool = True

    @classmethod
    def retrieve_for_edge(
        cls,
        edge_guid: str,
        tenant_guid: str | None = None,
        graph_guid: str | None = None,
    ) -> list["BaseModel"]:
        """
        Retrieve resources for a specific edge.

        Endpoint:
            /v1.0/tenants/{tenant}/graphs/{graph}/edges/{edge}/{resource_name}

        Args:
            edge_guid: The edge GUID.
            tenant_guid: The tenant GUID. If not provided, uses client.tenant_guid.
            graph_guid: The graph GUID. If not provided, uses client.graph_guid.

        Returns:
            List of resource instances validated against MODEL if defined.
        """
        client = get_client()

        # Use provided values or fall back to client values
        tenant_guid = tenant_guid or client.tenant_guid
        graph_guid = graph_guid or client.graph_guid

        if cls.REQUIRE_TENANT and tenant_guid is None:
            raise ValueError(TENANT_REQUIRED_ERROR)
        if cls.REQUIRE_GRAPH_GUID and not graph_guid:
            raise ValueError(GRAPH_REQUIRED_ERROR)

        # Build URL: v1.0/tenants/{tenant}/graphs/{graph}/edges/{edge}/{resource_name}
        # Use _get_url_base with a temporary class that has RESOURCE_NAME = "edges"
        # to build the tenant/graph/edges part, then append the actual resource name
        # Note: REQUIRE_GRAPH_GUID must be True to include graphs/{graph} in the path
        class _TempEdgeClass:
            RESOURCE_NAME = "edges"
            REQUIRE_TENANT = cls.REQUIRE_TENANT
            REQUIRE_GRAPH_GUID = (
                True  # Always True for edge endpoints (they require graph)
            )

        # Build base path: tenants/{tenant}/graphs/{graph}/edges/{edge}
        base_path = _get_url_base(_TempEdgeClass, tenant_guid, graph_guid, edge_guid)
        # Append the actual resource name
        url = f"v1.0/{base_path}/{cls.RESOURCE_NAME}"

        instance = client.request("GET", url)

        return (
            [cls.MODEL.model_validate(item) for item in instance]
            if getattr(cls, "MODEL", None)
            else instance
        )


class DeletableGraphResourceMixin:
    """
    Mixin class for deleting resources at the graph level.
    Provides method for deleting graph-specific resources.

    Endpoint pattern:
        /v1.0/tenants/{tenant}/graphs/{graph}/{resource_name}
    """

    RESOURCE_NAME: str = ""
    REQUIRE_TENANT: bool = True
    REQUIRE_GRAPH_GUID: bool = True

    @classmethod
    def delete_for_graph(
        cls, tenant_guid: str | None = None, graph_guid: str | None = None
    ) -> None:
        """
        Delete resources for a specific graph.

        Endpoint:
            /v1.0/tenants/{tenant}/graphs/{graph}/{resource_name}

        Args:
            tenant_guid: The tenant GUID. If not provided, uses client.tenant_guid.
            graph_guid: The graph GUID. If not provided, uses client.graph_guid.
        """
        client = get_client()

        # Use provided values or fall back to client values
        tenant_guid = tenant_guid or client.tenant_guid
        graph_guid = graph_guid or client.graph_guid

        if cls.REQUIRE_TENANT and tenant_guid is None:
            raise ValueError(TENANT_REQUIRED_ERROR)
        if cls.REQUIRE_GRAPH_GUID and not graph_guid:
            raise ValueError(GRAPH_REQUIRED_ERROR)

        # Build URL: v1.0/tenants/{tenant}/graphs/{graph}/{resource_name}
        # Manually construct URL to ensure correct path structure
        url = f"v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/{cls.RESOURCE_NAME}"

        client.request("DELETE", url, headers=JSON_CONTENT_TYPE)


class DeletableNodeResourceMixin:
    """
    Mixin class for deleting resources associated with a specific node.
    Provides method for deleting node-specific resources.

    Endpoint pattern:
        /v1.0/tenants/{tenant}/graphs/{graph}/nodes/{node}/{resource_name}
    """

    RESOURCE_NAME: str = ""
    REQUIRE_TENANT: bool = True
    REQUIRE_GRAPH_GUID: bool = True

    @classmethod
    def delete_for_node(
        cls,
        node_guid: str,
        tenant_guid: str | None = None,
        graph_guid: str | None = None,
    ) -> None:
        """
        Delete resources for a specific node.

        Endpoint:
            /v1.0/tenants/{tenant}/graphs/{graph}/nodes/{node}/{resource_name}

        Args:
            node_guid: The node GUID.
            tenant_guid: The tenant GUID. If not provided, uses client.tenant_guid.
            graph_guid: The graph GUID. If not provided, uses client.graph_guid.
        """
        client = get_client()

        # Use provided values or fall back to client values
        tenant_guid = tenant_guid or client.tenant_guid
        graph_guid = graph_guid or client.graph_guid

        if cls.REQUIRE_TENANT and tenant_guid is None:
            raise ValueError(TENANT_REQUIRED_ERROR)
        if cls.REQUIRE_GRAPH_GUID and not graph_guid:
            raise ValueError(GRAPH_REQUIRED_ERROR)

        # Build URL: v1.0/tenants/{tenant}/graphs/{graph}/nodes/{node}/{resource_name}
        # Use _get_url_base with a temporary class that has RESOURCE_NAME = "nodes"
        # to build the tenant/graph/nodes part, then append the actual resource name
        # Note: REQUIRE_GRAPH_GUID must be True to include graphs/{graph} in the path
        class _TempNodeClass:
            RESOURCE_NAME = "nodes"
            REQUIRE_TENANT = cls.REQUIRE_TENANT
            REQUIRE_GRAPH_GUID = (
                True  # Always True for node endpoints (they require graph)
            )

        # Build base path: tenants/{tenant}/graphs/{graph}/nodes/{node}
        base_path = _get_url_base(_TempNodeClass, tenant_guid, graph_guid, node_guid)
        # Append the actual resource name
        url = f"v1.0/{base_path}/{cls.RESOURCE_NAME}"

        client.request("DELETE", url, headers=JSON_CONTENT_TYPE)


class DeletableEdgeResourceMixin:
    """
    Mixin class for deleting resources associated with a specific edge.
    Provides method for deleting edge-specific resources.

    Endpoint pattern:
        /v1.0/tenants/{tenant}/graphs/{graph}/edges/{edge}/{resource_name}
    """

    RESOURCE_NAME: str = ""
    REQUIRE_TENANT: bool = True
    REQUIRE_GRAPH_GUID: bool = True

    @classmethod
    def delete_for_edge(
        cls,
        edge_guid: str,
        tenant_guid: str | None = None,
        graph_guid: str | None = None,
    ) -> None:
        """
        Delete resources for a specific edge.

        Endpoint:
            /v1.0/tenants/{tenant}/graphs/{graph}/edges/{edge}/{resource_name}

        Args:
            edge_guid: The edge GUID.
            tenant_guid: The tenant GUID. If not provided, uses client.tenant_guid.
            graph_guid: The graph GUID. If not provided, uses client.graph_guid.
        """
        client = get_client()

        # Use provided values or fall back to client values
        tenant_guid = tenant_guid or client.tenant_guid
        graph_guid = graph_guid or client.graph_guid

        if cls.REQUIRE_TENANT and tenant_guid is None:
            raise ValueError(TENANT_REQUIRED_ERROR)
        if cls.REQUIRE_GRAPH_GUID and not graph_guid:
            raise ValueError(GRAPH_REQUIRED_ERROR)

        # Build URL: v1.0/tenants/{tenant}/graphs/{graph}/edges/{edge}/{resource_name}
        # Use _get_url_base with a temporary class that has RESOURCE_NAME = "edges"
        # to build the tenant/graph/edges part, then append the actual resource name
        # Note: REQUIRE_GRAPH_GUID must be True to include graphs/{graph} in the path
        class _TempEdgeClass:
            RESOURCE_NAME = "edges"
            REQUIRE_TENANT = cls.REQUIRE_TENANT
            REQUIRE_GRAPH_GUID = (
                True  # Always True for edge endpoints (they require graph)
            )

        # Build base path: tenants/{tenant}/graphs/{graph}/edges/{edge}
        base_path = _get_url_base(_TempEdgeClass, tenant_guid, graph_guid, edge_guid)
        # Append the actual resource name
        url = f"v1.0/{base_path}/{cls.RESOURCE_NAME}"

        client.request("DELETE", url, headers=JSON_CONTENT_TYPE)
