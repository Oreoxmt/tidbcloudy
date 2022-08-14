import time
import MySQLdb
from typing import Union, Iterator

from tidbcloudy.specification import ClusterType, CloudProvider, ClusterConfig, ClusterInfo, UpdateClusterConfig, \
    ClusterStatus
from tidbcloudy.context import Context
from tidbcloudy.backup import Backup
from tidbcloudy.util.log import log
from tidbcloudy.util.timestamp import timestamp_to_string
from tidbcloudy.util.page import Page


# noinspection PyShadowingBuiltins
class Cluster:
    def __init__(self,
                 context: Context,
                 id: str = None,
                 *,
                 project_id: str = None,
                 name: str = None,
                 cluster_type: ClusterType = None,
                 cloud_provider: CloudProvider = None,
                 region: str = None,
                 create_timestamp: int = None,
                 config: ClusterConfig = None,
                 status: ClusterInfo = None,
                 _from: str = None
                 ):
        """
        Create a Cluster instance.
        Args:
            context: Context object.
            id: the id of the cluster.
            project_id: the id of the project.````
            name: the name of the cluster.````
            cluster_type: the type of the cluster.
            cloud_provider: the cloud provider of the cluster.
            region: the region of the cluster.
            create_timestamp: the timestamp of the cluster creation.
            config: the config of the cluster.
            status: the status of the cluster.
            _from: internal use.
        """
        if _from is None:
            if id is None:
                raise TypeError("id")
            if project_id is None:
                raise TypeError("project_id")
            if name is None:
                raise TypeError("name")
            if cluster_type is None:
                raise TypeError("cluster_type")
            if cloud_provider is None:
                raise TypeError("cloud_provider")
            if region is None:
                raise TypeError("region")
            if config is None:
                raise TypeError("config")
        elif _from == "object":
            # When init a cluster instance from object, automatically assign the context and id as None
            pass
        elif _from == "create" or _from == "dummy":
            # When init a cluster instance from Project().create_cluster endpoint,
            # the context, id and project_id are required
            if id is None:
                raise TypeError("id")
            if project_id is None:
                raise TypeError("project_id")
        self._context = context
        self._id = id
        self._project_id = project_id
        self._name = name
        self._cluster_type = cluster_type
        self._cloud_provider = cloud_provider
        self._region = region
        self._create_timestamp = create_timestamp
        self._config = config
        self._status = status

    def assign_object(self, obj: dict):
        self._id = obj["id"]
        self._project_id = obj["project_id"]
        self._name = obj["name"]
        self._cluster_type = obj["cluster_type"]
        self._cloud_provider = obj["cloud_provider"]
        self._region = obj["region"]
        self._create_timestamp = int(obj["create_timestamp"])
        self._config = ClusterConfig.from_object(obj["config"])
        self._status = ClusterInfo.from_object(obj["status"])

    @property
    def status(self):
        return self._status

    @property
    def connection_strings(self):
        return self.status.connection_strings

    @classmethod
    def from_object(cls, context: Context, obj: dict):
        new_cluster = cls(context, _from="object")
        new_cluster.assign_object(obj)
        return new_cluster

    def to_object(self) -> dict:
        return {
            "id": self._id,
            "project_id": self._project_id,
            "name": self._name,
            "cluster_type": self._cluster_type,
            "cloud_provider": self._cloud_provider,
            "region": self._region,
            "create_timestamp": self._create_timestamp,
            "config": self._config.to_object(),
            "status": self._status.to_object()
        }

    def _update_info_from_server(self):
        path = "projects/{}/clusters/{}".format(self._project_id, self._id)
        resp = self._context.call_get(path=path)
        self.assign_object(resp)

    def wait_for_ready(self, *, timeout_sec: int = None, interval_sec: int = 10) -> bool:
        """
        Wait for cluster to be ready.
        Args:
            timeout_sec: timeout in seconds.
            interval_sec: interval in seconds.

        Returns:
            True if cluster is ready, False if timeout.

        Examples:
            ```python
            import tidbcloudy
            from tidbcloudy.specification import CreateClusterConfig
            api = tidbcloudy.TiDBCloud(public_key="your_public_key", private_key="your_private_key")
            project = api.get_project(project_id)
            cluster_config = CreateClusterConfig()
            cluster_config.set_name("your_cluster_name").set_cluster_type("your_cluster_type").set_cloud_provider("your_cloud_provider").set_region("your_region").set_port(4000).set_root_password("your_root_password")
            cluster = project.create_cluster(cluster_config)
            cluster.wait_for_ready()
        """
        create_start = time.monotonic()
        counter = 1
        while True:
            duration = time.monotonic() - create_start
            minutes = duration - 60 * counter
            if timeout_sec is not None and duration > timeout_sec:
                return False
            elif minutes > 0:
                counter += 1
                log("Waiting for cluster {} to be ready, {} seconds passed...".format(self._id, int(duration)))
            self._update_info_from_server()
            if self._status.cluster_status == ClusterStatus.AVAILABLE:
                log("Cluster id={} is available".format(self._id))
                return True
            time.sleep(interval_sec)

    def update(self, config: Union[UpdateClusterConfig, dict], update_from_server: bool = False):
        path = "projects/{}/clusters/{}".format(self._project_id, self._id)
        if isinstance(config, UpdateClusterConfig):
            config = config.to_object()
        self._context.call_patch(path=path, json=config)
        log("Cluster id={} has been updated".format(self._id))
        if update_from_server:
            self._update_info_from_server()

    def delete(self):
        path = "projects/{}/clusters/{}".format(self._project_id, self._id)
        self._context.call_delete(path=path)
        log("Cluster id={} has been deleted".format(self._id))

    def create_backup(self, *, name: str, description: str = None) -> Backup:
        """
        Create a backup of the cluster.
        Args:
            name: the name of the backup task.
            description: the description of the backup task.

        Returns:
            Backup instance.

        """
        path = "projects/{}/clusters/{}/backups".format(self._project_id, self._id)
        config = {
            "name": name
        }
        if description is not None:
            config["description"] = description
        resp = self._context.call_post(path=path, json=config)
        return self.get_backup(resp["id"])

    def delete_backup(self, backup_id: str):
        """
        Delete a backup of the cluster.
        Args:
            backup_id: the id of the backup task you want to delete.

        Returns:
            The response of the API.

        """
        Backup(self._context, backup_id, cluster_id=self._id, project_id=self._project_id).delete()

    def iter_backups(self, *, page_size: int = 10) -> Iterator[Backup]:
        """
        This is not a TiDB Cloud official endpoint.
        Iterate all backups of the cluster.
        Args:
            page_size: the page size of the response.

        Returns:
            Backup instance.

        """
        page = 1
        total = None
        while total is None or (page - 1) * page_size < total:
            backups = self.list_backups(page=page, page_size=page_size)
            total = backups.total
            for backup in backups.items:
                yield backup
            page += 1

    def list_backups(self, *, page: int = None, page_size: int = None) -> Page[Backup]:
        """
        List all backups of the cluster.
        Args:
            page: the page of the response.
            page_size: the page size of each page.

        Returns:
            The response of the API.

        """
        path = "projects/{}/clusters/{}/backups".format(self._project_id, self._id)
        query = {}
        if page is not None:
            query["page"] = page
        if page_size is not None:
            query["page_size"] = page_size
        resp = self._context.call_get(path=path, params=query)
        return Page(
            [Backup.from_object(
                self._context, {"cluster_id": self._id, "project_id": self._project_id, **backup}
            ) for backup in resp["items"]],
            page, page_size, resp["total"]
        )

    def get_backup(self, backup_id: str) -> Backup:
        """
        Get a backup of the cluster.
        Args:
            backup_id: the id of the backup task you want to get.

        Returns:
            Backup instance.

        """
        path = "projects/{}/clusters/{}/backups/{}".format(self._project_id, self._id, backup_id)
        resp = self._context.call_get(path=path)
        return Backup.from_object(self._context, {"cluster_id": self._id, "project_id": self._project_id, **resp})

    def connect(self, type: str, database: str, password: str):
        connection_strings = self.status.connection_strings.to_object()
        user = connection_strings["default_user"]
        if connection_strings is None:
            raise ValueError("No connection strings found for type {}".format(type))
        connection_string = connection_strings[type]
        return MySQLdb.connect(host=connection_string["host"],
                               port=connection_string["port"],
                               user=user, password=password,
                               database=database)

    def __repr__(self):
        if self._status == ClusterStatus.CREATING.value:
            return "<Cluster id={} creating>".format(self._id)
        else:
            return "<Cluster id={} name={} type={} create_at={}>".format(
                self._id, self._name, self._cluster_type,
                timestamp_to_string(self._create_timestamp))

    @property
    def id(self):
        return self._id
