import litegraph

sdk = litegraph.configure(
    endpoint="http://192.168.101.63:8701",
    access_key="litegraphadmin",
    tenant_guid="00000000-0000-0000-0000-000000000000",
)

def create_backup():
    backup = litegraph.Admin.create_backup(filename="test.backup")
    print(backup)

# create_backup()

def check_backup_exists():
    backup = litegraph.Admin.exists(filename="test.backup")
    print(backup)

# check_backup_exists()

def retrieve_backup():
    backup = litegraph.Admin.retrieve(filename="test.backup")
    print(backup)

# retrieve_backup()

def delete_backup():
    backup = litegraph.Admin.delete(filename="test.backup")
    print(backup)

# delete_backup()

def flush_db_to_disk():
    backup = litegraph.Admin.flush_db_to_disk()
    print(backup)

# flush_db_to_disk()