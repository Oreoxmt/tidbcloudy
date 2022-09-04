from typing import Union, Iterator

from ._base import TiDBCloudyBase, TiDBCloudyContextualBase, TiDBCloudyField
from .cluster import Cluster
from .restore import Restore
from .specification import CreateClusterConfig, UpdateClusterConfig
from .util.timestamp import timestamp_to_string
from .util.page import Page


# noinspection PyShadowingBuiltins
class Project(TiDBCloudyBase, TiDBCloudyContextualBase):
    __slots__ = ["_id", "_org_id", "_name", "_cluster_count", "_user_count", "_create_timestamp"]
    id: str = TiDBCloudyField(str)
    org_id: str = TiDBCloudyField(str)
    name: str = TiDBCloudyField(str)
    cluster_count: int = TiDBCloudyField(int)
    user_count: int = TiDBCloudyField(int)
    create_timestamp: int = TiDBCloudyField(int, convert_from=int, convert_to=str)

    def create_cluster(self, config: Union[CreateClusterConfig, dict]) -> Cluster:
        """
        Create a cluster in the project.
        Args:
            config: the configuration of the cluster.

        Returns:
            The created cluster instance.

        Examples:
            .. code-block:: python
                import tidbcloudy
                api = tidbcloudy.TiDBCloud(public_key="your_public_key", private_key="your_private_key")
                project = api.get_project(project_id)
                config = CreateClusterConfig()
                config.set_name("your_cluster_name") \
                        .set_cluster_type("your_cluster_type") \
                        .set_cloud_provider("your_cloud_provider") \
                        .set_region("your_region") \
                        .set_port(4000) \
                        .set_root_password("your_root_password") \
                        .set_component("tidb", "8C16G", 2) \
                        .set_component("tikv", "8C32G", 3, 500) \
                        .set_component("tiflash", "16C128G", 1, 500) \
                        .add_ip_access(cidr="your ip") \
                        .add_ip_access(cidr="your ip")
                cluster = project.create_cluster(config)
                cluster.wait_for_ready()
        """
        if isinstance(config, CreateClusterConfig):
            config = config.to_object()
        path = "projects/{}/clusters".format(self.id)
        resp = self.context.call_post(path=path, json=config)
        return Cluster(context=self.context, id=resp["id"], project_id=self.id)

    def update_cluster(self, cluster_id: str, config: Union[UpdateClusterConfig, dict]):
        """
        Update the cluster.
        Args:
            cluster_id: the id of the cluster you want to update.
            config: the updated configuration of the cluster.

        Returns:
            The updated cluster instance.

        Examples:
            .. code-block:: python
                import tidbcloudy
                api = tidbcloudy.TiDBCloud(public_key="your_public_key", private_key="your_private_key")
                project = api.get_project(project_id)
                cluster = project.get_cluster(cluster_id)
                new_cluster_config = UpdateClusterConfig()
                new_cluster_config.update_component("tidb", 1).update_component("tikv", 1)
                new_cluster = project.update_cluster(cluster_id=cluster._id, config=new_config.to_object())
        """
        Cluster(context=self.context, id=cluster_id, project_id=self.id).update(config)

    def delete_cluster(self, cluster_id: str):
        """
        Delete the cluster.
        Args:
            cluster_id: the id of the cluster you want to delete.

        Returns:
            The response of the delete request.

        Examples:
            .. code-block:: python
                import tidbcloudy
                api = tidbcloudy.TiDBCloud(public_key="your_public_key", private_key="your_private_key")
                project = api.get_project(project_id)
                project.delete_cluster(cluster_id)
        """
        Cluster(context=self.context, id=cluster_id, project_id=self.id).delete()

    def get_cluster(self, cluster_id: str) -> Cluster:
        """
        Get the cluster.
        Args:
            cluster_id: the id of the cluster you want to get.

        Returns:
            The cluster instance.

        Examples:
            .. code-block:: python
                import tidbcloudy
                api = tidbcloudy.TiDBCloud(public_key="your_public_key", private_key="your_private_key")
                project = api.get_project(project_id)
                cluster = project.get_cluster(cluster_id)

        """
        path = "projects/{}/clusters/{}".format(self.id, cluster_id)
        resp = self.context.call_get(path=path)
        return Cluster.from_object(self.context, resp)

    def iter_clusters(self, page_size: int = 10) -> Iterator[Cluster]:
        """
        This is not a TiDB Cloud API official endpoint.
        Iterate all clusters in the project.
        Args:
            page_size:

        Returns:
            The iterator of the clusters.

        Examples:
            .. code-block:: python
                import tidbcloudy
                api = tidbcloudy.TiDBCloud(public_key="your_public_key", private_key="your_private_key")
                project = api.get_project(project_id)
                for cluster in project.iter_clusters():
                    print(cluster) # This is a Cluster instance.

        """
        page = 1
        total = None
        while total is None or (page - 1) * page_size < total:
            clusters = self.list_clusters(page=page, page_size=page_size)
            total = clusters.total
            for cluster in clusters.items:
                yield cluster
            page += 1

    def list_clusters(self, page: int = None, page_size: int = None) -> Page[Cluster]:
        """
        List all clusters in the project.
        Args:
            page:
            page_size:

        Returns:

        Examples:
            .. code-block:: python
                import tidbcloudy
                api = tidbcloudy.TiDBCloud(public_key="your_public_key", private_key="your_private_key")
                project = api.get_project(project_id)
                clusters = project.list_clusters()
                for cluster in clusters["items"]:
                    print(cluster) # This is a Cluster instance.

        """
        path = "projects/{}/clusters".format(self.id)
        query = {}
        if page is not None:
            query["page"] = page
        if page_size is not None:
            query["page_size"] = page_size
        resp = self.context.call_get(path=path, params=query)
        return Page(
            [Cluster.from_object(self.context, item) for item in resp["items"]],
            page, page_size, resp["total"])

    def create_restore(self, *, name: str, backup_id: str, cluster_config: Union[CreateClusterConfig, dict]) -> Restore:
        """
        Create a restore in the project.
        Args:
            name:
            backup_id:
            cluster_config:

        Returns:

        """
        path = "projects/{}/restores".format(self.id)
        if isinstance(cluster_config, CreateClusterConfig):
            cluster_config = cluster_config.to_object()
        create_config = {
            "name": name,
            "backup_id": backup_id,
            "config": cluster_config["config"]
        }
        resp = self.context.call_post(path=path, json=create_config)
        return Restore(context=self.context, id=resp["id"], cluster_id=resp["cluster_id"])

    def get_restore(self, restore_id: str) -> Restore:
        """
        Get the restore.
        Args:
            restore_id:

        Returns:

        """
        path = "projects/{}/restores/{}".format(self.id, restore_id)
        resp = self.context.call_get(path=path)
        return Restore.from_object(self.context, resp)

    def list_restores(self, *, page: int = None, page_size: int = None) -> Page[Restore]:
        """
        List all restores in the project.
        Args:
            page:
            page_size:

        Returns:

        """
        path = "projects/{}/restores".format(self.id)
        query = {}
        if page is not None:
            query["page"] = page
        if page_size is not None:
            query["page_size"] = page_size
        resp = self.context.call_get(path=path, params=query)
        return Page(
            [Restore.from_object(self.context, item) for item in resp["items"]],
            page, page_size, resp["total"]
        )

    def iter_restores(self, page_size: int = 10) -> Iterator[Restore]:
        """
        This is not a TiDB Cloud API official endpoint.
        Iterate all restores in the project.
        Args:
            page_size:

        Returns:

        """
        page = 1
        total = None
        while total is None or (page - 1) * page_size < total:
            restores = self.list_restores(page=page, page_size=page_size)
            total = restores.total
            for restore in restores.items:
                yield restore
            page += 1

    def __repr__(self):
        return "<Project id={} name={} create_at={}>".format(
            self.id, self.name, timestamp_to_string(self.create_timestamp))
