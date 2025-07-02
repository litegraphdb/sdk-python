from pprint import pprint

import litegraph

litegraph.configure(
    endpoint="http://localhost:8701",
    tenant_guid="00000000-0000-0000-0000-000000000000",
    graph_guid="00000000-0000-0000-0000-000000000000",
    access_key="litegraphadmin",
)

# Check if tenant exists
exists = litegraph.Tenant.exists(guid="00000000-0000-0000-0000-000000000000")
print(f"Tenant exists: {exists}")

# Enumerate tenants
tenants = litegraph.Tenant.enumerate_with_query(
    expr=litegraph.ExprModel(Left="Name", Operator="Equals", Right="Test")
)
print(f"Tenants: {tenants}")

# Retrieve statistics for a tenant
statistics = litegraph.Tenant.retrieve_statistics(
    tenant_guid="00000000-0000-0000-0000-000000000000"
)
print(f"Statistics: {statistics}")

statistics = litegraph.Tenant.retrieve_statistics()
print(f"Statistics: {statistics}")

# Retrieve statistics for a graph
statistics = litegraph.Graph.retrieve_statistics(
    graph_guid="00000000-0000-0000-0000-000000000000"
)
print(f"Statistics: {statistics}")

statistics = litegraph.Graph.retrieve_statistics()
print(f"Statistics: {statistics}")

# Create a new credential
new_tenant = litegraph.Credential.create(
    **{
        "UserGUID": "00000000-0000-0000-0000-000000000000",
        "Name": "New credential",
        "BearerToken": "foobar",
        "Active": True,
    }
)
print(f"Created tenant: {new_tenant}")

# Update a credential
updated_tenant = litegraph.Credential.update(
    guid="cea747d4-9af5-4d79-917f-351a88f1c738",
    **{
        "UserGUID": "00000000-0000-0000-0000-000000000000",
        "Name": "Updated credential",
        "BearerToken": "default",
        "Active": True,
    },
)
print(f"Updated tenant: {updated_tenant}")

# Retrieve a specific credential
tenant = litegraph.User.retrieve(guid="00000000-0000-0000-0000-000000000000")
print(f"Retrieved tenant: {tenant}")
# Delete a credential
litegraph.Credential.delete(guid="1deacf52-c1ea-4866-a78b-ed5a46828930")
print("Tenant deleted")

# Search
all_tenants = litegraph.Graph.search(
    graph_guid="00000000-0000-0000-0000-000000000000",
    **{
        "Ordering": "CreatedDescending",
        "Labels": ["updated", "test"],
        "Tags": {"type": "graph"},
    },
)
print(f"All tenants: {all_tenants}")

# Vector search
vectors = litegraph.Vector.retrieve_all()
print(f"Vectors: {vectors}")

# Create a new vector
new_vector = litegraph.Vector.create(
    tenant_guid="00000000-0000-0000-0000-000000000000",
    graph_guid="00000000-0000-0000-0000-000000000000",
    vector=[0.1, 0.2, 0.3],
)
print(f"New vector: {new_vector}")

# Update a vector
updated_vector = litegraph.Vector.update(
    guid="00000000-0000-0000-0000-000000000000",
    vector=[0.1, 0.2, 0.3],
)
print(f"Updated vector: {updated_vector}")

# Delete a vector
litegraph.Vector.delete(guid="00000000-0000-0000-0000-000000000000")
print("Vector deleted")


# Search vectors
vectors = litegraph.Vector.search_vectors(
    domain="Graph",
    embeddings=[0.1, 0.2, 0.3],
    tenant_guid="00000000-0000-0000-0000-000000000000",
    graph_guid="00000000-0000-0000-0000-000000000000",
)
pprint(f"Vectors: {vectors}")

# Authentication
token = litegraph.Authentication.generate_authentication_token(
    email="default@user.com",
    password="password",
    tenant_guid="00000000-0000-0000-0000-000000000000",
)
print(f"Token: {token}")

# Retrieve token details
token_details = litegraph.Authentication.retrieve_token_details(
    token=token.token,
)
print(f"Token details: {token_details}")

# Retrieve tenants for email
tenants = litegraph.Authentication.retrieve_tenants_for_email(
    email="default@user.com",
)
print(f"Tenants: {tenants}")

graph = litegraph.Graph.retrieve_first()
pprint(f"Graph: {graph}")

node = litegraph.Node.retrieve_first(graph_guid="00000000-0000-0000-0000-000000000000")
pprint(f"Node: {node}")

edge = litegraph.Edge.retrieve_first(graph_guid="00000000-0000-0000-0000-000000000000")
pprint(f"Edge: {edge}")

nodes = litegraph.Node.retrieve_many(
    guids=["00000000-0000-0000-0000-000000000000", "00000000-0000-0000-0000-000000000001"],
    graph_guid="00000000-0000-0000-0000-000000000000"
)
pprint(f"Nodes: {nodes}")