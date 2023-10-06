from test_server_config import TEST_CLUSTER_CONFIG
from tidbcloudy.specification import CreateClusterConfig, UpdateClusterConfig


class TestCreateClusterConfig:
    def test_default(self):
        cluster_config = CreateClusterConfig()
        assert (cluster_config.to_object() == {
            "cloud_provider": None,
            "cluster_type": None,
            "config": {
                "components": {"tidb": None, "tiflash": None, "tikv": None},
                "ip_access_list": [],
                "port": None,
                "root_password": None,
            },
            "name": "",
            "region": None})

    def test_set_value(self):
        cluster_config = CreateClusterConfig()
        cluster_config \
            .set_name("test") \
            .set_cluster_type("dEdicatEd") \
            .set_cloud_provider("aWs") \
            .set_region("us-west-1") \
            .set_root_password("root") \
            .set_port(4000) \
            .set_component("tidb", "4C16G", 1) \
            .set_component("tikv", "4C16G", 2, 200) \
            .set_component("tiflash", "4C16G", 3, 500) \
            .add_ip_access("0.0.0.0/0", "test 0") \
            .add_ip_access("1.1.1.1/1", "test 1")
        assert cluster_config.to_object() == TEST_CLUSTER_CONFIG


class TestUpdateClusterConfig:
    def test_default(self):
        cluster_config = UpdateClusterConfig()
        assert cluster_config.to_object() == {
            "config": {
                "components": {}
            }
        }

    def test_update_component(self):
        cluster_config = UpdateClusterConfig()
        cluster_config.update_component("tidb", 2, "8C16G")
        cluster_config.update_component("tikv", 1, "8C32G", 400)
        cluster_config.update_component("tiflash", 3, "8C64G", 500)
        assert cluster_config.to_object() == {
            "config": {
                "components": {
                    "tidb": {
                        "node_quantity": 2,
                        "node_size": "8C16G"
                    },
                    "tikv": {
                        "node_quantity": 1,
                        "node_size": "8C32G",
                        "storage_size_gib": 400
                    },
                    "tiflash": {
                        "node_quantity": 3,
                        "node_size": "8C64G",
                        "storage_size_gib": 500
                    }
                }
            }
        }
