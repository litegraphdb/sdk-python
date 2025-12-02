import litegraph

sdk = litegraph.configure(
    endpoint="http://YOUR_SERVER_URL_HERE:PORT",
    tenant_guid="00000000-0000-0000-0000-000000000000",
    graph_guid="00000000-0000-0000-0000-000000000000",
    access_key="litegraphadmin",
)


def create_label():
    label = litegraph.Label.create(
        graph_guid="00000000-0000-0000-0000-000000000000", label="Test Label"
    )
    print(label)


# create_label()


def retrieve_label():
    label = litegraph.Label.retrieve(guid="00000000-0000-0000-0000-000000000000")
    print(label)


# retrieve_label()


def retrieve_all_label():
    labels = litegraph.Label.retrieve_all()
    print(labels)


# retrieve_all_label()


def retrieve_multiple_label():
    labels = litegraph.Label.retrieve_many(
        guids=[
            "00000000-0000-0000-0000-000000000000",
            "d559b6e5-c6d0-4897-a9d7-4a199fb887da",
        ]
    )
    print(labels)


# retrieve_multiple_label()


def enumerate_label():
    labels = litegraph.Label.enumerate()
    print(labels)


# enumerate_label()


def enumerate_with_query_label():
    labels = litegraph.Label.enumerate_with_query(
        ordering="CreatedDescending",
        MaxResults=10,
        Skip=0,
        IncludeData=True,
        IncludeSubordinates=True,
        Expr=litegraph.ExprModel(Left="Name", Operator="Equals", Right="Test"),
    )
    print(labels)


# enumerate_with_query_label()


def update_label():
    label = litegraph.Label.update(
        guid="00000000-0000-0000-0000-000000000000", label="Updated Label"
    )
    print(label)


# update_label()


def delete_label():
    litegraph.Label.delete(guid="17a71ef7-c9c3-45f1-941d-c376f45f094a")
    print("Label deleted")


# delete_label()


def create_multiple_label():
    labels = litegraph.Label.create_multiple(
        [
            {
                "Label": "Test Label 1",
                "GraphGUID": "00000000-0000-0000-0000-000000000000",
            },
            {
                "Label": "Test Label 2",
                "GraphGUID": "00000000-0000-0000-0000-000000000000",
            },
        ]
    )
    print(labels)


# create_multiple_label()


def exists_label():
    exists = litegraph.Label.exists(guid="00000000-0000-0000-0000-000000000000")
    print(exists)


# exists_label()


def get_all_tenant_labels():
    labels = litegraph.Label.retrieve_all_tenant_labels(
        tenant_guid="00000000-0000-0000-0000-000000000000"
    )
    print(labels)


# get_all_tenant_labels()


def get_all_graph_labels():
    labels = litegraph.Label.retrieve_all_graph_labels(
        tenant_guid="00000000-0000-0000-0000-000000000000",
        graph_guid="00000000-0000-0000-0000-000000000000",
    )
    print(labels)


# get_all_graph_labels()


def get_node_labels():
    labels = litegraph.Label.retrieve_node_labels(
        tenant_guid="00000000-0000-0000-0000-000000000000",
        graph_guid="00000000-0000-0000-0000-000000000000",
        node_guid="bd74d996-4a2d-48e0-9e93-110d19dd7fb2",
    )
    print(labels)


# get_node_labels()


def get_edge_labels():
    labels = litegraph.Label.retrieve_edge_labels(
        tenant_guid="00000000-0000-0000-0000-000000000000",
        graph_guid="00000000-0000-0000-0000-000000000000",
        edge_guid="4015a4e1-b744-4727-ab7e-cd0fbc7fd8b8",
    )
    print(labels)


# get_edge_labels()


def delete_all_tenant_labels():
    litegraph.Label.delete_all_tenant_labels(
        tenant_guid="00000000-0000-0000-0000-000000000000"
    )
    print("All tenant labels deleted")


delete_all_tenant_labels()


def delete_all_graph_labels():
    litegraph.Label.delete_all_graph_labels(
        tenant_guid="00000000-0000-0000-0000-000000000000",
        graph_guid="00000000-0000-0000-0000-000000000000",
    )
    print("All graph labels deleted")


delete_all_graph_labels()


def delete_graph_labels():
    litegraph.Label.delete_graph_labels(
        tenant_guid="00000000-0000-0000-0000-000000000000",
        graph_guid="00000000-0000-0000-0000-000000000000",
    )
    print("Graph labels deleted")


delete_graph_labels()


def delete_node_labels():
    litegraph.Label.delete_node_labels(
        tenant_guid="00000000-0000-0000-0000-000000000000",
        graph_guid="00000000-0000-0000-0000-000000000000",
        node_guid="17155e85-9c9d-481e-a4e2-14d386fbe225",
    )
    print("Node labels deleted")


# delete_node_labels()


def delete_edge_labels():
    litegraph.Label.delete_edge_labels(
        tenant_guid="00000000-0000-0000-0000-000000000000",
        graph_guid="00000000-0000-0000-0000-000000000000",
        edge_guid="dbafd244-bd7d-4668-bf1d-ca773d93058b",
    )
    print("Edge labels deleted")


# delete_edge_labels()


def get_graph_labels():
    labels = litegraph.Label.retrieve_graph_labels()
    print(labels)


# get_graph_labels()
