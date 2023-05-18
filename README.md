# Python SDK for TiDB Cloud

`tidbcloudy` is an **unofficial** Python SDK for [TiDB Cloud](https://tidbcloud.com). If you encounter any problems or have suggestions, feel free to open an issue on the GitHub repository [Oreoxmt/tidbcloudy](https://github.com/Oreoxmt/tidbcloudy).

## Table of contents

- [Introduction](https://github.com/Oreoxmt/tidbcloudy#introduction)

    - [Compatibility with TiDB Cloud API](https://github.com/Oreoxmt/tidbcloudy#compatibility-with-tidb-cloud-api)
    - [Enhancements comparing to original TiDB Cloud API](https://github.com/Oreoxmt/tidbcloudy#enhancements-comparing-to-original-tidb-cloud-api)

- [Installation](https://github.com/Oreoxmt/tidbcloudy#installation)
- [Usage](https://github.com/Oreoxmt/tidbcloudy#usage)

    - [Prerequisites](https://github.com/Oreoxmt/tidbcloudy#prerequisites)
    - [List all resources in your organization](https://github.com/Oreoxmt/tidbcloudy#list-all-resources-in-your-organization)
    - [Create a cluster](https://github.com/Oreoxmt/tidbcloudy#create-a-cluster)
    - [Connect to TiDB](https://github.com/Oreoxmt/tidbcloudy#connect-to-tidb)
    - [Modify a cluster](https://github.com/Oreoxmt/tidbcloudy#modify-a-cluster)
    - [Backup and restore](https://github.com/Oreoxmt/tidbcloudy#backup-and-restore)
    - [Pause or resume your cluster](https://github.com/Oreoxmt/tidbcloudy#pause-or-resume-your-cluster)
    - [Delete all resources](https://github.com/Oreoxmt/tidbcloudy#delete-all-resources)

- [Related projects](https://github.com/Oreoxmt/tidbcloudy#related-projects)

## Introduction

For more information about TiDB Cloud API, see [TiDB Cloud API Documentation](https://docs.pingcap.com/tidbcloud/api/v1beta).

> TiDB Cloud is a fully-managed Database-as-a-Service (DBaaS) that brings everything great about TiDB to your cloud.

If you do not have a TiDB Cloud account yet, you can sign up [here](https://tidbcloud.com). For more details about TiDB Cloud, refer to [TiDB Cloud Documentation](https://docs.pingcap.com/tidbcloud).

You can use this SDK to access [TiDB Cloud](https://tidbcloud.com) and manage your projects, clusters, backups and restores:

- manage your TiDB Cloud **projects** (only _list_ is supported now)
- list all available cloud providers (AWS and GCP), regions and specifications before creating or modifying a cluster
- manage your Serverless Tier or Dedicated Tier **clusters** (_create_, _modify_, _pause_, _resume_, _get_, _list_, _delete_)
- manage your **backups** of a cluster (_create_, _get_, _list_, _delete_)
- manage your **restores** of a project (_create_, _get_, _list_)

### Compatibility with TiDB Cloud API

`tidbcloudy` is compatible with [TiDB Cloud API](https://docs.pingcap.com/tidbcloud/api/v1beta). **Endpoints added in [Release 20230228](https://docs.pingcap.com/tidbcloud/api/v1beta#section/API-Changelog/20230228) and [Release 20230328](https://docs.pingcap.com/tidbcloud/api/v1beta#section/API-Changelog/20230328) are not supported for now**. The following table lists the supported API versions:

| tidbcloudy                                                         | TiDB Cloud API                                                                                          |
|--------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------|
| [1.0.1](https://github.com/Oreoxmt/tidbcloudy/releases/tag/v1.0.1), [1.0.2](https://github.com/Oreoxmt/tidbcloudy/releases/tag/v1.0.2), [1.0.3](https://github.com/Oreoxmt/tidbcloudy/releases/tag/v1.0.3) | v1beta [Release 20220906](https://docs.pingcap.com/tidbcloud/api/v1beta#section/API-Changelog/20220906), [Release 20220920](https://docs.pingcap.com/tidbcloud/api/v1beta#section/API-Changelog/20220920), [Release 20221028](https://docs.pingcap.com/tidbcloud/api/v1beta#section/API-Changelog/20221028), [Release 20230104](https://docs.pingcap.com/tidbcloud/api/v1beta#section/API-Changelog/20230104), [Release 20230214](https://docs.pingcap.com/tidbcloud/api/v1beta#section/API-Changelog/20230214), [Release 20230321](https://docs.pingcap.com/tidbcloud/api/v1beta#section/API-Changelog/20230321)|
| [1.0.0](https://github.com/Oreoxmt/tidbcloudy/releases/tag/v1.0.0) | v1beta [Release 20220823](https://docs.pingcap.com/tidbcloud/api/v1beta#section/API-Changelog/20220823) |
| [0.2.1](https://github.com/Oreoxmt/tidbcloudy/releases/tag/v0.2.1) | v1beta [Release 20220809](https://docs.pingcap.com/tidbcloud/api/v1beta#section/API-Changelog/20220809) |                                                                          |

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
pip3 install tidbcloudy
```

⚠️ Make sure that you have installed **mysql client** in your environment. For more information, see [PyMySQL/mysqlclient](https://github.com/PyMySQL/mysqlclient#install).

## Usage

### Prerequisites

- Create a TiDB Cloud account.
- Create a TiDB Cloud API key. To manage your API keys, see [TiDB Cloud API Documentation](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management).
- Install the latest version of `tidbcloudy`.

To get full code examples, see the [`examples`](https://github.com/Oreoxmt/tidbcloudy/tree/main/examples) folder.

> Note:
>
> It is recommended to set environment variables for your API public and private key. For example, in bash, you can:
>
> ```bash
> export PUBLIC_KEY=your_api_public_key
> export PRIVATE_KEY=your_api_private_key
> ```

### List all resources in your organization

To get the full code example of listing all projects, clusters, backup tasks, and restore tasks in your organization, see [`0_list_resources.py`](https://github.com/Oreoxmt/tidbcloudy/tree/main/examples/0_list_resources.py).

```python
import os

import tidbcloudy
from tidbcloudy.specification import ClusterType

public_key = os.environ.get("PUBLIC_KEY")
private_key = os.environ.get("PRIVATE_KEY")

api = tidbcloudy.TiDBCloud(public_key=public_key, private_key=private_key)

for project in api.iter_projects():
    print(project)
    for cluster in project.iter_clusters():
        print(cluster)
        if cluster.cluster_type == ClusterType.DEDICATED:
            for backup in cluster.iter_backups():
                print(backup)
    for restore in project.iter_restores():
        print(restore)
```

### Create a cluster

Before creating a cluster, you should list all available provider regions and cluster configuration specifications. For more details, run the [`1_list_provider_regions.py`](https://github.com/Oreoxmt/tidbcloudy/tree/main/examples/1_list_provider_regions.py).

```python
import os

import tidbcloudy

public_key = os.environ.get("PUBLIC_KEY")
private_key = os.environ.get("PRIVATE_KEY")

api = tidbcloudy.TiDBCloud(public_key=public_key, private_key=private_key)

for spec in api.list_provider_regions():
    print(f"- type: {spec.cluster_type.value}")
    print(f"  provider: {spec.cloud_provider.value}")
    print(f"  region: {spec.region}")
    print(f"  components:")
    for tidb in spec.tidb:
        print(f"  - tidb: {tidb.node_size}; "
              f"min={tidb.node_quantity_range.min} step={tidb.node_quantity_range.step}")
    for tikv in spec.tikv:
        print(f"  - tikv: {tikv.node_size}; "
              f"min={tikv.node_quantity_range.min} "
              f"step={tikv.node_quantity_range.step}; "
              f"{tikv.storage_size_gib_range.min}..{tikv.storage_size_gib_range.max} GiB")
    for tiflash in spec.tiflash:
        print(
            f"  - tiflash: {tiflash.node_size}; "
            f"min={tiflash.node_quantity_range.min} step={tiflash.node_quantity_range.step}; "
            f"{tiflash.storage_size_gib_range.min}..{tiflash.storage_size_gib_range.max} GiB")
```

> Note:
>
> Creating a cluster might cost money. For more details, see [TiDB Cloud pricing details](https://www.pingcap.com/tidb-cloud-pricing-details).

To create a Serverless Tier cluster, run the [`2_1_create_serverless_cluster.py`](https://github.com/Oreoxmt/tidbcloudy/tree/main/examples/2_1_create_serverless_cluster.py).

To create a Dedicated Tier cluster, run the [`2_2_create_dedicated_cluster.py`](https://github.com/Oreoxmt/tidbcloudy/tree/main/examples/2_2_create_dedicated_cluster.py).

The following takes creating a Serverless Tier cluster as an example:

```python
import os
import tidbcloudy
from tidbcloudy.specification import CreateClusterConfig

public_key = os.environ.get("PUBLIC_KEY")
private_key = os.environ.get("PRIVATE_KEY")
debug_mode = os.environ.get("TIDBCLOUDY_LOG")
project_id = "1234567890123456789"

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

cluster.wait_for_available()
```

### Connect to TiDB

To connect to your TiDB cluster, run the [`3_connect_mysql.py`](https://github.com/Oreoxmt/tidbcloudy/tree/main/examples/3_connect_mysql.py).

```python
import os

import tidbcloudy
from tidbcloudy.specification import ClusterStatus

public_key = os.environ.get("PUBLIC_KEY")
private_key = os.environ.get("PRIVATE_KEY")
project_id = "1234567890123456789"
cluster_id = "1234567890123456789"

print("Connecting to TiDB Cloud...")
api = tidbcloudy.TiDBCloud(public_key=public_key, private_key=private_key)
project = api.get_project(project_id, update_from_server=True)
cluster = project.get_cluster(cluster_id)
print(cluster)

if cluster.status.cluster_status == ClusterStatus.AVAILABLE:
    connection_strings = cluster.status.connection_strings
    connection = cluster.connect(type="standard", database="test", password="your_root_password")
    print(connection)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT DATABASE();")
            m = cursor.fetchone()
            print(m[0])
```

### Modify a cluster

> Note:
>
> Modify a cluster might cost money. For more details, see [TiDB Cloud pricing details](https://www.pingcap.com/tidb-cloud-pricing-details).

To modify a cluster, run the [`4_scale_a_cluster.py`](https://github.com/Oreoxmt/tidbcloudy/tree/main/examples/4_scale_a_cluster.py).

```python
import os

import tidbcloudy
from tidbcloudy.specification import UpdateClusterConfig

public_key = os.environ.get("PUBLIC_KEY")
private_key = os.environ.get("PRIVATE_KEY")
project_id = "1234567890123456789"
cluster_id = "1234567890123456789"

api = tidbcloudy.TiDBCloud(public_key=public_key, private_key=private_key)
project = api.get_project(project_id, update_from_server=True)
cluster = project.get_cluster(cluster_id)

print("The original config is: {}".format(cluster.config.components.to_object()))

new_config = UpdateClusterConfig()
new_config.update_component("tiflash", node_quantity=1, node_size="8C64G", storage_size_gib=500)
cluster.update(new_config)
cluster.wait_for_available()

print("The new config is: {}".format(cluster.config.components.to_object()))
```

### Backup and restore

> Note:
>
> Backup or restore a cluster might cost money. For more details, see [TiDB Cloud pricing details](https://www.pingcap.com/tidb-cloud-pricing-details).

To create a backup and restore, run the [`5_backup_restore.py`](https://github.com/Oreoxmt/tidbcloudy/tree/main/examples/5_backup_restore.py)

```python
import os

import tidbcloudy
from tidbcloudy.specification import CreateClusterConfig

public_key = os.environ.get("PUBLIC_KEY")
private_key = os.environ.get("PRIVATE_KEY")
project_id = "1234567890123456789"
cluster_id = "1234567890123456789"
backup_id = "1234567"

api = tidbcloudy.TiDBCloud(public_key=public_key, private_key=private_key)
project = api.get_project(project_id, update_from_server=True)
cluster = project.get_cluster(cluster_id)
print("Create a manual backup task")
backup = cluster.create_backup(name="backup-1", description="automatically generated by tidbcloudy")
print(backup)

config = CreateClusterConfig()
config \
    .set_cluster_type("DEDICATED") \
    .set_cloud_provider("AWS") \
    .set_region("us-west-2") \
    .set_port(4399) \
    .set_root_password("your_root_password") \
    .set_component("tidb", "8C16G", 1) \
    .set_component("tikv", "8C32G", 3, 500) \
    .set_component("tiflash", "8C64G", 1, 500) \
    .add_current_ip_access()
print("Create a restore task from backup_id={}".format(backup_id))
restore = project.create_restore(backup_id=backup_id, name="restore-1", cluster_config=config)
restore_task = project.get_restore(restore.id)
print(restore_task.to_object())
for restore in project.iter_restores():
    print(restore)
```

### Pause or resume your cluster

To pause or resume your cluster, run the [`6_pause_cluster.py`](https://github.com/Oreoxmt/tidbcloudy/tree/main/examples/6_pause_cluster.py).

```python
import os

import tidbcloudy
from tidbcloudy.specification import ClusterStatus

public_key = os.environ.get("PUBLIC_KEY")
private_key = os.environ.get("PRIVATE_KEY")
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
```

### Delete all resources

> Warning:
>
> This is a destructive operation. It will delete all resources in the project. **DO NOT** run this script in a production environment.

To delete all clusters and backup tasks in your project, run the [`7_delete_resources.py`](https://github.com/Oreoxmt/tidbcloudy/tree/main/examples/7_delete_resources.py).

```python
import os

import tidbcloudy
from tidbcloudy.specification import ClusterType

public_key = os.environ.get("PUBLIC_KEY")
private_key = os.environ.get("PRIVATE_KEY")
project_id = "1234567890123456789"

api = tidbcloudy.TiDBCloud(public_key=public_key, private_key=private_key)
project = api.get_project(project_id, update_from_server=True)
for cluster in project.iter_clusters():
    print(cluster)
    if cluster.cluster_type == ClusterType.DEDICATED:
        for backup in cluster.iter_backups():
            print(backup)
            backup.delete()
    cluster.delete()
```

## Related projects

- Go SDK: [go-tidbcloud-sdk-v1](https://github.com/c4pt0r/go-tidbcloud-sdk-v1) by [@c4pt0r](https://github.com/c4pt0r)
- Official TiDB Cloud CLI: [tidbcloud-cli](https://github.com/tidbcloud/tidbcloud-cli) | [User documentation](https://docs.pingcap.com/tidbcloud/cli-reference)
- Official code samples in Go and Python: [tidbcloud-api-samples](https://github.com/tidbcloud/tidbcloud-api-samples)
