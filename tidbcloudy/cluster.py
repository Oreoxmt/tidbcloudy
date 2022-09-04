import time
import deprecation
import MySQLdb
from typing import Union, Iterator

from ._base import TiDBCloudyBase, TiDBCloudyContextualBase, TiDBCloudyField
from .specification import ClusterType, CloudProvider, ClusterConfig, ClusterInfo, UpdateClusterConfig, \
    ClusterStatus
from .backup import Backup
from .util.log import log
from .util.timestamp import timestamp_to_string
from .util.page import Page


# noinspection PyShadowingBuiltins
class Cluster(TiDBCloudyBase, TiDBCloudyContextualBase):
    __slots__ = ["_id", "_project_id", "_name", "_cluster_type", "_cloud_provider", "_region", "_create_timestamp",
                 "_config", "_status"]

    id: str = TiDBCloudyField(str)
    project_id: str = TiDBCloudyField(str)
    name: str = TiDBCloudyField(str)
    cluster_type: ClusterType = TiDBCloudyField(ClusterType)
    cloud_provider: CloudProvider = TiDBCloudyField(CloudProvider)
    region: str = TiDBCloudyField(str)
    create_timestamp: int = TiDBCloudyField(int, convert_from=int, convert_to=str)
    config: ClusterConfig = TiDBCloudyField(ClusterConfig)
    status: ClusterInfo = TiDBCloudyField(ClusterInfo)

    def _update_info_from_server(self):
        path = "projects/{}/clusters/{}".format(self.project_id, self.id)
        resp = self.context.call_get(path=path)
        self.assign_object(resp)

    def wait_for_available(self, *, timeout_sec: int = None, interval_sec: int = 10) -> bool:
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
        time_start = time.monotonic()
        counter = 1
        log("Cluster id={} is {}".format(self.id, self.status.cluster_status.value))
        while True:
            duration = time.monotonic() - time_start
            minutes = duration - 60 * counter
            if timeout_sec is not None and duration > timeout_sec:
                return False
            elif minutes > 0:
                counter += 1
                log("Waiting for cluster {} to be ready, {} seconds passed...".format(self.id, int(duration)))
            self._update_info_from_server()
            if self.status.cluster_status == ClusterStatus.AVAILABLE:
                log("Cluster id={} is {}".format(self.id, self.status.cluster_status.value))
                return True
            time.sleep(interval_sec)

    @deprecation.deprecated(details="Use wait_for_available instead")
    def wait_for_ready(self, *, timeout_sec: int = None, interval_sec: int = 10) -> bool:
        return self.wait_for_available(timeout_sec=timeout_sec, interval_sec=interval_sec)

    def update(self, config: Union[UpdateClusterConfig, dict], update_from_server: bool = False):
        path = "projects/{}/clusters/{}".format(self.project_id, self.id)
        if isinstance(config, UpdateClusterConfig):
            config = config.to_object()
        self.context.call_patch(path=path, json=config)
        log("Cluster id={} has been updated".format(self.id))
        if update_from_server:
            self._update_info_from_server()

    def pause(self):
        path = "projects/{}/clusters/{}".format(self.project_id, self.id)
        config = {
            "config": {
                "paused": True
            }
        }
        self.context.call_patch(path=path, json=config)
        self._update_info_from_server()
        log("Cluster id={} status={}".format(self.id, self.status.cluster_status.value))

    def resume(self):
        path = "projects/{}/clusters/{}".format(self.project_id, self.id)
        config = {
            "config": {
                "paused": False
            }
        }
        self.context.call_patch(path=path, json=config)
        self._update_info_from_server()
        log("Cluster id={} status={}".format(self.id, self.status.cluster_status.value))

    def delete(self):
        path = "projects/{}/clusters/{}".format(self.project_id, self.id)
        self.context.call_delete(path=path)
        log("Cluster id={} has been deleted".format(self.id))

    def create_backup(self, *, name: str, description: str = None) -> Backup:
        """
        Create a backup of the cluster.
        Args:
            name: the name of the backup task.
            description: the description of the backup task.

        Returns:
            Backup instance.

        """
        path = "projects/{}/clusters/{}/backups".format(self.project_id, self.id)
        config = {
            "name": name
        }
        if description is not None:
            config["description"] = description
        resp = self.context.call_post(path=path, json=config)
        return self.get_backup(resp["id"])

    def delete_backup(self, backup_id: str):
        """
        Delete a backup of the cluster.
        Args:
            backup_id: the id of the backup task you want to delete.

        Returns:
            The response of the API.

        """
        Backup(context=self.context, backup_id=backup_id, cluster_id=self.id, project_id=self.project_id).delete()

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
        path = "projects/{}/clusters/{}/backups".format(self.project_id, self.id)
        query = {}
        if page is not None:
            query["page"] = page
        if page_size is not None:
            query["page_size"] = page_size
        resp = self.context.call_get(path=path, params=query)
        return Page(
            [Backup.from_object(
                self.context, {"cluster_id": self.id, "project_id": self.project_id, **backup}
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
        path = "projects/{}/clusters/{}/backups/{}".format(self.project_id, self.id, backup_id)
        resp = self.context.call_get(path=path)
        return Backup.from_object(self.context, {"cluster_id": self.id, "project_id": self.project_id, **resp})

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
        if self.status.cluster_status == ClusterStatus.CREATING.value:
            return "<Cluster id={} CREATING>".format(self.id)
        elif self.cluster_type is None:
            return "<Cluster id={} name={}>".format(self.id, self.name)
        else:
            return "<Cluster id={} name={} type={} create_at={}>".format(
                self.id, self.name, self.cluster_type.value,
                timestamp_to_string(self.create_timestamp))
