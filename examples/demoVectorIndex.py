import litegraph

sdk = litegraph.configure(
    endpoint="http://192.168.101.63:8701",
    access_key="litegraphadmin",
    tenant_guid="00000000-0000-0000-0000-000000000000",
    graph_guid="00000000-0000-0000-0000-000000000000",
)

def read_config():
    config = litegraph.VectorIndex.get_config(graph_guid="00000000-0000-0000-0000-000000000000")
    print(config)

read_config()

def write_config():
    config = litegraph.VectorIndex.create_from_dict(
        graph_guid="00000000-0000-0000-0000-000000000000", 
        config_dict={
            "VectorIndexType": "HnswSqlite",
            "VectorIndexFile": "graph-00000000-0000-0000-0000-000000000000-hnsw.db",
            "VectorDimensionality": 384,
            "M": 16,
            "DefaultEf": 50,
            "EfConstruction": 200
        }
    )
    print(config)

# write_config()

def delete_config():
    litegraph.VectorIndex.delete(graph_guid="00000000-0000-0000-0000-000000000000")
    print("Vector index deleted")

# delete_config()

def get_stats():
    stats = litegraph.VectorIndex.get_stats(graph_guid="00000000-0000-0000-0000-000000000000")
    print(stats)

# get_stats()

def create_vector_index():
    vector_index = litegraph.VectorIndex.rebuild(
        graph_guid="00000000-0000-0000-0000-000000000000", 

    )
    print(vector_index)

#create_vector_index()


def delete_vector_index():
    litegraph.VectorIndex.delete(graph_guid="00000000-0000-0000-0000-000000000000")
    print("Vector index deleted")

# delete_vector_index()


def enable_vector_index():
    vector_index = litegraph.VectorIndex.enable(
        graph_guid="00000000-0000-0000-0000-000000000000", 
        config=litegraph.HnswLiteVectorIndexModel(
            VectorIndexType="HnswSqlite", 
            VectorIndexFile="graph-00000000-0000-0000-0000-000000000000-hnsw.db", 
            VectorDimensionality=384, 
            M=16, 
            DefaultEf=50, 
            EfConstruction=200
        )
    )
    print(vector_index)
    
enable_vector_index()