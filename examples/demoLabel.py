import litegraph

sdk = litegraph.configure(
    endpoint="http://YOUR_SERVER_URL_HERE:PORT",
    tenant_guid="00000000-0000-0000-0000-000000000000",
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


enumerate_with_query_label()


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


exists_label()
