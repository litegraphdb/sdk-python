import litegraph

sdk = litegraph.configure(
    endpoint="http://YOUR_SERVER_URL_HERE:PORT",
    tenant_guid="00000000-0000-0000-0000-000000000000",
    access_key="litegraphadmin",
)


def create_graph():
    graph = litegraph.Graph.create(name="Test Graph")
    print(graph)


# create_graph()


def retrieve_graph():
    graph = litegraph.Graph.retrieve(guid="33773395-d573-4ea1-af25-a7d19bb37b1a")
    print(graph)


# retrieve_graph()


def retrieve_all_graph():
    graphs = litegraph.Graph.retrieve_all()
    print(graphs)


# retrieve_all_graph()


def retrieve_multiple_graph():
    graphs = litegraph.Graph.retrieve_many(
        ["ed784972-8e8d-4df7-a104-ff7e23338c80", "4072ce04-94ec-48c0-a714-79a484e891a0"]
    )
    print(graphs)


# retrieve_multiple_graph()


def update_graph():
    graph = litegraph.Graph.update(
        guid="33773395-d573-4ea1-af25-a7d19bb37b1a",
        name="Test Graph Updated",
        labels=["test"],
        tags={"Foo": "Bar"},
        data={"Key": "Value"},
        vectors=[
            {
                "Vectors": [0.1, 0.2, 0.3],
                "Content": "Test Content",
                "GraphGUID": "00000000-0000-0000-0000-000000000000",
                "Dimensionality": 3,
                "Model": "all-MiniLM-L6-v2",
            }
        ],
    )
    print(graph)


# update_graph()


def delete_graph():
    litegraph.Graph.delete(
        resource_id="33773395-d573-4ea1-af25-a7d19bb37b1a", force=True
    )
    print("Graph deleted")


# delete_graph()


def export_gexf():
    gexf = litegraph.Graph.export_gexf(graph_id="1cbb2bc5-a990-49a8-9975-e0b1c34d1011")
    print(gexf)


# export_gexf()


def retrieve_statistics():
    statistics = litegraph.Graph.retrieve_statistics(
        graph_guid="33773395-d573-4ea1-af25-a7d19bb37b1a"
    )
    print(statistics)


# retrieve_statistics()


def retrieve_statistics_all():
    statistics = litegraph.Graph.retrieve_statistics()
    print(statistics)


# retrieve_statistics_all()


def enumerate_graph():
    graphs = litegraph.Graph.enumerate()
    print(graphs)


# enumerate_graph()


def enumerate_with_query_graph():
    graphs = litegraph.Graph.enumerate_with_query(
        ordering="CreatedDescending",
        MaxResults=10,
        Skip=0,
        IncludeData=True,
        IncludeSubordinates=True,
        Expr=litegraph.ExprModel(Left="Name", Operator="Equals", Right="Test"),
    )
    print(graphs)


# enumerate_with_query_graph()


def exists_graph():
    exists = litegraph.Graph.exists(guid="33773395-d573-4ea1-af25-a7d19bb37b1a")
    print(exists)


# exists_graph()


def search_graph():
    graphs = litegraph.Graph.search(
        expr=litegraph.ExprModel(Left="Name", Operator="Equals", Right="Test")
    )
    print(graphs)


# search_graph()


def retrieve_first_graph():
    graph = litegraph.Graph.retrieve_first(ordering="CreatedDescending")
    print(graph)


# retrieve_first_graph()


def delete_graph_force():
    litegraph.Graph.delete(
        resource_id="dd198ef9-6de0-4716-bd58-008fb989480d", force=True
    )
    print("Graph deleted")


# delete_graph_force()


def retrieve_subgraph():
    subgraph = litegraph.Graph.retrieve_subgraph(
        graph_guid="b6eb533b-2f46-47e8-b732-2ec0ea09ae0a",
        node_guid="2dfef492-601d-4c72-a17c-97b9edbe6b15",
    )
    print(subgraph)


retrieve_subgraph()


def retrieve_subgraph_statistics():
    statistics = litegraph.Graph.retrieve_subgraph_statistics(
        graph_guid="b6eb533b-2f46-47e8-b732-2ec0ea09ae0a",
        node_guid="2dfef492-601d-4c72-a17c-97b9edbe6b15",
    )
    print(statistics)


retrieve_subgraph_statistics()
