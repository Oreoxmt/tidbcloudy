import os

import tidbcloudy
from tidbcloudy.specification import CreateClusterConfig

public_key = os.environ.get("PUBLIC_KEY")
private_key = os.environ.get("PRIVATE_KEY")
debug_mode = os.environ.get("TIDBCLOUDY_LOG")
project_id = os.environ.get("PROJECT_ID", "1234567890123456789")

api = tidbcloudy.TiDBCloud(public_key=public_key, private_key=private_key)
project = api.get_project(project_id, update_from_server=True)

config = CreateClusterConfig()
config\
    .set_name("serverless-0") \
    .set_cluster_type("DEVELOPER") \
    .set_cloud_provider("AWS") \
    .set_region("us-west-2") \
    .set_root_password("your_root_password") \
    .add_ip_access(cidr="0.0.0.0/0") \
    .add_current_ip_access()
cluster = project.create_cluster(config)
print(cluster)

cluster.wait_for_available(interval_sec=1)
print(cluster)
