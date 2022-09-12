# Python SDK for TiDB Cloud

`tidbcloudy` is an unofficial Python SDK for [TiDB Cloud](https://tidbcloud.com).

## Introduction

For more information about TiDB Cloud API, see [TiDB Cloud API Documentation](https://docs.pingcap.com/tidbcloud/api/v1beta).

> TiDB Cloud is a fully-managed Database-as-a-Service (DBaaS) that brings everything great about TiDB to your cloud.

If you do not have a TiDB Cloud account yet, you can sign up [here](https://tidbcloud.com). For more details about TiDB Cloud, refer to [TiDB Cloud Documentation](https://docs.pingcap.com/tidbcloud/).

You can use this SDK to access [TiDB Cloud](https://tidbcloud.com) and manage your projects, clusters, backups and restores:

- manage your TiDB Cloud projects (only _list_ is supported now)
- list all available cloud providers (AWS and GCP), regions and specifications before creating or modifying a cluster
- manage your Developer Tier or Dedicated Tier clusters (_create_, _modify_, _pause_, _resume_, _get_, _list_, _delete_)
- manage your **backups** of a cluster (_crete_, _get_, _list_, _delete_)
- manage your **restores** of a project (_crete_, _get_, _list_)

### Compatibility with TiDB Cloud API

`tidbcloudy` is compatible with [TiDB Cloud API](https://docs.pingcap.com/tidbcloud/api/v1beta). The following table lists the supported API versions.

| tidbcloudy                                                         | TiDB Cloud API                                                                                          |
|--------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------|
| [1.0.1](https://github.com/Oreoxmt/tidbcloudy/releases/tag/v1.0.1) | v1beta [Release 20220906](https://docs.pingcap.com/tidbcloud/api/v1beta#section/API-Changelog/20220906) |
| [1.0.0](https://github.com/Oreoxmt/tidbcloudy/releases/tag/v1.0.0) | v1beta [Release 20220823](https://docs.pingcap.com/tidbcloud/api/v1beta#section/API-Changelog/20220823) |
| [0.2.1](https://github.com/Oreoxmt/tidbcloudy/releases/tag/v0.2.1) | v1beta [Release 20220809](https://docs.pingcap.com/tidbcloud/api/v1beta#section/API-Changelog/20220809)                                                                             |

### Enhancements comparing to original [TiDB Cloud API](https://docs.pingcap.com/tidbcloud/api/v1beta)

- **Iterate over** resources instead of manual pagination
- **Connect to a TiDB cluster** using the [MySQL client](https://github.com/PyMySQL/mysqlclient)
- **Get** a Project using a Project **ID**
- Configure your cluster with **method chaining**
- Add your **current IP address automatically**
- **Wait for the cluster to be ready** when creating/modifying a cluster
- **Case-insensitive** when setting cluster type, cloud provider, and component name

## Installation

```bash
pip install tidbcloudy
```

:warning Make sure that you have installed mysql client in your environment. For more information, see [PyMySQL/mysqlclient](https://github.com/PyMySQL/mysqlclient#install).

## Usage

### Prerequisites

- Create a TiDB Cloud account.
- Create a TiDB Cloud API key. To manage your API keys, see [TiDB Cloud API Documentation](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management).
- Install `tidbcloudy` and the version is >= 0.2.1.

To get full code examples, see the [`examples`](/examples/) folder.

### List all resources in your organization

To get the full code example of listing all projects, clusters, backup tasks, and restore tasks in your organization, see [`/examples/0_list_resources.py`](/examples/0_list_resources.py).

```python
import tidbcloudy

api = tidbcloudy.TiDBCloud(public_key="PUBLIC_KEY", private_key="PRIVATE_KEY")

for project in api.iter_projects():
    print(project)
    for cluster in project.iter_clusters():
        print(cluster)
        if cluster.cluster_type.value == "DEDICATED":
            for backup in cluster.iter_backups():
                print(backup)
    for restore in project.iter_restores():
        print(restore)
```

### Create a cluster

Before creating a cluster, you should list all available provider regions and cluster configuration specifications. For more details, run the [`/examples/1_list_provider_regions.py`](/examples/1_list_provider_regions.py).

```python
import tidbcloudy

api = tidbcloudy.TiDBCloud(public_key="PUBLIC_KEY", private_key="PRIVATE_KEY")

for spec in api.list_provider_regions():
    print(spec)
```

> Note:
> 
> Create a cluster might cause cost. For more details, see [TiDB Cloud pricing details](https://www.pingcap.com/tidb-cloud-pricing-details/).

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

To connect with your TiDB cluster, run the [`3_connect_mysql.py`](/examples/3_connect_mysql.py).

```python
```

### Modify a cluster

> Note:
> 
> Modify a cluster might cause cost. For more details, see [TiDB Cloud pricing details](https://www.pingcap.com/tidb-cloud-pricing-details/).


To modify a cluster, run the [`4_scale_a_cluster.py`](/examples/4_scale_a_cluster.py).

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

> Note:
> 
> Backup or restore a cluster might cause extra cost. For more details, see [TiDB Cloud pricing details](https://www.pingcap.com/tidb-cloud-pricing-details/).


To create a backup and restore, run the [`5_backup_restore.py`](/examples/5_backup_restore.py)

```python
import tidbcloudy

api = tidbcloudy.TiDBCloud(public_key="public_key", private_key="private_key")
project = api.get_project("project_id", update_from_server=True)
cluster = project.get_cluster("cluster_id")
backup = cluster.create_backup(name="backup-1", description="created by tidbcloudy")
print(backup)
```

### Pause or resume your cluster

To pause or resume your cluster, run the [`6_pause_cluster.py`](/examples/6_pause_cluster.py).

```python

```

### Delete all resources

To delete all clusters and backup tasks in your project, run the [`7_delete_resources.py`](/examples/7_delete_resources.py).

```python

```


## TiDB Cloud SDKs


| Language | SDK        |
|----------|------------|
| Python   | tidbcloudy |
| Go       | xxx        |

