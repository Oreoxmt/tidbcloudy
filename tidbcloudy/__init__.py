import sys

from .api.tidbcloud import TiDBCloud
from .api.context import Context
from .api.project import Project
from .api.cluster import Cluster
from .api.backup import Backup
from .api.restore import Restore
from .exception import TiDBCloudException

from .api import backup
from .api import cluster
from .api import context
from .api import project
from .api import restore
from .api import specification
from .api import tidbcloud

_aliases = ["backup", "cluster", "context", "project", "restore", "specification", "tidbcloud"]

for _alias in _aliases:
    sys.modules["tidbcloudy.{}".format(_alias)] = sys.modules["tidbcloudy.api.{}".format(_alias)]
