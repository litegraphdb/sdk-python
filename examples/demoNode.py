import litegraph

sdk = litegraph.configure(
    endpoint="http://YOUR_SERVER_URL_HERE:PORT",
    tenant_guid="00000000-0000-0000-0000-000000000000",
    graph_guid="1cbb2bc5-a990-49a8-9975-e0b1c34d1011",
    access_key="litegraphadmin",
)

def retrieve_all_node():
    nodes = litegraph.Node.retrieve_all()
    print(nodes)

#retrieve_all_node()

def retrieve_node():
    node = litegraph.Node.retrieve(guid="14ffe58e-6488-4001-bada-6886bcc272ba")
    print(node)

# retrieve_node()

def retrieve_many_node():
    nodes = litegraph.Node.retrieve_many(guids=["14ffe58e-6488-4001-bada-6886bcc272ba","adfb3587-a6c7-43fb-95a7-b6fb1d2d1317"],graph_guid="1cbb2bc5-a990-49a8-9975-e0b1c34d1011")
    print(nodes)
    
# retrieve_many_node()

def enumerate_node():
    nodes = litegraph.Node.enumerate()
    print(nodes)
    
# enumerate_node()

def enumerate_with_query_node():
    nodes = litegraph.Node.enumerate_with_query(
        expr=litegraph.ExprModel(
            Left="Name",
            Operator="Equals", 
            Right="Test"
        )
    )
    print(nodes)

enumerate_with_query_node()


def exists_node():
    exists = litegraph.Node.exists(guid="14ffe58e-6488-4001-bada-6886bcc272ba")
    print(exists)
    
#exists_node()

def create_node():
    node = litegraph.Node.create(name="Test Node",data={"type": "service"})
    print(node)
    
# create_node()

def create_multiple_node():
    nodes = litegraph.Node.create_multiple([
        {
            "name": "Active Directory",
            "data": {
                "type": "service"
            }
        },
        {
            "name": "Website", 
            "data": {
                "type": "service"
            }
        }
    ])
    print(nodes)

# create_multiple_node()

def update_node():
    node = litegraph.Node.update(guid="71eedd9e-3aa9-4e6d-a6ce-299e10fb23ef",name="Test Node Updated")
    print(node)
    
# update_node()

def search_node():
    nodes = litegraph.Node.search(graph_guid="1cbb2bc5-a990-49a8-9975-e0b1c34d1011",expr=litegraph.ExprModel(Left="Name",Operator="Equals",Right="Test"))
    print(nodes)
    
# search_node()

def retrieve_first_node():
    node = litegraph.Node.retrieve_first(graph_guid="1cbb2bc5-a990-49a8-9975-e0b1c34d1011")
    print(node)
    
# retrieve_first_node()

def delete_node():
    litegraph.Node.delete(guid="aaed310d-9c8b-48b8-ad7f-1b35decc7187")
    print("Node deleted")
    
# delete_node()

def delete_multiple_node():
    litegraph.Node.delete_multiple(guid=["a3f25f44-1f88-462c-84bb-df143a73ce69","c674315b-8a1f-4dc4-a6a7-a598379b7918"])
    print("Nodes deleted")

# delete_multiple_node()

def delete_all_node():
    litegraph.Node.delete_all()
    print("Nodes deleted")
    
# delete_all_node()