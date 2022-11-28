import os

import tidbcloudy
from tidbcloudy.api.specification import CreateClusterConfig

public_key = os.environ.get("PUBLIC_KEY")
private_key = os.environ.get("PRIVATE_KEY")
debug_mode = os.environ.get("TIDBCLOUDY_LOG")
project_id = "1234567890123456789"

api = tidbcloudy.TiDBCloud(public_key=public_key, private_key=private_key)
project = api.get_project(project_id, update_from_server=True)

config = CreateClusterConfig()
config\
    .set_name("dedicated-1") \
    .set_cluster_type("DEDICATED") \
    .set_cloud_provider("AWS") \
    .set_region("us-west-2") \
    .set_port(4399) \
    .set_root_password("your_root_password") \
    .set_component("tidb", "8C16G", 1) \
    .set_component("tikv", "8C32G", 3, 500) \
    .add_current_ip_access()
cluster = project.create_cluster(config)
print(cluster)

cluster.wait_for_ready()
