import litegraph

sdk = litegraph.configure(
    endpoint="http://192.168.101.63:8701",
    tenant_guid="00000000-0000-0000-0000-000000000000",
    access_key="litegraphadmin",
)

def create_user():
    user = litegraph.User.create(email="test@test.com", password="password", first_name="Test", last_name="User")
    print(user)

# create_user()

def retrieve_user():
    user = litegraph.User.retrieve(guid="00000000-0000-0000-0000-000000000000")
    print(user)

# retrieve_user()

def enumerate_user():
    users = litegraph.User.enumerate()
    print(users)

# enumerate_user()

def enumerate_with_query_user():
    users = litegraph.User.enumerate_with_query(ordering="CreatedDescending",MaxResults=10,Skip=0,IncludeData=True,IncludeSubordinates=True,Expr=litegraph.ExprModel(Left="Name",Operator="Equals",Right="Test"))
    print(users)

# enumerate_with_query_user()

def retrieve_multiple_user():
    users = litegraph.User.retrieve_many(guids=["00000000-0000-0000-0000-000000000000","00000000-0000-0000-0000-000000000000"])
    print(users)

# retrieve_multiple_user()

def retrieve_all_user():
    users = litegraph.User.retrieve_all()
    print(users)

# retrieve_all_user()

def exists_user():
    exists = litegraph.User.exists(guid="00000000-0000-0000-0000-000000000000")
    print(exists)

# exists_user()

def delete_user():
    litegraph.User.delete(guid="21844ccc-d0c9-4cac-bc5b-405cb2d0bf67")
    print("User deleted")

# delete_user()

def update_user():
    user = litegraph.User.update(guid="00000000-0000-0000-0000-000000000000", first_name="Test", last_name="User")
    print(user)

update_user()