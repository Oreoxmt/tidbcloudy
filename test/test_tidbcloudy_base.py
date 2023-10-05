from test_server_config import TEST_CLUSTER_CONFIG
from tidbcloudy.cluster import Cluster
from tidbcloudy.context import Context


class TestTiDBCloudyBase:
    def test_from_to_object(self):
        context = Context("", "", {})
        cluster = Cluster.from_object(context, TEST_CLUSTER_CONFIG)
        assert cluster.cloud_provider.value == "AWS"
        assert cluster.cluster_type.value == "DEDICATED"
        assert cluster.config.components.tidb.node_size == "4C16G"
        assert cluster.config.components.tidb.node_quantity == 1
        assert cluster.config.components.tikv.node_size == "4C16G"
        assert cluster.config.components.tikv.node_quantity == 2
        assert cluster.config.components.tikv.storage_size_gib == 200
        assert cluster.config.components.tiflash.node_size == "4C16G"
        assert cluster.config.components.tiflash.node_quantity == 3
        assert cluster.config.components.tiflash.storage_size_gib == 500
        assert cluster.config.ip_access_list[0].cidr == "0.0.0.0/0"
        assert cluster.config.ip_access_list[0].description == "test 0"
        assert cluster.config.ip_access_list[1].cidr == "1.1.1.1/1"
        assert cluster.config.ip_access_list[1].description == "test 1"
        assert cluster.config.port == 4000
        assert cluster.config.root_password == "root"
        assert cluster.name == "test"
        assert cluster.region == "us-west-1"
        assert cluster.to_object() == TEST_CLUSTER_CONFIG
