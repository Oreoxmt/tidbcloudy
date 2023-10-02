import os

import tidbcloudy
from tidbcloudy.specification import ClusterType

public_key = os.environ.get("PUBLIC_KEY")
private_key = os.environ.get("PRIVATE_KEY")
debug_mode = os.environ.get("TIDBCLOUDY_LOG")
project_id = os.environ.get("PROJECT_ID", "1234567890123456789")

api = tidbcloudy.TiDBCloud(public_key=public_key, private_key=private_key)
project = api.get_project(project_id, update_from_server=True)
for cluster in project.iter_clusters():
    print(cluster)
    if cluster.cluster_type == ClusterType.DEDICATED:
        for backup in cluster.iter_backups():
            print(backup)
            backup.delete()
    cluster.delete()
