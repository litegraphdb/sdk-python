import litegraph

sdk = litegraph.configure(
    endpoint="http://YOUR_SERVER_URL_HERE:PORT",
    tenant_guid="00000000-0000-0000-0000-000000000000",
    graph_guid="33773395-d573-4ea1-af25-a7d19bb37b1a",
    access_key="litegraphadmin",
)

def batch_existence():
    batch_existence = litegraph.Graph.batch_existence(graph_guid="33773395-d573-4ea1-af25-a7d19bb37b1a",request=litegraph.ExistenceRequestModel(nodes=["33773395-d573-4ea1-af25-a7d19bb37b1a"],edges=["33773395-d573-4ea1-af25-a7d19bb37b1a"],edges_between=[litegraph.EdgeBetweenModel(from_node_guid="33773395-d573-4ea1-af25-a7d19bb37b1a",to_node_guid="33773395-d573-4ea1-af25-a7d19bb37b1a")]))
    print(batch_existence)

batch_existence()