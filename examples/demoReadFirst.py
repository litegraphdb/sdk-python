import litegraph

sdk = litegraph.configure(
    endpoint="http://ec2-18-217-169-161.us-east-2.compute.amazonaws.com:8701",
    tenant_guid="00000000-0000-0000-0000-000000000000",
    access_key="litegraphadmin",
)


def read_first_graph():
    graph = litegraph.Graph.read_first(ordering="CreatedDescending")
    print(graph)


# read_first_graph()


def read_first_node():
    node = litegraph.Node.read_first(graph_guid="8e72e2b7-86fe-4f94-8483-547c23c8a833")
    print(node)


# read_first_node()


def read_first_edge():
    edge = litegraph.Edge.read_first(graph_guid="8e72e2b7-86fe-4f94-8483-547c23c8a833")
    print(edge)


# read_first_edge()


def create_backup():
    backup = litegraph.Admin.create_backup(filename="my-backup-py1.db")
    print(backup)


# create_backup()


def check_backup_exists():
    backup = litegraph.Admin.exists(filename="my-backup-py11.db")
    print(backup)


# check_backup_exists()


def retrieve_all_backups():
    backups = litegraph.Admin.retrieve_all()
    print(backups)


# retrieve_all_backups()


def retrieve_backup():
    backup = litegraph.Admin.retrieve(filename="my-backup-py1.db")
    print(backup)


# retrieve_backup()


def delete_backup():
    backup = litegraph.Admin.delete(filename="my-backup-py1.db")
    print(backup)


# delete_backup()


def flush_db_to_disk():
    backup = litegraph.Admin.flush_db_to_disk()
    print(backup)


# flush_db_to_disk()
