import os

import tidbcloudy
from tidbcloudy.specification import ClusterStatus

public_key = os.environ.get("PUBLIC_KEY")
private_key = os.environ.get("PRIVATE_KEY")
debug_mode = os.environ.get("TIDBCLOUDY_LOG")
project_id = os.environ.get("PROJECT_ID", "1234567890123456789")
cluster_id = os.environ.get("CLUSTER_ID", "1234567890123456789")

print("Connecting to TiDB Cloud...")
api = tidbcloudy.TiDBCloud(public_key=public_key, private_key=private_key)
project = api.get_project(project_id, update_from_server=True)
cluster = project.get_cluster(cluster_id)
print(cluster)

if cluster.status.cluster_status == ClusterStatus.AVAILABLE:
    connection_strings = cluster.status.connection_strings
    connection = cluster.connect(type="standard", database="test",
                                 password=os.environ.get("CLUSTER_PWD", "your_root_password"))
    print(connection)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT DATABASE();")
            m = cursor.fetchone()
            print(m[0])
