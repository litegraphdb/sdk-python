import litegraph

sdk = litegraph.configure(
    endpoint="http://192.168.101.63:8701",
    tenant_guid="00000000-0000-0000-0000-000000000000",
    access_key="litegraphadmin",
)

def create_tenant():
    tenant = litegraph.Tenant.create(name="Test Tenant")
    print(tenant)

# create_tenant()

def retrieve_tenant():
    tenant = litegraph.Tenant.retrieve(guid="00000000-0000-0000-0000-000000000000")
    print(tenant)

# retrieve_tenant()

def update_tenant():
    tenant = litegraph.Tenant.update(guid="00000000-0000-0000-0000-000000000000", name="Updated Tenant")
    print(tenant)

# update_tenant()

def enumerate_tenant():
    tenants = litegraph.Tenant.enumerate()
    print(tenants)

#enumerate_tenant()

def enumerate_with_query_tenant():
    tenants = litegraph.Tenant.enumerate_with_query(ordering="CreatedDescending",MaxResults=10,Skip=0,IncludeData=True,IncludeSubordinates=True,Expr=litegraph.ExprModel(Left="Name",Operator="Equals",Right="Test"))
    print(tenants)

# enumerate_with_query_tenant()

def retrieve_statistics_single_tenant():
    statistics = litegraph.Tenant.retrieve_statistics(tenant_guid="00000000-0000-0000-0000-000000000000")
    print(statistics)

# retrieve_statistics_single_tenant()

def retrieve_statistics_all_tenant():
    statistics = litegraph.Tenant.retrieve_statistics()
    print(statistics)

# retrieve_statistics_all_tenant()

def delete_tenant():
    litegraph.Tenant.delete(guid="23bc2e88-0a3e-4373-ba72-ca523bed18d6")
    print("Tenant deleted")

# delete_tenant()

def delete_tenant_force():
    litegraph.Tenant.delete(guid="347f7a9b-0b97-48c5-a420-019a9c07c336", force=True)
    print("Tenant deleted")

# delete_tenant_force()

def tenant_exists():
    exists = litegraph.Tenant.exists(guid="00000000-0000-0000-0000-000000000000")
    print(exists)

# tenant_exists()

def retrieve_multiple_tenants():
    tenants = litegraph.Tenant.retrieve_many(["00000000-0000-0000-0000-000000000000","00000000-0000-0000-0000-000000000001"])
    print(tenants)

# retrieve_multiple_tenants()

def retrieve_all_tenants():
    tenants = litegraph.Tenant.retrieve_all()
    print(tenants)

retrieve_all_tenants()

