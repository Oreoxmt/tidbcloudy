import os

import tidbcloudy
from tidbcloudy.backup import Backup
from tidbcloudy.cluster import Cluster
from tidbcloudy.project import Project
from tidbcloudy.restore import Restore
from tidbcloudy.specification import ClusterType, ProjectAWSCMEK

public_key = os.environ.get("PUBLIC_KEY")
private_key = os.environ.get("PRIVATE_KEY")
debug_mode = os.environ.get("TIDBCLOUDY_LOG")
project_id = os.environ.get("PROJECT_ID", "1234567890123456789")

api = tidbcloudy.TiDBCloud(public_key=public_key, private_key=private_key)

for project in api.iter_projects():
    assert isinstance(project, Project)
    print(project)
    if project.aws_cmek_enabled:
        for aws_cmek in project.iter_aws_cmek():
            assert isinstance(aws_cmek, ProjectAWSCMEK)
            print(aws_cmek)
    for cluster in project.iter_clusters():
        assert isinstance(cluster, Cluster)
        print(cluster)
        if cluster.cluster_type == ClusterType.DEDICATED:
            for backup in cluster.iter_backups():
                assert isinstance(backup, Backup)
                print(backup)
    for restore in project.iter_restores():
        assert isinstance(restore, Restore)
        print(restore)

# get_project() does not fetch full information of a project from the server by default
project = api.get_project(project_id)
print(project)

# To fetch full information of a project, set update_from_server as True
project = api.get_project(project_id, update_from_server=True)
print(project)
