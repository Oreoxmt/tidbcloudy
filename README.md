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
    - [Create a project and manage your AWS CMEK](https://github.com/Oreoxmt/tidbcloudy#create-a-project-and-manage-your-aws-cmek) **New in 1.0.9**
    - [Create a cluster](https://github.com/Oreoxmt/tidbcloudy#create-a-cluster)
    - [Connect to TiDB](https://github.com/Oreoxmt/tidbcloudy#connect-to-tidb)
    - [Modify a cluster](https://github.com/Oreoxmt/tidbcloudy#modify-a-cluster)
    - [Backup and restore](https://github.com/Oreoxmt/tidbcloudy#backup-and-restore)
    - [Pause or resume your cluster](https://github.com/Oreoxmt/tidbcloudy#pause-or-resume-your-cluster) **New in 1.0.0**
    - [Get monthly bills of your organization](https://github.com/Oreoxmt/tidbcloudy#get-monthly-bills-of-your-organization) **New in 1.0.8**
    - [Delete all resources](https://github.com/Oreoxmt/tidbcloudy#delete-all-resources)

- [Related projects](https://github.com/Oreoxmt/tidbcloudy#related-projects)

## Introduction

For more information about TiDB Cloud API, see TiDB Cloud API Documentation ([v1beta](https://docs.pingcap.com/tidbcloud/api/v1beta) and [v1beta1](https://docs.pingcap.com/tidbcloud/api/v1beta1)).

> TiDB Cloud is a fully-managed Database-as-a-Service (DBaaS) that brings everything great about TiDB to your cloud.

If you do not have a TiDB Cloud account yet, you can sign up [here](https://tidbcloud.com). For more details about TiDB Cloud, refer to [TiDB Cloud Documentation](https://docs.pingcap.com/tidbcloud).

You can use this SDK to access [TiDB Cloud](https://tidbcloud.com) and manage your billings, projects, clusters, backups and restores:

- manage your **billings** of your organization (_get_)
- manage your TiDB Cloud **projects** (_list_, _create_) and manage the **AWS CMEK** of your projects (_get_, _create_)
- list all available cloud providers (AWS and GCP), regions, and specifications before creating or modifying a cluster
- manage your TiDB Serverless or TiDB Dedicated **clusters** (_create_, _modify_, _pause_, _resume_, _get_, _list_, _delete_)
- manage your **backups** of a cluster (_create_, _get_, _list_, _delete_)
- manage your **restores** of a project (_create_, _get_, _list_)

### Compatibility with TiDB Cloud API

`tidbcloudy` is compatible with TiDB Cloud API. **Endpoints added in [v1beta Release 20230228](https://docs.pingcap.com/tidbcloud/api/v1beta#section/API-Changelog/20230228) and [v1beta Release 20230905](https://docs.pingcap.com/tidbcloud/api/v1beta#section/API-Changelog/20230905) are not supported for now**. The following table lists the compatibility between `tidbcloudy` and TiDB Cloud API.

<table>
<thead>
  <tr>
    <th rowspan="2"></th>
    <th><a href="https://docs.pingcap.com/tidbcloud/api/v1beta1" target="_blank" rel="noopener noreferrer">TiDB Cloud API v1beta1</a></th>
    <th colspan="13"><a href="https://docs.pingcap.com/tidbcloud/api/v1beta" target="_blank" rel="noopener noreferrer">TiDB Cloud API v1beta</a></th>
  </tr>
  <tr>
    <th><a href="https://docs.pingcap.com/tidbcloud/api/v1beta1#section/API-Changelog/2023-09-28" target="_blank" rel="noopener noreferrer">2023-09-28</a></th>
    <th><a href="https://docs.pingcap.com/tidbcloud/api/v1beta#section/API-Changelog/20230905" target="_blank" rel="noopener noreferrer">20230905</a></th>
    <th><a href="https://docs.pingcap.com/tidbcloud/api/v1beta#section/API-Changelog/20230801" target="_blank" rel="noopener noreferrer">20230801</a></th>
    <th><a href="https://docs.pingcap.com/tidbcloud/api/v1beta#section/API-Changelog/20230602" target="_blank" rel="noopener noreferrer">20230602</a></th>
    <th><a href="https://docs.pingcap.com/tidbcloud/api/v1beta#section/API-Changelog/20230328" target="_blank" rel="noopener noreferrer">20230328</a></th>
    <th><a href="https://docs.pingcap.com/tidbcloud/api/v1beta#section/API-Changelog/20230321" target="_blank" rel="noopener noreferrer">20230321</a></th>
    <th><a href="https://docs.pingcap.com/tidbcloud/api/v1beta#section/API-Changelog/20230228" target="_blank" rel="noopener noreferrer">20230228</a></th>
    <th><a href="https://docs.pingcap.com/tidbcloud/api/v1beta#section/API-Changelog/20230214" target="_blank" rel="noopener noreferrer">20230214</a></th>
    <th><a href="https://docs.pingcap.com/tidbcloud/api/v1beta#section/API-Changelog/20230104" target="_blank" rel="noopener noreferrer">20230104</a></th>
    <th><a href="https://docs.pingcap.com/tidbcloud/api/v1beta#section/API-Changelog/20221028" target="_blank" rel="noopener noreferrer">20221028</a></th>
    <th><a href="https://docs.pingcap.com/tidbcloud/api/v1beta#section/API-Changelog/20220920" target="_blank" rel="noopener noreferrer">20220920</a></th>
    <th><a href="https://docs.pingcap.com/tidbcloud/api/v1beta#section/API-Changelog/20220906" target="_blank" rel="noopener noreferrer">20220906</a></th>
    <th><a href="https://docs.pingcap.com/tidbcloud/api/v1beta#section/API-Changelog/20220823" target="_blank" rel="noopener noreferrer">20220823</a></th>
    <th><a href="https://docs.pingcap.com/tidbcloud/api/v1beta#section/API-Changelog/20220809" target="_blank" rel="noopener noreferrer">20220809</a></th>
  </tr>
</thead>
<tbody>
  <tr>
    <td><a href="https://github.com/Oreoxmt/tidbcloudy/releases/tag/v1.0.9" target="_blank" rel="noopener noreferrer">1.0.9</a></td>
    <td>✅</td>
    <td>❌</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
    <td>❌</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
  </tr>
  <tr>
    <td><a href="https://github.com/Oreoxmt/tidbcloudy/releases/tag/v1.0.8" target="_blank" rel="noopener noreferrer">1.0.8</a></td>
    <td>✅</td>
    <td>❌</td>
    <td>✅</td>
    <td>✅</td>
    <td>❌</td>
    <td>✅</td>
    <td>❌</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
  </tr>
  <tr>
    <td><a href="https://github.com/Oreoxmt/tidbcloudy/releases/tag/v1.0.7" target="_blank" rel="noopener noreferrer">1.0.7</a></td>
    <td>❌</td>
    <td>❌</td>
    <td>✅</td>
    <td>✅</td>
    <td>❌</td>
    <td>✅</td>
    <td>❌</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
  </tr>
  <tr>
    <td><a href="https://github.com/Oreoxmt/tidbcloudy/releases/tag/v1.0.6" target="_blank" rel="noopener noreferrer">1.0.6</a></td>
    <td>❌</td>
    <td>❌</td>
    <td>✅</td>
    <td>✅</td>
    <td>❌</td>
    <td>✅</td>
    <td>❌</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
  </tr>
  <tr>
    <td><a href="https://github.com/Oreoxmt/tidbcloudy/releases/tag/v1.0.5" target="_blank" rel="noopener noreferrer">1.0.5</a></td>
    <td>❌</td>
    <td>❌</td>
    <td>✅</td>
    <td>✅</td>
    <td>❌</td>
    <td>✅</td>
    <td>❌</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
  </tr>
  <tr>
    <td><a href="https://github.com/Oreoxmt/tidbcloudy/releases/tag/v1.0.4" target="_blank" rel="noopener noreferrer">1.0.4</a></td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>❌</td>
    <td>✅</td>
    <td>❌</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
  </tr>
  <tr>
    <td><a href="https://github.com/Oreoxmt/tidbcloudy/releases/tag/v1.0.3" target="_blank" rel="noopener noreferrer">1.0.3</a></td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
  </tr>
  <tr>
    <td><a href="https://github.com/Oreoxmt/tidbcloudy/releases/tag/v1.0.2" target="_blank" rel="noopener noreferrer">1.0.2</a></td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
  </tr>
  <tr>
    <td><a href="https://github.com/Oreoxmt/tidbcloudy/releases/tag/v1.0.1" target="_blank" rel="noopener noreferrer">1.0.1</a></td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>✅</td>
    <td>✅</td>
    <td>✅</td>
  </tr>
  <tr>
    <td><a href="https://github.com/Oreoxmt/tidbcloudy/releases/tag/v1.0.0" target="_blank" rel="noopener noreferrer">1.0.0</a></td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>✅</td>
    <td>✅</td>
  </tr>
  <tr>
    <td><a href="https://github.com/Oreoxmt/tidbcloudy/releases/tag/v0.2.2" target="_blank" rel="noopener noreferrer">0.2.2</a></td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>✅</td>
  </tr>
  <tr>
    <td><a href="https://github.com/Oreoxmt/tidbcloudy/releases/tag/v0.2.1" target="_blank" rel="noopener noreferrer">0.2.1</a></td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>✅</td>
  </tr>
  <tr>
    <td><a href="https://github.com/Oreoxmt/tidbcloudy/releases/tag/v0.2.0" target="_blank" rel="noopener noreferrer">0.2.0</a></td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>/</td>
    <td>✅</td>
  </tr>
</tbody>
</table>

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

**This feature is available in `tidbcloudy` 1.0.9 or later.**

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
    if project.aws_cmek_enabled:
        for aws_cmek in project.iter_aws_cmek():
            print(aws_cmek)
    for cluster in project.iter_clusters():
        print(cluster)
        if cluster.cluster_type == ClusterType.DEDICATED:
            for backup in cluster.iter_backups():
                print(backup)
    for restore in project.iter_restores():
        print(restore)
```

### Create a project and manage your AWS CMEK

To create a project, run the [`8_manage_project.py`](https://github.com/Oreoxmt/tidbcloudy/tree/main/examples/8_manage_project.py).

```python
import os

import tidbcloudy

public_key = os.environ.get("PUBLIC_KEY")
private_key = os.environ.get("PRIVATE_KEY")
debug_mode = os.environ.get("TIDBCLOUDY_LOG")

api = tidbcloudy.TiDBCloud(public_key=public_key, private_key=private_key)
# Create a project with AWS CMEK enabled
project = api.create_project(name="0", aws_cmek_enabled=True, update_from_server=True)
print(project)

# Configure AWS CMEK for the project
project.create_aws_cmek([("your_aws_region_1", "your_aws_kms_arn_1"), ("your_aws_region_2", "your_aws_kms_arn_2")])

# List all AWS CMEKs of the project
for cmek in project.iter_aws_cmek():
    print(cmek)
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

To create a TiDB Serverless cluster, run the [`2_1_create_serverless_cluster.py`](https://github.com/Oreoxmt/tidbcloudy/tree/main/examples/2_1_create_serverless_cluster.py).

To create a TiDB Dedicated cluster, run the [`2_2_create_dedicated_cluster.py`](https://github.com/Oreoxmt/tidbcloudy/tree/main/examples/2_2_create_dedicated_cluster.py).

The following takes creating a TiDB Serverless cluster as an example:

```python
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
    .set_root_password("your_root_password")
cluster = project.create_cluster(config)
print(cluster)

cluster.wait_for_available(interval_sec=1)
print(cluster)
```

### Connect to TiDB

To connect to your TiDB cluster, run the [`3_connect_mysql.py`](https://github.com/Oreoxmt/tidbcloudy/tree/main/examples/3_connect_mysql.py).

```python
import os

import tidbcloudy
from tidbcloudy.specification import ClusterStatus

public_key = os.environ.get("PUBLIC_KEY")
private_key = os.environ.get("PRIVATE_KEY")
project_id = os.environ.get("PROJECT_ID", "1234567890123456789")
cluster_id = os.environ.get("CLUSTER_ID", "1234567890123456789")

print("Connecting to TiDB Cloud...")
api = tidbcloudy.TiDBCloud(public_key=public_key, private_key=private_key)
project = api.get_project(project_id, update_from_server=True)
cluster = project.get_cluster(cluster_id)
print(cluster)

if cluster.status.cluster_status == ClusterStatus.AVAILABLE:
    connection_strings = cluster.status.connection_strings
    connection = cluster.connect(type="standard", database="test", password=os.environ.get("CLUSTER_PWD", "your_root_password"))
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
project_id = os.environ.get("PROJECT_ID", "1234567890123456789")
cluster_id = os.environ.get("CLUSTER_ID", "1234567890123456789")
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

**This feature is available in `tidbcloudy` 1.0.0 or later.**

To pause or resume your cluster, run the [`6_pause_cluster.py`](https://github.com/Oreoxmt/tidbcloudy/tree/main/examples/6_pause_cluster.py).

```python
import os

import tidbcloudy
from tidbcloudy.specification import ClusterStatus

public_key = os.environ.get("PUBLIC_KEY")
private_key = os.environ.get("PRIVATE_KEY")
project_id = os.environ.get("PROJECT_ID", "1234567890123456789")
cluster_id = os.environ.get("CLUSTER_ID", "1234567890123456789")

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

### Get monthly bills of your organization

**This feature is available in `tidbcloudy` 1.0.8 or later.**

To get the billing information of your organization, run the [`v1beta1_get_monthly_bill.py`](https://github.com/Oreoxmt/tidbcloudy/tree/main/examples/v1beta1_get_monthly_bill.py).

```python
import os

import tidbcloudy

public_key = os.environ.get("PUBLIC_KEY")
private_key = os.environ.get("PRIVATE_KEY")
debug_mode = os.environ.get("TIDBCLOUDY_LOG")

api = tidbcloudy.TiDBCloud(public_key=public_key, private_key=private_key)
billing = api.get_monthly_bill(month="2023-10")
# billing = api.get_monthly_bill(month="202310")
# billing = api.get_current_month_bill()
print(billing)
print(billing.overview)
print(billing.summaryByProject)
print(billing.summaryByService)
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
```

## Related projects

- Go SDK: [go-tidbcloud-sdk-v1](https://github.com/c4pt0r/go-tidbcloud-sdk-v1) by [@c4pt0r](https://github.com/c4pt0r)
- Official TiDB Cloud CLI: [tidbcloud-cli](https://github.com/tidbcloud/tidbcloud-cli) | [User documentation](https://docs.pingcap.com/tidbcloud/cli-reference)
- Official code samples in Go and Python: [tidbcloud-api-samples](https://github.com/tidbcloud/tidbcloud-api-samples)
