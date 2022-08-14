from tidbcloudy.specification import BackupType, BackupStatus
from tidbcloudy.context import Context
from tidbcloudy.util.log import log


# noinspection PyShadowingBuiltins
class Backup:
    def __init__(self,
                 context: Context,
                 id: str = None,
                 *,
                 cluster_id: str = None,
                 project_id: str = None,
                 name: str = None,
                 description: str = None,
                 type: BackupType = None,
                 create_timestamp: str = None,
                 size: str = None,
                 status: BackupStatus = None,
                 _from: str = None
                 ):
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
        self._context = context
        self._from = _from
        if self._from is None:
            if id is None:
                raise TypeError("id")
            if cluster_id is None:
                raise TypeError("cluster_id")
        elif self._from == "create":
            # When init a backup instance from create_backup endpoint, the id and cluster_id is required
            if id is None:
                raise TypeError("id")
            if cluster_id is None:
                raise TypeError("cluster_id")
        elif self._from == "object":
            pass
        else:
            raise ValueError("_from")
        self._id = id
        self._cluster_id = cluster_id
        self._project_id = project_id
        self._name = name
        self._description = description
        self._type = type
        self._create_timestamp = create_timestamp
        self._size = size
        self._status = status

    def assign_object(self, obj: dict):
        self._id = obj["id"]
        self._cluster_id = obj["cluster_id"]
        self._project_id = obj["project_id"]
        self._name = obj["name"]
        self._description = obj["description"]
        self._type = obj["type"]
        self._create_timestamp = obj["create_timestamp"]
        self._size = obj["size"]
        self._status = obj["status"]

    @classmethod
    def from_object(cls, context: Context, obj: dict):
        new_backup = cls(
            context=context,
            _from="object"
        )
        new_backup.assign_object(obj)
        return new_backup

    def delete(self):
        path = "projects/{}/clusters/{}/backups/{}".format(self._project_id, self._cluster_id, self._id)
        self._context.call_delete(path=path)
        log("backup task id={} has been deleted".format(self._id))

    def __repr__(self):
        return "<backup id={} name={} create_at= {}>".format(self._id, self._name, self._create_timestamp)
