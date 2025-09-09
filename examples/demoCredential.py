import litegraph

sdk = litegraph.configure(
    endpoint="http://192.168.101.63:8701",
    tenant_guid="00000000-0000-0000-0000-000000000000",
    access_key="litegraphadmin",
)

def create_credential():
    credential = litegraph.Credential.create(user_guid="00000000-0000-0000-0000-000000000000", name="Test Credential", bearer_token="test")
    print(credential)

# create_credential()

def retrieve_all_credential():
    credentials = litegraph.Credential.retrieve_all()
    print(credentials)

# retrieve_all_credential()

def retrieve_credential():
    credential = litegraph.Credential.retrieve(guid="00000000-0000-0000-0000-000000000000")
    print(credential)

# retrieve_credential()

def enumerate_credential():
    credentials = litegraph.Credential.enumerate()
    print(credentials)

# enumerate_credential()

def enumerate_with_query_credential():
    credentials = litegraph.Credential.enumerate_with_query(ordering="CreatedDescending",MaxResults=10,Skip=0,IncludeData=True,IncludeSubordinates=True,Expr=litegraph.ExprModel(Left="Name",Operator="Equals",Right="Test"))
    print(credentials)

# enumerate_with_query_credential()

def retrieve_multiple_credential():
    credentials = litegraph.Credential.retrieve_many(guids=["00000000-0000-0000-0000-000000000000","00000000-0000-0000-0000-000000000000"])
    print(credentials)

# retrieve_multiple_credential()

def update_credential():
    credential = litegraph.Credential.update(guid="00000000-0000-0000-0000-000000000000",user_guid="00000000-0000-0000-0000-000000000000", name="Updated Credential")
    print(credential)

# update_credential()

def delete_credential():
    litegraph.Credential.delete(guid="00000000-0000-0000-0000-000000000000")
    print("Credential deleted")

# delete_credential()

def exists_credential():
    exists = litegraph.Credential.exists(guid="00000000-0000-0000-0000-000000000000")
    print(exists)

exists_credential()