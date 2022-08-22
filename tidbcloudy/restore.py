from ._base import TiDBCloudyBase, TiDBCloudyContextualBase, TiDBCloudyField
from tidbcloudy.specification import RestoreStatus, ClusterInfoOfRestore


# noinspection PyShadowingBuiltins
class Restore(TiDBCloudyBase, TiDBCloudyContextualBase):
    __slots__ = ["_id", "_create_timestamp", "_backup_id", "_cluster_id", "_cluster", "_status", "_error_message"]
    id: str = TiDBCloudyField(str)
    create_timestamp: str = TiDBCloudyField(str)
    backup_id: str = TiDBCloudyField(str)
    cluster_id: str = TiDBCloudyField(str)
    cluster: ClusterInfoOfRestore = TiDBCloudyField(ClusterInfoOfRestore)
    status: RestoreStatus = TiDBCloudyField(RestoreStatus)
    error_message: str = TiDBCloudyField(str)

    def __repr__(self):
        return "<restore id={} backup_id={} create_at= {} status={}>".format(self._id, self._backup_id,
                                                                             self._create_timestamp, self._status)
