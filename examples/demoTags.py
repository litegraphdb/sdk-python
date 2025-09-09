import litegraph

sdk = litegraph.configure(
    endpoint="http://YOUR_SERVER_URL_HERE:PORT",
    tenant_guid="00000000-0000-0000-0000-000000000000",
    access_key="litegraphadmin",
)

def create_tag():
    tag = litegraph.Tag.create(key="Test Key",value="Test Value")
    print(tag)

# create_tag()

def retrieve_tag():
    tag = litegraph.Tag.retrieve(guid="00000000-0000-0000-0000-000000000000")
    print(tag)

# retrieve_tag()

def create_multiple_tag():
    tags = litegraph.Tag.create_multiple(tags=[
        {
            "Key": "Test Key 1",
            "Value": "Test Value 1"
        },
        {
            "Key": "Test Key 2",
            "Value": "Test Value 2"
        }
    ])
    print(tags)

# create_multiple_tag()

def retrieve_all_tag():
    tags = litegraph.Tag.retrieve_all()
    print(tags)

# retrieve_all_tag()

def retrieve_multiple_tag():
    tags = litegraph.Tag.retrieve_many(guids=["00000000-0000-0000-0000-000000000000","6c01c166-2be9-4afb-8ce0-345445e26206"])
    print(tags)

# retrieve_multiple_tag()

def enumerate_tag():
    tags = litegraph.Tag.enumerate()
    print(tags)

# enumerate_tag()

def enumerate_with_query_tag():
    tags = litegraph.Tag.enumerate_with_query(
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
    print(tags)

enumerate_with_query_tag()

def update_tag():
    tag = litegraph.Tag.update(guid="00000000-0000-0000-0000-000000000000",key="Updated Key",value="Updated Value")
    print(tag)

# update_tag()

def delete_tag():
    litegraph.Tag.delete(guid="8fd19186-da53-4887-837d-a953f4630d39")
    print("Tag deleted")

# delete_tag()

def delete_multiple_tag():
    litegraph.Tag.delete_multiple(guid=["6de05592-ffd5-4ae7-9eaa-f50aeea7fd06","a5ce1932-23b2-4e55-9b16-d83692357500"])
    print("Tags deleted")

#delete_multiple_tag()


def exists_tag():
    exists = litegraph.Tag.exists(guid="f8ba8651-8a80-4de5-8b56-81124a9c4b5a")
    print(exists)

exists_tag()