TEST_SERVER_CONFIG = {
    "v1beta": "http://127.0.0.1:5000/api/v1beta/",
    "billing": "http://127.0.0.1:5000/billing/v1beta1/"
}
TEST_CLUSTER_CONFIG = {
    "cloud_provider": "AWS",
    "cluster_type": "DEDICATED",
    "config": {
        "components": {"tidb": {"node_size": "4C16G", "node_quantity": 1},
                       "tikv": {"node_size": "4C16G", "node_quantity": 2, "storage_size_gib": 200},
                       "tiflash": {"node_size": "4C16G", "node_quantity": 3, "storage_size_gib": 500}},
        "ip_access_list": [{"cidr": "0.0.0.0/0", "description": "test 0"},
                           {"cidr": "1.1.1.1/1", "description": "test 1"}],
        "port": 4000,
        "root_password": "root",
    },
    "name": "test",
    "region": "us-west-1"}
