import os

import tidbcloudy
from tidbcloudy.specification import ClusterStatus

public_key = os.environ.get("PUBLIC_KEY")
private_key = os.environ.get("PRIVATE_KEY")
debug_mode = os.environ.get("TIDBCLOUDY_LOG")
project_id = "1372813089206751385"
cluster_id = "10912822641423447137"

print("Connecting to TiDB Cloud...")
api = tidbcloudy.TiDBCloud(public_key=public_key, private_key=private_key)
project = api.get_project(project_id, update_from_server=True)
cluster = project.get_cluster(cluster_id)
print(cluster)

if cluster.status.cluster_status == ClusterStatus.AVAILABLE:
    connection_strings = cluster.status.connection_strings
    connection = cluster.connect(type="standard", database="test", password="xQXacEZAoomvb9BN")
    print(connection)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT DATABASE();")
            m = cursor.fetchone()
            print(m[0])
