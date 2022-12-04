import os
import click
import toml
import json
from tabulate import tabulate

from tidbcloudy.api.tidbcloud import TiDBCloud
from tidbcloudy.api.project import Project
from tidbcloudy.api.cluster import Cluster
from tidbcloudy.exception import TiDBCloudResponseException
from tidbcloudy.util.timestamp import timestamp_to_string
from tidbcloudy.api.specification import ClusterType, CreateClusterConfig


@click.group()
@click.option("--profile", default="default", help="The profile name in config file")
@click.pass_context
def cli(ctx, profile):
    ctx.ensure_object(dict)

    obj = ctx.obj
    obj["config_path"] = os.path.expanduser("~/.tidbcloudy.toml")
    obj["profile_name"] = profile
    obj["profile"] = {}
    obj["api"] = None
    obj["project"] = None

    if os.path.isfile(obj["config_path"]):
        config_content = toml.load(obj["config_path"])
        if profile in config_content:
            obj["profile"] = config_content[profile]
            obj["api"] = TiDBCloud(
                public_key=obj["profile"].get("public_key"),
                private_key=obj["profile"].get("private_key"),
                base_url=obj["profile"].get("base_url"))
            obj["project"] = obj["api"].get_project(obj["profile"].get("project_id"))


@cli.group(name="cluster")
def cli_cluster():
    pass


@cli_cluster.command("create")
@click.option("-f", "--file", help="The json configuration file")
@click.pass_obj
def cli_cluster_create(obj, f):
    cluster_config = CreateClusterConfig()
    api = obj["api"]  # type: TiDBCloud
    project = obj["project"]  # type: Project
    if f is not None:
        cluster_config = json.load(f)
        new_cluster = project.create_cluster(cluster_config)
        click.echo(f"Creating the cluster...")
        new_cluster.wait_for_available()
        return
    cluster_type = click.prompt("Select cluster type",
                                type=click.Choice([str(item.value) for item in ClusterType], case_sensitive=False))
    cluster_config.set_cluster_type(cluster_type)
    name = click.prompt("Specify the cluster name", type=str)
    cluster_config.set_name(name)
    if cluster_type == "DEDICATED":
        port = click.prompt("Specify the cluster port", type=int)
        cluster_config.set_port(port)
    click.echo("Loading cloud provider...")
    provider_regions = api.list_provider_regions()
    available_provider = set()
    for item in provider_regions:
        if item.cluster_type.value == cluster_type:
            available_provider.add(str(item.cloud_provider.value))
    cloud_provider = click.prompt("Select cloud provider",
                                  type=click.Choice(sorted(available_provider), case_sensitive=False))
    cluster_config.set_cloud_provider(cloud_provider)
    click.echo("Loading regions...")
    available_regions = set()
    for item in provider_regions:
        if item.cluster_type.value == cluster_type and item.cloud_provider.value == cloud_provider:
            available_regions.add(str(item.region))
    region = click.prompt("Select cloud region", type=click.Choice(sorted(available_regions), case_sensitive=False))
    cluster_config.set_region(region)
    if cluster_type == "DEDICATED":
        click.echo("Loading cluster configurations...")
        for component in ("tidb", "tikv", "tiflash"):
            for item in provider_regions:
                if item.cluster_type.value == cluster_type and item.cloud_provider.value == cloud_provider and \
                        item.region == region:
                    component_config = getattr(item, component)
                    click.echo(f"Specify the size of {component}")
                    # Configure node_size
                    available_node_size = set()
                    for config_item in component_config:
                        available_node_size.add(str(config_item.node_size))
                    node_size = click.prompt("Select the node size",
                                             type=click.Choice(sorted(available_node_size), case_sensitive=False))

                    # Configure node_quantity
                    node_quantity = None
                    node_storage = None
                    for config_item in component_config:
                        if config_item.node_size == node_size:
                            quantity_min = config_item.node_quantity_range.min
                            quantity_step = config_item.node_quantity_range.step
                            node_quantity = click.prompt(
                                f"Specify the node quantity [min={quantity_min} step={quantity_step}]",
                                type=click.IntRange(quantity_min))

                            # Configure node_storage
                            if hasattr(config_item, "storage_size_gib_range"):
                                storage_min = config_item.storage_size_gib_range.min
                                storage_max = config_item.storage_size_gib_range.max
                                node_storage = click.prompt(
                                    f"Specify the node storage [min={storage_min} max={storage_max}]",
                                    type=click.IntRange(storage_min, storage_max))
                    cluster_config.set_component(component, node_size, node_quantity, node_storage)
    cluster_config.set_root_password("THIS_PASSWORD_IS_NOT_USED")
    new_cluster = project.create_cluster(cluster_config)
    click.echo(f"Creating the cluster {name}")
    new_cluster.wait_for_available()


@cli_cluster.command("modify")
def cli_cluster_modify():
    click.echo('modify cluster')


@cli_cluster.command("list")
@click.pass_obj
def cli_cluster_list(obj):
    project = obj["project"]  # type: Project
    cluster_table = []
    for cluster in project.iter_clusters():
        cluster_table.append(
            [cluster.id,
             cluster.name,
             cluster.status.cluster_status.value,
             cluster.cluster_type.value,
             cluster.status.tidb_version,
             f"{cluster.cloud_provider.value}:{cluster.region}",
             timestamp_to_string(cluster.create_timestamp)
             ]
        )
    click.echo(
        tabulate(cluster_table, headers=["ID", "NAME", "STATUS", "TYPE", "VERSION", "PROVIDER", "CREATED"]))


@cli_cluster.command("info")
@click.argument("cluster_id")
@click.pass_obj
def cli_cluster_info(obj, cluster_id):
    project = obj["project"]
    cluster_info = project.get_cluster(cluster_id).to_object()
    click.echo(json.dumps(cluster_info, indent=2))


@cli_cluster.command("delete")
@click.argument("cluster_id")
@click.pass_obj
def cli_cluster_delete(obj, cluster_id):
    project = obj["project"]  # type: Project
    # Confirm
    project.delete_cluster(cluster_id)


@cli.group(name="project")
def cli_project():
    pass


@cli_project.command("list", help="List all projects")
@click.pass_obj
def cli_project_list(obj):
    api = obj["api"]  # type: TiDBCloud
    project_table = []
    for project in api.iter_projects():
        project_table.append(
            [project.id,
             project.name,
             project.org_id,
             project.cluster_count,
             project.user_count,
             timestamp_to_string(project.create_timestamp)
             ]
        )
    click.echo(
        tabulate(project_table, headers=["ID", "NAME", "ORGANIZATION ID", "CLUSTER", "USER", "CREATED"]))


@cli_project.command("info", help="Get the info of a project")
@click.argument("project_id")
@click.pass_obj
def cli_project_info(obj, project_id):
    api = obj["api"]  # type: TiDBCloud
    cluster_info = api.get_project(project_id, update_from_server=True).to_object()
    click.echo(json.dumps(cluster_info, indent=2))


@cli.group(name="backup")
def cli_backup():
    pass


@cli_backup.command("create")
@click.pass_obj
def cli_backup_create():
    click.echo('create backup')


@cli_backup.command("list")
@click.argument("cluster_id")
@click.pass_obj
def cli_backup_list(obj, cluster_id):
    project = obj["project"]  # type: Project
    cluster = project.get_cluster(cluster_id)  # type: Cluster
    backup_table = []
    for backup in cluster.iter_backups():
        backup_table.append(
            [backup.id,
             backup.name,
             backup.description,
             backup.type,
             backup.size,
             backup.create_timestamp
             ]
        )
    click.echo(
        tabulate(backup_table, headers=["ID", "NAME", "DESCRIPTION", "TYPE", "SIZE", "CREATED"]))


@cli_backup.command("info")
@click.argument("cluster_id")
@click.argument("backup_id")
@click.pass_obj
def cli_backup_info(obj, cluster_id, backup_id):
    project = obj["project"]  # type: Project
    cluster = project.get_cluster(cluster_id)  # type: Cluster
    backup_info = cluster.get_backup(backup_id).to_object()
    click.echo(json.dumps(backup_info, indent=2))


@cli_backup.command("delete")
def cli_backup_delete():
    click.echo('delete backup')


@cli.group(name="restore")
def cli_restore():
    pass


@cli_restore.command("create")
def cli_restore_create():
    click.echo('create restore')


@cli_restore.command("list")
@click.pass_obj
def cli_restore_list(obj):
    click.echo('list restore')
    project = obj["project"]
    for restore in project.iter_restores():
        print(restore)


@cli_restore.command("info")
def cli_restore_info():
    click.echo('info restore')


@cli.command("config", help="Configure your TiDB Cloud API key and in ~/.tidbcloudy.toml")
@click.pass_obj
def cli_config(obj):
    profile_name = obj["profile_name"]
    profile = obj["profile"]

    # Read from user input
    public_key = click.prompt('TiDB Cloud API public key',
                              hide_input=False, default=profile.get("public_key"))
    private_key = click.prompt('TiDB Cloud API private key',
                               hide_input=False, default=profile.get("private_key"))
    base_url = click.prompt('TiDB Cloud API base URL [https://api.tidbcloud.com/api/v1beta/]',
                            hide_input=False, default=profile.get("base_url", ""), show_default=False)

    # Load project info from server
    click.echo("Loading projects ...")
    if base_url == "":
        base_url = None
    api = TiDBCloud(public_key=public_key, private_key=private_key, base_url=base_url)
    try:
        projects = list(api.iter_projects())
    except TiDBCloudResponseException as e:
        click.echo("Error: {}".format(e))
        return

    # Select project
    selected_project = ""
    if len(projects) == 0:
        click.echo("No project found.")
    elif len(projects) == 1:
        selected_project = projects[0]
    else:
        click.echo("Available projects:")
        for index, project in enumerate(projects):
            click.echo(f"{index + 1}. {project.name} (id={project.id})")
        project_choice = click.prompt(f'Select a project (1-{len(projects)})', hide_input=False,
                                      type=click.IntRange(1, len(projects)))
        selected_project = projects[project_choice - 1]
    click.echo(f"Selected project: {selected_project.name} (id={selected_project.id})")

    # Create new profile content
    new_profile = {
        "public_key": public_key,
        "private_key": private_key
    }
    if base_url:
        new_profile["base_url"] = base_url
    if selected_project:
        new_profile["project_id"] = selected_project.id

    # Update configuration file
    config_path = obj["config_path"]
    config_content = {}
    if os.path.isfile(config_path):
        config_content = toml.load(config_path)
    config_content[profile_name] = new_profile
    with open(config_path, 'w') as f:
        toml.dump(config_content, f)


if __name__ == "__main__":
    cli()
