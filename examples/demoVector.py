import litegraph

sdk = litegraph.configure(
    endpoint="http://YOUR_SERVER_URL_HERE:PORT",
    tenant_guid="00000000-0000-0000-0000-000000000000",
    access_key="litegraphadmin",
)

def create_vector():
    vector = litegraph.Vector.create(
        vectors=[0.1, 0.2, 0.3],
        content="Test Content",
        graph_guid="00000000-0000-0000-0000-000000000000",
        dimensionality=3,
        model="all-MiniLM-L6-v2"
    )
    print(vector)

create_vector()

def exists_vector():
    exists = litegraph.Vector.exists(guid="00000000-0000-0000-0000-000000000000")
    print(exists)

# exists_vector()

def retrieve_vector():
    vector = litegraph.Vector.retrieve(guid="00000000-0000-0000-0000-000000000000")
    print(vector)

# retrieve_vector()

def retrieve_all_vector():
    vectors = litegraph.Vector.retrieve_all()
    print(vectors)

# retrieve_all_vector()

def retrieve_multiple_vector():
    vectors = litegraph.Vector.retrieve_many(guids=["00000000-0000-0000-0000-000000000000","00000000-0000-0000-0000-000000000000"])
    print(vectors)

# retrieve_multiple_vector()

def update_vector():
    vector = litegraph.Vector.update(
        guid="00000000-0000-0000-0000-000000000000",
        vectors=[0.1, 0.2, 0.3],
        content="Updated Content",
        graph_guid="00000000-0000-0000-0000-000000000000",
        dimensionality=3,
        model="all-MiniLM-L6-v2"
    )
    print(vector)

update_vector()

def delete_vector():
    litegraph.Vector.delete(guid="00000000-0000-0000-0000-000000000000")
    print("Vector deleted")

# delete_vector()

def enumerate_vector():
    vectors = litegraph.Vector.enumerate()
    print(vectors)

# enumerate_vector()

def enumerate_with_query_vector():
    vectors = litegraph.Vector.enumerate_with_query(
        ordering="CreatedDescending",
        MaxResults=10,
        Skip=0,
        IncludeData=True,
        IncludeSubordinates=True,
        Expr=litegraph.ExprModel(
            Left="Name",
            Operator="Equals",
            Right="Test"
        )
    )
    print(vectors)

enumerate_with_query_vector()

def create_multiple_vector():
    vectors = litegraph.Vector.create_multiple([
        {
            "graph_guid": "00000000-0000-0000-0000-000000000000",
            "node_guid": None,
            "edge_guid": None,
            "model": "all-MiniLM-L6-v2",
            "dimensionality": 384,
            "content": "Test Content",
            "vectors": [0.1, 0.2, 0.3]
        },
        {
            "graph_guid": "00000000-0000-0000-0000-000000000000",
            "node_guid": None,
            "edge_guid": None,
            "model": "all-MiniLM-L6-v2",
            "dimensionality": 384,
            "content": "Test Content 2",
            "vectors": [0.4, 0.5, 0.6]
        }
    ])
    print(vectors)

create_multiple_vector()

def delete_multiple_vector():
    litegraph.Vector.delete_multiple(["922022b6-83a7-4dc8-8e10-fcdfec3c294b","b60d5330-2bb3-4b17-9b7f-16d29660b5fb"])
    print("Vectors deleted")

#delete_multiple_vector()