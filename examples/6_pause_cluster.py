import os

import tidbcloudy
from tidbcloudy.specification import ClusterStatus

public_key = os.environ.get("PUBLIC_KEY")
private_key = os.environ.get("PRIVATE_KEY")
debug_mode = os.environ.get("TIDBCLOUDY_LOG")
project_id = "1234567890123456789"
cluster_id = "1234567890123456789"

api = tidbcloudy.TiDBCloud(public_key=public_key, private_key=private_key)
project = api.get_project(project_id, update_from_server=True)
cluster = project.get_cluster(cluster_id)

if cluster.status.cluster_status == ClusterStatus.AVAILABLE:
    print("Pause the cluster id={}".format(cluster_id))
    cluster.pause()
if cluster.status.cluster_status == ClusterStatus.PAUSED:
    print("Resume the cluster id={}".format(cluster_id))
    cluster.resume()
if cluster.status.cluster_status == ClusterStatus.RESUMING:
    print("Wait for the RESUMING cluster id={} to be available".format(cluster_id))
    cluster.wait_for_available()
