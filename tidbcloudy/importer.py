from ._base import TiDBCloudyBase, TiDBCloudyContextualBase, TiDBCloudyField
from .specification import ImportMetadta, ImportSpec, ImportStatus
from .util.log import log

class Import(TiDBCloudyBase, TiDBCloudyContextualBase):
    __slots__ =["_metadata", "_spec", "_status"]
    metadata: ImportMetadta = TiDBCloudyField(ImportMetadta)
    spec: ImportSpec = TiDBCloudyField(ImportSpec)
    status: ImportStatus = TiDBCloudyField(ImportStatus)

    def update(self):
        pass