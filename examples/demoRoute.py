import litegraph

sdk = litegraph.configure(
    endpoint="http://192.168.101.63:8701",
    tenant_guid="00000000-0000-0000-0000-000000000000",
    access_key="litegraphadmin",
)

def get_edges_from_node():
    edges = litegraph.RouteNodes.get_edges_from(graph_guid="1cbb2bc5-a990-49a8-9975-e0b1c34d1011",node_guid="00000000-0000-0000-0000-000000000000")
    print(edges)

# get_edges_from_node()

def get_edges_to_node():
    edges = litegraph.RouteNodes.get_edges_to(graph_guid="1cbb2bc5-a990-49a8-9975-e0b1c34d1011",node_guid="00000000-0000-0000-0000-000000000000")
    print(edges)

# get_edges_to_node()

def get_edges_between_nodes():
    edges = litegraph.RouteEdges.between(graph_guid="1cbb2bc5-a990-49a8-9975-e0b1c34d1011",from_node_guid="00000000-0000-0000-0000-000000000000",to_node_guid="00000000-0000-0000-0000-000000000001")
    print(edges)

# get_edges_between_nodes()

def get_edges_of_node():
    edges = litegraph.RouteNodes.edges(
        graph_guid="1cbb2bc5-a990-49a8-9975-e0b1c34d1011",
        node_guid="00000000-0000-0000-0000-000000000000"
    )
    print(edges)

# get_edges_of_node()

def get_parents_of_node():
    parents = litegraph.RouteNodes.parents(
        graph_guid="1cbb2bc5-a990-49a8-9975-e0b1c34d1011",
        node_guid="00000000-0000-0000-0000-000000000000"
    )
    print(parents)

# get_parents_of_node()

def get_children_of_node():
    children = litegraph.RouteNodes.children(
        graph_guid="1cbb2bc5-a990-49a8-9975-e0b1c34d1011",
        node_guid="00000000-0000-0000-0000-000000000000"
    )
    print(children)

#get_children_of_node()

def get_neighbors_of_node():
    neighbors = litegraph.RouteNodes.neighbors(
        graph_guid="1cbb2bc5-a990-49a8-9975-e0b1c34d1011",
        node_guid="00000000-0000-0000-0000-000000000000"
    )
    print(neighbors)

# get_neighbors_of_node()

def get_routes():
    routes = litegraph.Routes.routes(
        graph_guid="ac4c56d0-d9f7-40ac-9054-011780c115cc",
        from_guid="53a4dc8b-1de4-4712-b979-a8d109b09a6d",
        to_guid="d4d58959-416e-4ec5-ae26-84c04809a412"
    )
    print(routes)

get_routes()