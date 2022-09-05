# Python SDK for [TiDB Cloud](https://tidbcloud.com)

## Introduction

`tidbcloudy` is a Python package that provides a high-level interface to access [TiDB Cloud](https://tidbcloud.com). For more information about TiDB Cloud API, see [TiDB Cloud API Documentation](https://docs.pingcap.com/tidbcloud/api/v1beta).

## Installation

```bash
pip install tidbcloudy
```

Make sure that you have installed mysql client in your environment. For more information, see [PyMySQL/mysqlclient](https://github.com/PyMySQL/mysqlclient#install).

## Usage

To get full code examples, see the [`examples`](/examples/) folder.

### List all resources in your organization

To get the full code example of listing all projects, clusters, backup tasks, and restore tasks in your organization, see [`/examples/0_list_resources.py`](/examples/0_list_resources.py).

```python
import tidbcloudy

api = tidbcloudy.TiDBCloud(public_key="public_key", private_key="private_key")
for project in api.iter_projects():
    print(project)
    for cluster in project.iter_clusters():
        print(cluster)
        for backup in cluster.iter_backups():
            print(backup)
    for restore in project.iter_restores():
        print(restore)
```

### Create a cluster

To list all provider regions and cluster configuration specifications, run the [`/examples/1_list_provider_regions.py`](/examples/1_list_provider_regions.py).

To create a Developer Tier cluster, run the [`2_1_create_developer_cluster.py`](/examples/2_1_create_developer_cluster.py).

To create a Dedicated Tier cluster, run the [`2_2_create_dedicated_cluster.py`](/examples/2_2_create_dedicated_cluster.py).

```python
import tidbcloudy
from tidbcloudy.specification import CreateClusterConfig

api = tidbcloudy.TiDBCloud(public_key="public_key", private_key="private_key")
project = api.get_project("project_id", update_from_server=True)

config = CreateClusterConfig()
config.set_name("cluster-name") \
    .set_cluster_type("cluster-type") \
    .set_cloud_provider("cloud-provider") \
    .set_region("region-code") \
    .set_port(4399) \
    .set_root_password("root_password") \
    .set_component("tidb", "8C16G", 1) \
    .set_component("tikv", "8C32G", 3, 500) \
    .add_current_ip_access()

cluster = project.create_cluster(config)
cluster.wait_for_ready()
```

### Connect with TiDB

To connect with your TiDB cluster, run the [](/examples/3_connect_mysql.py).

```python
```

### Modify a cluster

To modify a cluster, run the [](/examples/4_scale_a_cluster.py).

```python
import tidbcloudy
from tidbcloudy.specification import UpdateClusterConfig

api = tidbcloudy.TiDBCloud(public_key="public_key", private_key="private_key")
project = api.get_project("project_id", update_from_server=True)
cluster = project.get_cluster("cluster_id")
new_config = UpdateClusterConfig()
new_config.update_component("tiflash", node_quantity=1, node_size="8C64G", storage_size_gib=500)
cluster.update(new_config)
```

### Backup and restore

To create a backup and restore, run the [](/examples/5_backup_restore.py)

```python
import tidbcloudy

api = tidbcloudy.TiDBCloud(public_key="public_key", private_key="private_key")
project = api.get_project("project_id", update_from_server=True)
cluster = project.get_cluster("cluster_id")
backup = cluster.create_backup(name="backup-1", description="created by tidbcloudy")
print(backup)
```

### Pause or resume your cluster

To pause or resume your cluster, run the [](/examples/6_pause_cluster.py).

```python
```

### Delete all resources

To delete all clusters and backup tasks in your project, run the [](/examples/7_delete_resources.py).

```python
```

## Enhancements comparing to original TiDB Cloud API

- Iterate over resources instead of manual pagination
- Connect to a TiDB cluster using the MySQL client
- Get a Project using a Project ID
- Configure your cluster with method chaining
- Add your current IP address automatically
- Wait for the cluster to be ready when creating/modifying a cluster
- Case-insensitive when setting cluster type, cloud provider, and component name
