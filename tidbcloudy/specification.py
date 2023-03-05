from enum import Enum
from typing import Union, List

from ._base import TiDBCloudyBase, TiDBCloudyField, TiDBCloudyListField
from .util.ip import get_current_ip_address


class ClusterType(Enum):
    DEVELOPER = "DEVELOPER"
    DEDICATED = "DEDICATED"


class CloudProvider(Enum):
    AWS = "AWS"
    GCP = "GCP"


class ClusterStatus(Enum):
    INITIALIZING = "INITIALIZING"
    AVAILABLE = "AVAILABLE"
    CREATING = "CREATING"
    MODIFYING = "MODIFYING"
    PAUSED = "PAUSED"
    RESUMING = "RESUMING"
    UNAVAILABLE = "UNAVAILABLE"
    IMPORTING = "IMPORTING"
    CLEARED = "CLEARED"


class NodeStatus(Enum):
    NODE_STATUS_AVAILABLE = "NODE_STATUS_AVAILABLE"
    NODE_STATUS_UNAVAILABLE = "NODE_STATUS_UNAVAILABLE"
    NODE_STATUS_CREATING = "NODE_STATUS_CREATING"
    NODE_STATUS_DELETING = "NODE_STATUS_DELETING"


class BackupType(Enum):
    MANUAL = "MANUAL"
    AUTO = "AUTO"


class BackupStatus(Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    FAILED = "FAILED"
    SUCCESS = "SUCCESS"


class RestoreStatus(Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    FAILED = "FAILED"
    SUCCESS = "SUCCESS"

class ImportStatusPhase(Enum):
    PREPARING = "PREPARING"
    IMPORTING = "IMPORTING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELING = "CANCELING"
    CANCELED = "CANCELED"

class ImportSourceType(Enum):
    S3 = "S3"
    GCS = "GCS"
    LOCAL_FILE = "LOCAL_FILE"

class ImportSourceType(Enum):
    CSV = "CSV"
    PARQUET = "PARQUET"
    SQL = "SQL"
    AURORA_SNAPSHOT = "AURORA_SNAPSHOT"


# noinspection PyShadowingBuiltins
class NodeQuantityRange(TiDBCloudyBase):
    __slots__ = ["_min", "_step"]
    min: int = TiDBCloudyField(int)
    step: int = TiDBCloudyField(int)


# noinspection PyShadowingBuiltins
class StorageSizeGibRange(TiDBCloudyBase):
    __slots__ = ["_min", "_max"]
    min: int = TiDBCloudyField(int)
    max: int = TiDBCloudyField(int)


class TiDBProfile(TiDBCloudyBase):
    __slots__ = ["_node_size", "_node_quantity_range"]
    node_size: str = TiDBCloudyField(str)
    node_quantity_range: NodeQuantityRange = TiDBCloudyField(NodeQuantityRange)

    def __repr__(self):
        return "<TiDB {}>".format(self.node_size)


class TiKVProfile(TiDBCloudyBase):
    __slots__ = ["_node_size", "_node_quantity_range", "_storage_size_gib_range"]
    node_size: str = TiDBCloudyField(str)
    node_quantity_range: NodeQuantityRange = TiDBCloudyField(NodeQuantityRange)
    storage_size_gib_range: StorageSizeGibRange = TiDBCloudyField(StorageSizeGibRange)

    def __repr__(self):
        return "<TiKV {}>".format(self.node_size)


class TiFlashProfile(TiDBCloudyBase):
    __slots__ = ["_node_size", "_node_quantity_range", "_storage_size_gib_range"]
    node_size: str = TiDBCloudyField(str)
    node_quantity_range: NodeQuantityRange = TiDBCloudyField(NodeQuantityRange)
    storage_size_gib_range: StorageSizeGibRange = TiDBCloudyField(StorageSizeGibRange)

    def __repr__(self):
        return "<TiFlash {}>".format(self.node_size)


class ConnectionString(TiDBCloudyBase):
    __slots__ = ["_host", "_port"]
    host: str = TiDBCloudyField(str)
    port: int = TiDBCloudyField(int)


class ConnectionStrings(TiDBCloudyBase):
    __slots__ = ["_default_user", "_standard", "_vpc_peering"]
    default_user: str = TiDBCloudyField(str)
    standard: ConnectionString = TiDBCloudyField(ConnectionString)
    vpc_peering: ConnectionString = TiDBCloudyField(ConnectionString)


class TiDBNodeMap(TiDBCloudyBase):
    __slots__ = ["_node_name", "_availability_zone", "_node_size", "_vcpu_num", "_ram_bytes", "_status"]
    node_name: str = TiDBCloudyField(str)
    availability_zone: str = TiDBCloudyField(str)
    node_size: str = TiDBCloudyField(str)
    vcpu_num: int = TiDBCloudyField(int)
    ram_bytes: int = TiDBCloudyField(int)
    status: NodeStatus = TiDBCloudyField(NodeStatus)


class TiKVNodeMap(TiDBCloudyBase):
    __slots__ = [
        "_node_name", "_availability_zone", "_node_size", "_vcpu_num", "_ram_bytes", "_storage_size_gib", "_status"]

    node_name: str = TiDBCloudyField(str)
    availability_zone: str = TiDBCloudyField(str)
    node_size: str = TiDBCloudyField(str)
    vcpu_num: int = TiDBCloudyField(int)
    ram_bytes: int = TiDBCloudyField(int)
    storage_size_gib: int = TiDBCloudyField(int)
    status: NodeStatus = TiDBCloudyField(NodeStatus)


class TiFlashNodeMap(TiDBCloudyBase):
    __slots__ = ["_node_name", "_availability_zone", "_node_size", "_vcpu_num", "_ram_bytes", "_storage_size_gib",
                 "_status", ]

    node_name: str = TiDBCloudyField(str)
    availability_zone: str = TiDBCloudyField(str)
    node_size: str = TiDBCloudyField(str)
    vcpu_num: int = TiDBCloudyField(int)
    ram_bytes: int = TiDBCloudyField(int)
    storage_size_gib: int = TiDBCloudyField(int)
    status: NodeStatus = TiDBCloudyField(NodeStatus)


class NodeMapSpec(TiDBCloudyBase):
    __slots__ = ["_tidb", "_tikv", "_tiflash"]
    tidb: List[TiDBNodeMap] = TiDBCloudyListField(TiDBNodeMap)
    tikv: List[TiKVNodeMap] = TiDBCloudyListField(TiKVNodeMap)
    tiflash: List[TiFlashNodeMap] = TiDBCloudyListField(TiFlashNodeMap)


class IPAccessList(TiDBCloudyBase):
    __slots__ = ["_cidr", "_description"]
    cidr: str = TiDBCloudyField(str)
    description: str = TiDBCloudyField(str)


class TiDBComponent(TiDBCloudyBase):
    __slots__ = ["_node_size", "_node_quantity"]
    node_size: str = TiDBCloudyField(str)
    node_quantity: int = TiDBCloudyField(int)


class TiKVComponent(TiDBCloudyBase):
    __slots__ = ["_node_size", "_node_quantity", "_storage_size_gib"]
    node_size: str = TiDBCloudyField(str)
    node_quantity: int = TiDBCloudyField(int)
    storage_size_gib: int = TiDBCloudyField(int)


class TiFlashComponent(TiDBCloudyBase):
    __slots__ = ["_node_size", "_node_quantity", "_storage_size_gib"]
    node_size: str = TiDBCloudyField(str)
    node_quantity: int = TiDBCloudyField(int)
    storage_size_gib: int = TiDBCloudyField(int)


class ClusterComponents(TiDBCloudyBase):
    __slots__ = ["_tidb", "_tikv", "_tiflash"]
    tidb: TiDBComponent = TiDBCloudyField(TiDBComponent)
    tikv: TiKVComponent = TiDBCloudyField(TiKVComponent)
    tiflash: TiFlashComponent = TiDBCloudyField(TiFlashComponent)


class ClusterConfig(TiDBCloudyBase):
    __slots__ = ["_root_password", "_port", "_components", "_ip_access_list"]
    root_password: str = TiDBCloudyField(str)
    port: int = TiDBCloudyField(int)
    components: ClusterComponents = TiDBCloudyField(ClusterComponents)
    ip_access_list: List[IPAccessList] = TiDBCloudyListField(IPAccessList)

    def __repr__(self):
        return "<ClusterConfig port={} components={}>".format(self.port, self.components)


class CreateClusterConfig:
    def __init__(self):
        self._name = None
        self._cluster_type = None
        self._cloud_provider = None
        self._region = None
        self._root_password = None
        self._port = None
        self._components = None
        self._tidb = None
        self._tikv = None
        self._tiflash = None
        self._ip_access_list = []

    def set_name(self, name: str):
        self._name = name
        return self

    def set_cluster_type(self, cluster_type: Union[ClusterType, str]):
        if isinstance(cluster_type, ClusterType):
            self._cluster_type = cluster_type.value
        else:
            self._cluster_type = cluster_type.upper()
        return self

    def set_cloud_provider(self, cloud_provider: Union[CloudProvider, str]):
        if isinstance(cloud_provider, CloudProvider):
            self._cloud_provider = cloud_provider.value
        else:
            self._cloud_provider = cloud_provider.upper()
        return self

    def set_region(self, region: str):
        self._region = region
        return self

    def set_root_password(self, root_password: str):
        self._root_password = root_password
        return self

    def set_port(self, port: int):
        self._port = port
        return self

    def set_component(self, component: str, node_size: str, node_quantity: int, storage_size_gib: int = None):
        component = component.lower()
        if component == "tidb":
            self._tidb = TiDBComponent(node_size=node_size, node_quantity=node_quantity)
        elif component == "tikv":
            self._tikv = TiKVComponent(node_size=node_size, node_quantity=node_quantity,
                                       storage_size_gib=storage_size_gib)
        elif component == "tiflash":
            self._tiflash = TiFlashComponent(node_size=node_size, node_quantity=node_quantity,
                                             storage_size_gib=storage_size_gib)
        else:
            raise Exception("Invalid component, only tidb, tikv, tiflash are supported")
        return self

    def add_ip_access(self, cidr: str, description: str = ""):
        self._ip_access_list.append(IPAccessList(cidr=cidr, description=description))
        return self

    def add_current_ip_access(self, description: str = "Current IP automatically generated by tidbcloudy"):
        self.add_ip_access(cidr=get_current_ip_address() + "/32", description=description)
        return self

    def to_object(self) -> dict:
        return {
            "name": self._name if self._name is not None else "",
            "cluster_type": self._cluster_type,
            "cloud_provider": self._cloud_provider,
            "region": self._region,
            "config": {
                "root_password": self._root_password,
                "port": self._port,
                "components": {
                    "tidb": {
                        "node_size": self._tidb.node_size,
                        "node_quantity": self._tidb.node_quantity
                    } if self._tidb is not None else None,
                    "tikv": {
                        "node_size": self._tikv.node_size,
                        "node_quantity": self._tikv.node_quantity,
                        "storage_size_gib": self._tikv.storage_size_gib
                    } if self._tikv is not None else None,
                    "tiflash": {
                        "node_size": self._tiflash.node_size,
                        "node_quantity": self._tiflash.node_quantity,
                        "storage_size_gib": self._tiflash.storage_size_gib
                    } if self._tiflash is not None else None
                },
                "ip_access_list": [
                    item.to_object() for item in self._ip_access_list] if self._ip_access_list is not None else None
            }
        }

class CreateImportSpec:
    def __init__(self):
        self._name = None
        self._source_type = None
        self._source_uri = None
        self._aws_assume_role = None
        self._source_aws_key_access = None
        self._source_format = None
        self._target_table = []
        self._pre_created_tables = []
        self._pre_created_columns = []
        self._pre_created_primary_keys = []
    def set_name(self, name:str):
        self._name = name
        return self
    def set_source(self, type:ImportSourceType, uri:str, format_type: ImportSourceType):
        self._source_type = type
        self._source_uri = uri
        self._source_format = {
            "type": format_type
        }
        return self
    def set_aws_access_role(self, aws_assume_role: str):
        self._aws_assume_role = aws_assume_role
        return self

    def set_csv_config(self, delimiter:str = ",", quote:str = "\"", backslash_escape:bool = True, has_header_row:bool = True):
        self._delimiter = delimiter
        self._quote = quote
        self._backslash_escape = backslash_escape
        self._has_header_row = has_header_row
        return self
    def set_aws_key(self, access_key_id: str, secret_access_key: str):
        self._source_aws_key_access = {
            "access_key_id": access_key_id,
            "secret_access_key": secret_access_key
        }
        return self

    def set_target_tables(self, database_name:str, table_name:str, file_name_pattern:str = ""):
        table = {
            "database_name": database_name,
            "table_name": table_name,
            "file_name_pattern": file_name_pattern
        }
        self._target_table.append(table)
        return self

    def add_pre_created_table(self, database_name:str, table_name:str, pre_created_schema:list):
        table = {
            "database_name": database_name,
            "table_name": table_name,
            "schema":{
                pre_created_schema
            }
        }
        self._pre_created_tables.append(table)
        return self
    def add_pre_created_column(self, column_name:str, column_type:str):
        self._column_name = column_name
        self._column_type = column_type
        column = {
            "column_name": column_name,
            "column_type": column_type
        }
        self._pre_created_columns.append(column)
        return self
    def add_pre_created_primary_key(self, primary_key_columns: str):
        self._pre_created_primary_keys.append(primary_key_columns)
        return self

class UpdateClusterConfig:
    def __init__(self):
        self._tidb = None
        self._tikv = None
        self._tiflash = None

    def update_component(self, component: str, node_quantity: int = None, node_size: str = None,
                         storage_size_gib: int = None):
        if component == "tidb" and node_quantity is not None:
            self._tidb = TiDBComponent(node_size=node_size, node_quantity=node_quantity)
        elif component == "tikv" and node_quantity is not None:
            self._tikv = TiKVComponent(node_size=node_size, node_quantity=node_quantity,
                                       storage_size_gib=storage_size_gib)
        elif component == "tiflash" and node_quantity is not None:
            self._tiflash = TiFlashComponent(node_size=node_size, node_quantity=node_quantity,
                                             storage_size_gib=storage_size_gib)
        else:
            raise Exception("Invalid component, only tidb, tikv, tiflash are supported")
        return self

    def to_object(self) -> dict:
        components = {}
        if self._tidb is not None:
            components["tidb"] = {}
            if self._tidb.node_size is not None:
                components["tidb"]["node_size"] = self._tidb.node_size
            if self._tidb.node_quantity is not None:
                components["tidb"]["node_quantity"] = self._tidb.node_quantity
        if self._tikv is not None:
            components["tikv"] = {}
            if self._tikv.node_size is not None:
                components["tikv"]["node_size"] = self._tikv.node_size
            if self._tikv.node_quantity is not None:
                components["tikv"]["node_quantity"] = self._tikv.node_quantity
            if self._tikv.storage_size_gib is not None:
                components["tikv"]["storage_size_gib"] = self._tikv.storage_size_gib
        if self._tiflash is not None:
            components["tiflash"] = {}
            if self._tiflash.node_size is not None:
                components["tiflash"]["node_size"] = self._tiflash.node_size
            if self._tiflash.node_quantity is not None:
                components["tiflash"]["node_quantity"] = self._tiflash.node_quantity
            if self._tiflash.storage_size_gib is not None:
                components["tiflash"]["storage_size_gib"] = self._tiflash.storage_size_gib

        return {
            "config": {
                "components": components
            }
        }


class ClusterInfo(TiDBCloudyBase):
    __slots__ = ["_tidb_version", "_cluster_status", "_node_map", "_connection_strings"]
    tidb_version: str = TiDBCloudyField(str)
    cluster_status: ClusterStatus = TiDBCloudyField(ClusterStatus)
    node_map: NodeMapSpec = TiDBCloudyField(NodeMapSpec)
    connection_strings: ConnectionStrings = TiDBCloudyField(ConnectionStrings)

    def __repr__(self):
        return "<tidb={} status= {} default user={}>".format(
            self.tidb_version,
            self.cluster_status.value if self.cluster_status is not None else None,
            self.connection_strings.default_user)


# noinspection PyShadowingBuiltins
class ClusterInfoOfRestore(TiDBCloudyBase):
    __slots__ = ["_id", "_name", "_status", ]
    id: str = TiDBCloudyField(str)
    name: str = TiDBCloudyField(str)
    status: ClusterStatus = TiDBCloudyField(ClusterStatus)

    def __repr__(self):
        return "<id={}, name={}, status={}>".format(self.id, self.name,
                                                    self.status.value if self.status is not None else None)


class CloudSpecification(TiDBCloudyBase):
    __slots__ = ["_cluster_type", "_cloud_provider", "_region", "_tidb", "_tikv", "_tiflash"]
    cluster_type: ClusterType = TiDBCloudyField(ClusterType)
    cloud_provider: CloudProvider = TiDBCloudyField(CloudProvider)
    region: str = TiDBCloudyField(str)
    tidb: List[TiDBProfile] = TiDBCloudyListField(TiDBProfile)
    tikv: List[TiKVProfile] = TiDBCloudyListField(TiKVProfile)
    tiflash: List[TiFlashProfile] = TiDBCloudyListField(TiFlashProfile)

    def __repr__(self):
        return "<Specification cluster_type={} cloud_provider={} region={}>".format(
            self.cluster_type.value if self.cluster_type is not None else None,
            self.cloud_provider.value if self.cloud_provider is not None else None,
            self.region)

class ImportMetadta(TiDBCloudyBase):
    __slots__ = ["_id", "_name", "_create_timestamp", ]
    id: str = TiDBCloudyField(str)
    name: str = TiDBCloudyField(str)
    create_timestamp: str = TiDBCloudyField(str)

    def __repr__(self):
        return "<id={}, name={}, create_timestamp={}>".format(self.id, self.name, self.create_timestamp)


class AWSAssumeRole(TiDBCloudyBase):
    assume_role: str = TiDBCloudyField(str)

class AWSAccessKey(TiDBCloudyBase):
    access_key_id: str = TiDBCloudyField(str)
    secret_access_key: str = TiDBCloudyField(str)


class ImportSourceCSV(TiDBCloudyBase):
    delimiter: str = TiDBCloudyField(str)
    quote: str = TiDBCloudyField(str)
    backslash_escape: bool = TiDBCloudyField(bool)
    has_header_row: bool = TiDBCloudyField(bool)

class ImportSourceFormat(TiDBCloudyBase):
    type: ImportSourceType = TiDBCloudyField(ImportSourceType)
    csv_config: ImportSourceCSV = TiDBCloudyField(ImportSourceCSV)

class ImportSource(TiDBCloudyBase):
    type: ImportSourceType = TiDBCloudyField(ImportSourceType)
    uri: str = TiDBCloudyField(str)
    aws_assume_role_access: AWSAssumeRole = TiDBCloudyField(AWSAssumeRole)
    aws_key_access: AWSAccessKey = TiDBCloudyField(AWSAccessKey)
    format: ImportSourceFormat = TiDBCloudyField(ImportSourceFormat)

class ImportTargettable(TiDBCloudyBase):
    database_name: str = TiDBCloudyField(str)
    table_name: str = TiDBCloudyField(str)
    file_name_pattern: str = TiDBCloudyField(str)

class ImportTarget(TiDBCloudyBase):
    tables: ImportTargettable = TiDBCloudyField(ImportTargettable)
class ImportSpec(TiDBCloudyBase):
    source: ImportSource = TiDBCloudyField(ImportSource)
    target: ImportTarget = TiDBCloudyField(ImportTarget)

class ImportProgress(TiDBCloudyBase):
    import_progress: int = TiDBCloudyField(int)
    validation_progress: int = TiDBCloudyField(int)

class ImportStatus(TiDBCloudyBase):
    phase: ImportStatusPhase = TiDBCloudyField(ImportStatusPhase)
    error_message: str = TiDBCloudyField(str)
    start_timestamp: str = TiDBCloudyField(str)
    end_timestamp: str = TiDBCloudyField(str)
    progress: ImportProgress = TiDBCloudyField(ImportProgress)
    source_total_size_bytes: str = TiDBCloudyField(str)