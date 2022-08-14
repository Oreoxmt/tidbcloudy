from typing import Union, Iterator

from tidbcloudy.context import Context
from tidbcloudy.cluster import Cluster
from tidbcloudy.restore import Restore
from tidbcloudy.specification import CreateClusterConfig, UpdateClusterConfig
from tidbcloudy.util.timestamp import timestamp_to_string
from tidbcloudy.util.page import Page


# noinspection PyShadowingBuiltins
class Project:
    def __init__(self,
                 context: Context,
                 id: str = None,
                 *,
                 org_id: str = None,
                 name: str = None,
                 cluster_count: int = None,
                 user_count: int = None,
                 create_timestamp: int = None):
        self._context = context
        self._id = id
        self._org_id = org_id
        self._name = name
        self._cluster_count = cluster_count
        self._user_count = user_count
        self._create_timestamp = create_timestamp

    @property
    def id(self):
        return self._id

    def _assign_from_object(self, obj: dict):
        self._id = obj["id"]
        self._org_id = obj["org_id"]
        self._name = obj["name"]
        self._cluster_count = obj["cluster_count"]
        self._user_count = obj["user_count"]
        self._create_timestamp = int(obj["create_timestamp"])

    def to_object(self) -> dict:
        return {
            "id": self._id,
            "org_id": self._org_id,
            "name": self._name,
            "cluster_count": self._cluster_count,
            "user_count": self._user_count,
            "create_timestamp": self._create_timestamp,
        }

    @classmethod
    def from_object(cls, context: Context, obj: dict):
        new_project = cls(context)
        new_project._assign_from_object(obj)
        return new_project

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
        path = "projects/{}/clusters".format(self._id)
        resp = self._context.call_post(path=path, json=config)
        return Cluster(self._context, id=resp["id"], project_id=self._id, _from="create")

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
        Cluster(self._context, id=cluster_id, project_id=self._id, _from="dummy").update(config)

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
        Cluster(self._context, id=cluster_id, project_id=self._id, _from="dummy").delete()

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
        path = "projects/{}/clusters/{}".format(self._id, cluster_id)
        resp = self._context.call_get(path=path)
        return Cluster.from_object(self._context, resp)

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
        path = "projects/{}/clusters".format(self._id)
        query = {}
        if page is not None:
            query["page"] = page
        if page_size is not None:
            query["page_size"] = page_size
        resp = self._context.call_get(path=path, params=query)
        return Page(
            [Cluster.from_object(self._context, item) for item in resp["items"]],
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
        path = "projects/{}/restores".format(self._id)
        if isinstance(cluster_config, CreateClusterConfig):
            cluster_config = cluster_config.to_object()
        create_config = {
            "name": name,
            "backup_id": backup_id,
            "config": cluster_config["config"]
        }
        resp = self._context.call_post(path=path, json=create_config)
        return Restore(self._context, id=resp["id"], cluster_id=resp["cluster_id"])

    def get_restore(self, restore_id: str) -> Restore:
        """
        Get the restore.
        Args:
            restore_id:

        Returns:

        """
        path = "projects/{}/restores/{}".format(self._id, restore_id)
        resp = self._context.call_get(path=path)
        return Restore.from_object(self._context, resp)

    def list_restores(self, *, page: int = None, page_size: int = None) -> Page[Restore]:
        """
        List all restores in the project.
        Args:
            page:
            page_size:

        Returns:

        """
        path = "projects/{}/restores".format(self._id)
        query = {}
        if page is not None:
            query["page"] = page
        if page_size is not None:
            query["page_size"] = page_size
        resp = self._context.call_get(path=path, params=query)
        return Page(
            [Restore.from_object(self._context, item) for item in resp["items"]],
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
            self._id, self._name, timestamp_to_string(self._create_timestamp))
