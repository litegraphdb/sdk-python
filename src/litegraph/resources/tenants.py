from ..mixins import (
    AllRetrievableAPIResource,
    CreateableAPIResource,
    DeletableAPIResource,
    EnumerableAPIResource,
    EnumerableAPIResourceWithData,
    ExistsAPIResource,
    RetrievableAPIResource,
    RetrievableManyMixin,
    RetrievableStatisticsMixin,
    UpdatableAPIResource,
)
from ..models.enumeration_result import EnumerationResultModel
from ..models.tenant_metadata import TenantMetadataModel
from ..models.tenant_statistics import TenantStatisticsModel


class Tenant(
    ExistsAPIResource,
    RetrievableAPIResource,
    AllRetrievableAPIResource,
    CreateableAPIResource,
    UpdatableAPIResource,
    DeletableAPIResource,
    EnumerableAPIResource,
    EnumerableAPIResourceWithData,
    RetrievableStatisticsMixin,
    RetrievableManyMixin,
):
    RESOURCE_NAME: str = "tenants"
    MODEL = TenantMetadataModel
    STATS_MODEL = TenantStatisticsModel
    REQUIRE_TENANT = False
    REQUIRE_GRAPH_GUID = False

    @classmethod
    def delete(cls, guid: str, force: bool = False) -> None:
        """
        Delete a resource by its GUID.
        """
        kwargs = {"force": None} if force else {}
        return super().delete(guid, **kwargs)

    @classmethod
    def enumerate_with_query(cls, **kwargs) -> EnumerationResultModel:
        """
        Enumerate tenants with a query.
        """
        return super().enumerate_with_query(_data=kwargs)

    @classmethod
    def retrieve_statistics(
        cls, tenant_guid: str | None = None
    ) -> TenantStatisticsModel | dict[str, TenantStatisticsModel]:
        """
        Retrieves statistics for a given resource.
        """
        if tenant_guid:
            response = super().retrieve_statistics(tenant_guid)
            return TenantStatisticsModel.model_validate(response)
        else:
            response = super().retrieve_statistics()
            return {
                k: TenantStatisticsModel.model_validate(v) for k, v in response.items()
            }
