import litegraph

sdk = litegraph.configure(
    endpoint="http://YOUR_SERVER_URL_HERE:PORT",
    tenant_guid="00000000-0000-0000-0000-000000000000",
    graph_guid="c940d490-6693-4237-bb08-635890c03bcb",
    access_key="litegraphadmin",
)


def retrieve_all_edge():
    edges = litegraph.Edge.retrieve_all()
    print(edges)


# retrieve_all_edge()


def retrieve_edge():
    edge = litegraph.Edge.retrieve(guid="1cbb2bc5-a990-49a8-9975-e0b1c34d1011")
    print(edge)


# retrieve_edge()


def retrieve_many_edge():
    edges = litegraph.Edge.retrieve_many(
        graph_guid="1cbb2bc5-a990-49a8-9975-e0b1c34d1011",
        guids=[
            "e73bbd3f-2637-4ae3-86a0-7d09f4d76028",
            "e9e90c37-74cd-4a77-9c1f-96167e2bb3f9",
        ],
    )
    print(edges)


# retrieve_many_edge()


def enumerate_edge():
    edges = litegraph.Edge.enumerate()
    print(edges)


# enumerate_edge()


def enumerate_with_query_edge():
    edges = litegraph.Edge.enumerate_with_query(
        expr=litegraph.ExprModel(Left="Name", Operator="Equals", Right="Test")
    )
    print(edges)


enumerate_with_query_edge()


def exists_edge():
    exists = litegraph.Edge.exists(guid="e73bbd3f-2637-4ae3-86a0-7d09f4d76028")
    print(exists)


# exists_edge()


def create_edge():
    edge = litegraph.Edge.create(
        from_guid="00000000-0000-0000-0000-000000000000",
        to_guid="00000000-0000-0000-0000-000000000001",
        name="Test Edge",
        cost=1,
    )
    print(edge)


# create_edge()


def create_multiple_edge():
    edges = litegraph.Edge.create_multiple(
        [
            {
                "from_guid": "00000000-0000-0000-0000-000000000000",
                "to_guid": "00000000-0000-0000-0000-000000000001",
                "name": "Test Edge",
                "cost": 1,
            },
            {
                "from_guid": "00000000-0000-0000-0000-000000000001",
                "to_guid": "00000000-0000-0000-0000-000000000002",
                "name": "Test Edge",
                "cost": 1,
            },
        ]
    )
    print(edges)


# create_multiple_edge()


def update_edge():
    edge = litegraph.Edge.update(
        guid="e73bbd3f-2637-4ae3-86a0-7d09f4d76028", name="Test Edge Updated", cost=2
    )
    print(edge)


# update_edge()


def delete_edge():
    litegraph.Edge.delete(guid="f040fccb-8337-4666-8175-5cfcfb131189")
    print("Edge deleted")


# delete_edge()


def delete_multiple_edge():
    litegraph.Edge.delete_multiple(
        guid=[
            "c818e91d-b414-4bb6-b666-03d37790b45f",
            "d3aa9a3f-81d7-4efc-a3bb-a806e722c3b8",
        ]
    )
    print("Edges deleted")


# delete_multiple_edge()


def delete_all_edge():
    litegraph.Edge.delete_all()
    print("Edges deleted")


# delete_all_edge()


def retrieve_first_edge():
    graph = litegraph.Edge.retrieve_first(
        ordering="CreatedDescending", graph_guid="c940d490-6693-4237-bb08-635890c03bcb"
    )
    print(graph)


# retrieve_first_edge()


def get_all_graph_edges():
    edges = litegraph.Edge.retrieve_all_graph_edges(
        tenant_guid="00000000-0000-0000-0000-000000000000",
        graph_guid="00000000-0000-0000-0000-000000000000",
    )
    print(edges)


get_all_graph_edges()


def get_all_tenant_edges():
    edges = litegraph.Edge.retrieve_all_tenant_edges(
        tenant_guid="00000000-0000-0000-0000-000000000000",
    )
    print(edges)


get_all_tenant_edges()


def delete_all_tenant_edges():
    litegraph.Edge.delete_all_tenant_edges(
        tenant_guid="00000000-0000-0000-0000-000000000000",
    )
    print("Edges deleted")


# delete_all_tenant_edges()


def delete_node_edges():
    litegraph.Edge.delete_node_edges(
        tenant_guid="00000000-0000-0000-0000-000000000000",
        graph_guid="00000000-0000-0000-0000-000000000000",
        node_guid="51c6bb09-76a5-45ce-b4a4-dcc902a383d3",
    )
    print("Edges deleted")


# delete_node_edges()


def delete_node_edges_bulk():
    litegraph.Edge.delete_node_edges_bulk(
        tenant_guid="00000000-0000-0000-0000-000000000000",
        graph_guid="00000000-0000-0000-0000-000000000000",
        node_guids=[
            "51c6bb09-76a5-45ce-b4a4-dcc902a383d3",
            "51c6bb09-76a5-45ce-b4a4-dcc902a383d3",
        ],
    )
    print("Edges deleted")


# delete_node_edges_bulk()
