from ._base import TiDBCloudyBase, TiDBCloudyContextualBase, TiDBCloudyField
from .specification import BackupType, BackupStatus
from .util.log import log


# noinspection PyShadowingBuiltins
class Backup(TiDBCloudyBase, TiDBCloudyContextualBase):
    __slots__ = ["_id", "_cluster_id", "_project_id", "_name", "_description", "_type", "_create_timestamp", "_size",
                 "_status"]

    id: str = TiDBCloudyField(str)
    cluster_id: str = TiDBCloudyField(str)
    project_id: str = TiDBCloudyField(str)
    name: str = TiDBCloudyField(str)
    description: str = TiDBCloudyField(str)
    type: BackupType = TiDBCloudyField(BackupType)
    create_timestamp: str = TiDBCloudyField(str)
    size: str = TiDBCloudyField(str)
    status: BackupStatus = TiDBCloudyField(BackupStatus)

    """
    Args:
        id: the id of the backup
        cluster_id: the id of the cluster
        name: the name of the backup
        description: the description of the backup
        type: the type of the backup
        create_timestamp: the created timestamp of the backup
        size: the size of the backup
        status: the status of the backup
        _from: internal use only
    """

    def delete(self):
        path = "projects/{}/clusters/{}/backups/{}".format(self.project_id, self.cluster_id, self.id)
        self.context.call_delete(path=path)
        log("backup task id={} has been deleted".format(self.id))

    def __repr__(self):
        return "<backup id={} name={} create_at= {}>".format(self.id, self.name, self.create_timestamp)
