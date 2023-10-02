import os

import tidbcloudy
from tidbcloudy.specification import UpdateClusterConfig

public_key = os.environ.get("PUBLIC_KEY")
private_key = os.environ.get("PRIVATE_KEY")
debug_mode = os.environ.get("TIDBCLOUDY_LOG")
project_id = os.environ.get("PROJECT_ID", "1234567890123456789")
cluster_id = os.environ.get("CLUSTER_ID", "1234567890123456789")

api = tidbcloudy.TiDBCloud(public_key=public_key, private_key=private_key)
project = api.get_project(project_id, update_from_server=True)
cluster = project.get_cluster(cluster_id)

print("The original config is: {}".format(cluster.config.components.to_object()))
new_config = UpdateClusterConfig()
new_config.update_component("tiflash", node_quantity=1, node_size="8C64G", storage_size_gib=500)
cluster.update(new_config)
cluster.wait_for_available()
print("The new config is: {}".format(cluster.config.components.to_object()))
