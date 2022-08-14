from tidbcloudy.specification import RestoreStatus, ClusterInfoOfRestore
from tidbcloudy.context import Context


# noinspection PyShadowingBuiltins
class Restore:
    def __init__(self,
                 context: Context,
                 id: str = None,
                 *,
                 create_timestamp: str = None,
                 backup_id: str = None,
                 cluster_id: str = None,
                 cluster: ClusterInfoOfRestore = None,
                 status: RestoreStatus = None,
                 error_message: str = None,
                 _from: str = None):
        self._context = context
        self._from = _from
        if self._from is None:
            if id is None:
                raise TypeError("id")
        elif self._from == "object":
            pass
        elif self._from == "create":
            if id is None:
                raise TypeError("id")
            if cluster_id is None:
                raise TypeError("cluster_id")
        else:
            raise ValueError("_from")
        self._id = id
        self._create_timestamp = create_timestamp
        self._backup_id = backup_id
        self._cluster_id = cluster_id
        self._cluster = cluster
        self._status = status
        self._error_message = error_message

    def assign_object(self, obj: dict):
        self._id = obj["id"]
        self._create_timestamp = obj["create_timestamp"]
        self._backup_id = obj["backup_id"]
        self._cluster_id = obj["cluster_id"]
        self._cluster = ClusterInfoOfRestore(
            id=obj["cluster"]["id"],
            name=obj["cluster"]["name"],
            status=obj["cluster"]["status"])
        self._status = obj["status"]
        self._error_message = obj["error_message"]

    @classmethod
    def from_object(cls, context: Context, obj: dict):
        new_restore = cls(
            context=context,
            _from="object"
        )
        new_restore.assign_object(obj)
        return new_restore

    def __repr__(self):
        return "<restore id={} backup_id={} create_at= {} status={}>".format(self._id, self._backup_id,
                                                                             self._create_timestamp, self._status)
