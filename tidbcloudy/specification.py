from enum import Enum
from tidbcloudy.util.ip import get_current_ip_address
from typing import Union


class ClusterType(Enum):
    DEVELOPER = "DEVELOPER"
    DEDICATED = "DEDICATED"


class CloudProvider(Enum):
    AWS = "AWS"
    GCP = "GCP"


class ClusterStatus(Enum):
    AVAILABLE = "AVAILABLE"
    CREATING = "CREATING"
    MODIFYING = "MODIFYING"
    PAUSED = "PAUSED"
    RESUMING = "RESUMING"
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


# noinspection PyShadowingBuiltins
class NodeQuantityRange:
    def __init__(self, min: int, step: int):
        self.min = min
        self.step = step


# noinspection PyShadowingBuiltins
class StorageSizeGibRange:
    def __init__(self, min: int, max: int):
        self.min = min
        self.max = max


class TiDBProfile:
    def __init__(self, node_size: str, node_quantity_range: NodeQuantityRange):
        self.node_size = node_size
        self.node_quantity_range = node_quantity_range

    @classmethod
    def from_object(cls, obj: dict):
        return cls(
            node_size=obj["node_size"],
            node_quantity_range=NodeQuantityRange(
                min=obj["node_quantity_range"]["min"],
                step=obj["node_quantity_range"]["step"]
            )
        )

    def to_object(self):
        return {
            "node_size": self.node_size,
            "node_quantity_range": {
                "min": self.node_quantity_range.min,
                "step": self.node_quantity_range.step
            }
        }

    def __repr__(self):
        return "<TiDB {}>".format(self.node_size)


class TiKVProfile:
    def __init__(self,
                 node_size: str,
                 node_quantity_range: NodeQuantityRange,
                 storage_size_gib_range: StorageSizeGibRange,
                 ):
        self.node_size = node_size
        self.node_quantity_range = node_quantity_range
        self.storage_size_gib_range = storage_size_gib_range

    @classmethod
    def from_object(cls, obj: dict):
        return cls(
            node_size=obj["node_size"],
            node_quantity_range=NodeQuantityRange(min=obj["node_quantity_range"]["min"],
                                                  step=obj["node_quantity_range"]["step"]),
            storage_size_gib_range=StorageSizeGibRange(min=obj["storage_size_gib_range"]["min"],
                                                       max=obj["storage_size_gib_range"]["max"]))

    def to_object(self):
        return {
            "node_size": self.node_size,
            "node_quantity_range": {
                "min": self.node_quantity_range.min,
                "step": self.node_quantity_range.step
            },
            "storage_size_gib_range": {
                "min": self.storage_size_gib_range.min,
                "max": self.storage_size_gib_range.max
            }
        }

    def __repr__(self):
        return "<TiKV {}>".format(self.node_size)


class TiFlashProfile:
    def __init__(self,
                 node_size: str,
                 node_quantity_range: NodeQuantityRange,
                 storage_size_gib_range: StorageSizeGibRange,
                 ):
        self.node_size = node_size
        self.node_quantity_range = node_quantity_range
        self.storage_size_gib_range = storage_size_gib_range

    @classmethod
    def from_object(cls, obj: dict):
        return cls(
            obj["node_size"],
            NodeQuantityRange(obj["node_quantity_range"]["min"], obj["node_quantity_range"]["step"]),
            StorageSizeGibRange(obj["storage_size_gib_range"]["min"], obj["storage_size_gib_range"]["max"]))

    def to_object(self):
        return {
            "node_size": self.node_size,
            "node_quantity_range": {
                "min": self.node_quantity_range.min,
                "step": self.node_quantity_range.step
            },
            "storage_size_gib_range": {
                "min": self.storage_size_gib_range.min,
                "max": self.storage_size_gib_range.max
            }
        }

    def __repr__(self):
        return "<TiFlash {}>".format(self.node_size)


class ConnectionString:
    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port


class ConnectionStrings:
    def __init__(self, default_user: str, standard: ConnectionString, vpc_peering: ConnectionString):
        self._default_user = default_user
        self._standard = standard
        self._vpc_peering = vpc_peering

    @property
    def default_user(self):
        return self._default_user

    @property
    def standard(self):
        return self._standard

    @property
    def vpc_peering(self):
        return self._vpc_peering

    @classmethod
    def from_object(cls, obj: dict):
        return cls(
            default_user=obj["default_user"],
            standard=ConnectionString(obj["standard"]["host"], obj["standard"]["port"]) if obj.get(
                "standard") else None,
            vpc_peering=ConnectionString(obj["vpc_peering"]["host"], obj["vpc_peering"]["port"]) if obj.get(
                "vpc_peering") else None
        )

    def to_object(self) -> dict:
        return {
            "default_user": self._default_user,
            "standard": {
                "host": self.standard.host,
                "port": self.standard.port
            },
            "vpc_peering": {
                "host": self.vpc_peering.host if self.vpc_peering else None,
                "port": self.vpc_peering.port if self.vpc_peering else None
            }
        }


class TiDBNodeMap:
    def __init__(self, node_name: str, availability_zone: str, node_size: str, vcpu_num: int, ram_bytes: int,
                 status: NodeStatus):
        self._node_name = node_name
        self._availability_zone = availability_zone
        self._node_size = node_size
        self._vcpu_num = vcpu_num
        self._ram_bytes = ram_bytes
        self._status = status

    @classmethod
    def from_object(cls, obj: dict):
        return cls(
            node_name=obj["node_name"],
            availability_zone=obj["availability_zone"],
            node_size=obj["node_size"],
            vcpu_num=obj["vcpu_num"],
            ram_bytes=obj["ram_bytes"],
            status=NodeStatus(obj["status"])
        )

    def to_object(self) -> dict:
        return {
            "node_name": self._node_name,
            "availability_zone": self._availability_zone,
            "node_size": self._node_size,
            "vcpu_num": self._vcpu_num,
            "ram_bytes": self._ram_bytes,
            "status": self._status.value
        }


class TiKVNodeMap:
    def __init__(self, node_name: str, availability_zone: str, node_size: str, vcpu_num: int, ram_bytes: int,
                 storage_size_gib: int, status: NodeStatus):
        self._node_name = node_name
        self._availability_zone = availability_zone
        self._node_size = node_size
        self._vcpu_num = vcpu_num
        self._ram_bytes = ram_bytes
        self._storage_size_gib = storage_size_gib
        self._status = status

    @classmethod
    def from_object(cls, obj: dict):
        return cls(
            node_name=obj["node_name"],
            availability_zone=obj["availability_zone"],
            node_size=obj["node_size"],
            vcpu_num=obj["vcpu_num"],
            ram_bytes=obj["ram_bytes"],
            storage_size_gib=obj["storage_size_gib"],
            status=NodeStatus(obj["status"])
        )

    def to_object(self) -> dict:
        return {
            "node_name": self._node_name,
            "availability_zone": self._availability_zone,
            "node_size": self._node_size,
            "vcpu_num": self._vcpu_num,
            "ram_bytes": self._ram_bytes,
            "storage_size_gib": self._storage_size_gib,
            "status": self._status.value
        }


class TiFlashNodeMap:
    def __init__(self, node_name: str, availability_zone: str, node_size: str, vcpu_num: int, ram_bytes: int,
                 storage_size_gib: int, status: NodeStatus):
        self._node_name = node_name
        self._availability_zone = availability_zone
        self._node_size = node_size
        self._vcpu_num = vcpu_num
        self._ram_bytes = ram_bytes
        self._storage_size_gib = storage_size_gib
        self._status = status

    @classmethod
    def from_object(cls, obj: dict):
        return cls(
            node_name=obj["node_name"],
            availability_zone=obj["availability_zone"],
            node_size=obj["node_size"],
            vcpu_num=obj["vcpu_num"],
            ram_bytes=obj["ram_bytes"],
            storage_size_gib=obj["storage_size_gib"],
            status=NodeStatus(obj["status"])
        )

    def to_object(self) -> dict:
        return {
            "node_name": self._node_name,
            "availability_zone": self._availability_zone,
            "node_size": self._node_size,
            "vcpu_num": self._vcpu_num,
            "ram_bytes": self._ram_bytes,
            "storage_size_gib": self._storage_size_gib,
            "status": self._status.value
        }


class NodeMapSpec:
    def __init__(self, tidb: [TiDBNodeMap], tikv: [TiKVNodeMap], tiflash: [TiFlashNodeMap]):
        self._tidb = tidb
        self._tikv = tikv
        self._tiflash = tiflash

    @classmethod
    def from_object(cls, obj: dict):
        return cls(
            tidb=[TiDBNodeMap.from_object(item) for item in obj["tidb"]],
            tikv=[TiKVNodeMap.from_object(item) for item in obj["tikv"]],
            tiflash=[TiFlashNodeMap.from_object(item) for item in obj["tiflash"]]
        )

    def to_object(self) -> dict:
        return {
            "tidb": [item.to_object() for item in self._tidb],
            "tikv": [item.to_object() for item in self._tikv],
            "tiflash": [item.to_object() for item in self._tiflash]
        }


class IPAccessList:
    def __init__(self, cidr: str, description: str = ""):
        self._cidr = cidr
        self._description = description

    def to_object(self) -> dict:
        return {
            "cidr": self._cidr,
            "description": self._description
        }


class TiDBComponent:
    def __init__(self, node_size: str = None, node_quantity: int = None):
        self._node_size = node_size
        self._node_quantity = node_quantity

    @property
    def node_size(self) -> str:
        return self._node_size

    @property
    def node_quantity(self) -> int:
        return self._node_quantity


class TiKVComponent:
    def __init__(self, node_size: str = None, node_quantity: int = None, storage_size_gib: int = None):
        self._node_size = node_size
        self._node_quantity = node_quantity
        self._storage_size_gib = storage_size_gib

    @property
    def node_size(self) -> str:
        return self._node_size

    @property
    def node_quantity(self) -> int:
        return self._node_quantity

    @property
    def storage_size_gib(self) -> int:
        return self._storage_size_gib


class TiFlashComponent:
    def __init__(self, node_size: str = None, node_quantity: int = None, storage_size_gib: int = None):
        self._node_size = node_size
        self._node_quantity = node_quantity
        self._storage_size_gib = storage_size_gib

    @property
    def node_size(self) -> str:
        return self._node_size

    @property
    def node_quantity(self) -> int:
        return self._node_quantity

    @property
    def storage_size_gib(self) -> int:
        return self._storage_size_gib


class ClusterComponents:
    def __init__(self, tidb: TiDBComponent, tikv: TiKVComponent, tiflash: TiFlashComponent = None):
        self._tidb = tidb
        self._tikv = tikv
        self._tiflash = tiflash

    @classmethod
    def from_object(cls, obj: dict):
        return cls(
            TiDBComponent(obj["tidb"].get("node_size"), obj["tidb"].get("node_quantity")),
            TiKVComponent(obj["tikv"].get("node_size"), obj["tikv"].get("node_quantity"),
                          obj["tikv"].get("storage_size_gib")),
            TiFlashComponent(obj["tiflash"].get("node_size"), obj["tiflash"].get("node_quantity"),
                             obj["tiflash"].get("storage_size_gib")) if obj.get("tiflash") else None
        )

    def to_object(self) -> dict:
        return {
            "tidb": {
                "node_size": self._tidb.node_size,
                "node_quantity": self._tidb.node_quantity
            },
            "tikv": {
                "node_size": self._tikv.node_size,
                "node_quantity": self._tikv.node_quantity,
                "storage_size_gib": self._tikv.storage_size_gib
            },
            "tiflash": {
                "node_size": self._tiflash.node_size,
                "node_quantity": self._tiflash.node_quantity,
                "storage_size_gib": self._tiflash.storage_size_gib
            } if self._tiflash is not None else None
        }


class ClusterConfig:
    def __init__(self, root_password: str = None, port: int = None, components: ClusterComponents = None,
                 ip_access_list: [IPAccessList] = None):
        self._root_password = root_password
        self._port = port
        self._components = components
        self._ip_access_list = ip_access_list

    @classmethod
    def from_object(cls, obj: dict):
        return cls(
            port=obj["port"],
            components=ClusterComponents.from_object(obj["components"])
        )

    def to_object(self) -> dict:
        return {
            "root_password": self._root_password,
            "port": self._port,
            "components": self._components.to_object(),
            "ip_access_list": [item.to_object() for item in self._ip_access_list] if self._ip_access_list else None
        }

    def __repr__(self):
        return "<ClusterConfig port={} components={}>".format(self._port, self._components)


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
            self._tidb = TiDBComponent(node_size, node_quantity)
        elif component == "tikv":
            self._tikv = TiKVComponent(node_size, node_quantity, storage_size_gib)
        elif component == "tiflash":
            self._tiflash = TiFlashComponent(node_size, node_quantity, storage_size_gib)
        else:
            raise Exception("Invalid component, only tidb, tikv, tiflash are supported")
        return self

    def add_ip_access(self, cidr: str, description: str = ""):
        self._ip_access_list.append(IPAccessList(cidr, description))
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


class UpdateClusterConfig:
    def __init__(self):
        self._tidb = None
        self._tikv = None
        self._tiflash = None

    def update_component(self, component: str, node_quantity: int = None, node_size: str = None,
                         storage_size_gib: int = None):
        if component == "tidb" and node_quantity is not None:
            self._tidb = TiDBComponent(node_size, node_quantity)
        elif component == "tikv" and node_quantity is not None:
            self._tikv = TiKVComponent(node_size, node_quantity, storage_size_gib)
        elif component == "tiflash" and node_quantity is not None:
            self._tiflash = TiFlashComponent(node_size, node_quantity, storage_size_gib)
        else:
            raise Exception("Invalid component, only tidb, tikv, tiflash are supported")
        return self

    def to_object(self) -> dict:
        components = {}
        if self._tidb is not None:
            components["tidb"] = {"node_quantity": self._tidb.node_quantity}
        if self._tikv is not None:
            components["tikv"] = {"node_quantity": self._tikv.node_quantity}
        if self._tiflash is not None:
            components["tiflash"] = {}
            if self._tiflash.storage_size_gib is not None:
                components["tiflash"]["storage_size_gib"] = self._tiflash.storage_size_gib
            if self._tiflash.node_size is not None:
                components["tiflash"]["node_size"] = self._tiflash.node_size
            if self._tiflash.node_quantity is not None:
                components["tiflash"]["node_quantity"] = self._tiflash.node_quantity

        return {
            "config": {
                "components": components
            }
        }


class ClusterInfo:
    def __init__(self, tidb_version: str, cluster_status: ClusterStatus, node_map: NodeMapSpec,
                 connection_strings: ConnectionStrings):
        self._tidb_version = tidb_version
        self._cluster_status = cluster_status
        self._node_map = node_map
        self._connection_strings = connection_strings

    @property
    def connection_strings(self):
        return self._connection_strings

    @property
    def cluster_status(self):
        return self._cluster_status

    @classmethod
    def from_object(cls, obj: dict):
        return cls(
            tidb_version=obj["tidb_version"],
            cluster_status=ClusterStatus(obj["cluster_status"]),
            node_map=NodeMapSpec.from_object(obj["node_map"]),
            connection_strings=ConnectionStrings.from_object(obj["connection_strings"])
        )

    def to_object(self) -> dict:
        return {
            "tidb_version": self._tidb_version,
            "cluster_status": self._cluster_status.value,
            "node_map": self._node_map.to_object(),
            "connection_strings": self._connection_strings.to_object()
        }

    def __repr__(self):
        return "<tidb={} status= {} default user={}>".format(self._tidb_version, self._cluster_status,
                                                             self._connection_strings.default_user)


# noinspection PyShadowingBuiltins
class ClusterInfoOfRestore:
    def __init__(self, id: str = None, name: str = None, status: ClusterStatus = None):
        self._id = id
        self._name = name
        self._status = status

    def __repr__(self):
        return "<id={}, name={}, status={}>".format(self._id, self._name, self._status)


class CloudSpecification:
    def __init__(self, cluster_type: ClusterType, cloud_provider: CloudProvider, region: str, tidb: [TiDBProfile],
                 tikv: [TiKVProfile],
                 tiflash: [TiFlashProfile]):
        self.cluster_type = cluster_type
        self.cloud_provider = cloud_provider
        self.region = region
        self.tidb = tidb
        self.tikv = tikv
        self.tiflash = tiflash

    @classmethod
    def from_object(cls, obj: dict):
        return cls(
            cluster_type=ClusterType[obj["cluster_type"]],
            cloud_provider=CloudProvider[obj["cloud_provider"]],
            region=obj["region"],
            tidb=[TiDBProfile.from_object(item) for item in obj["tidb"]],
            tikv=[TiKVProfile.from_object(item) for item in obj["tikv"]],
            tiflash=[TiFlashProfile.from_object(item) for item in obj["tiflash"]]
        )

    def to_object(self):
        return {
            "cluster_type": self.cluster_type.value,
            "cloud_provider": self.cloud_provider.value,
            "region": self.region,
            "tidb": [item.to_object() for item in self.tidb],
            "tikv": [item.to_object() for item in self.tikv],
            "tiflash": [item.to_object() for item in self.tiflash]
        }

    def __repr__(self):
        return "<Specification cluster_type={} cloud_provider={} region={}>".format(self.cluster_type,
                                                                                    self.cloud_provider,
                                                                                    self.region)
