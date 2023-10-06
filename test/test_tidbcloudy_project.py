import tidbcloudy
from test_server_config import TEST_SERVER_CONFIG
from tidbcloudy.cluster import Cluster
from tidbcloudy.specification import ProjectAWSCMEK
from tidbcloudy.util.page import Page
from tidbcloudy.util.timestamp import timestamp_to_string

api = tidbcloudy.TiDBCloud(public_key="", private_key="", server_config=TEST_SERVER_CONFIG)
project = api.get_project(project_id="2", update_from_server=True)


class TestAWSCMEK:
    @staticmethod
    def assert_awscmek_properties(awscmek: ProjectAWSCMEK):
        assert isinstance(awscmek, ProjectAWSCMEK)
        assert isinstance(awscmek.region, str)
        assert isinstance(awscmek.kms_arn, str)

    @staticmethod
    def assert_awscmek_1(awscmek: ProjectAWSCMEK):
        TestAWSCMEK.assert_awscmek_properties(awscmek)
        assert awscmek.region == "us-east-1"
        assert awscmek.kms_arn == "arn:aws:kms:us-east-1:123456789"

    @staticmethod
    def assert_awscmek_2(awscmek: ProjectAWSCMEK):
        TestAWSCMEK.assert_awscmek_properties(awscmek)
        assert awscmek.region == "us-west-2"
        assert awscmek.kms_arn == "arn:aws:kms:us-west-2:123456789"

    def test_list_aws_cmek(self):
        cmeks = project.list_aws_cmek()
        assert isinstance(cmeks, Page)
        assert cmeks.page == 1
        assert len(cmeks.items) == 0
        assert cmeks.total == 0
        assert cmeks.page_size == cmeks.total

    def test_create_aws_cmek(self):
        project.create_aws_cmek(
            [("us-east-1", "arn:aws:kms:us-east-1:123456789"),
             ("us-west-2", "arn:aws:kms:us-west-2:123456789")])
        cmeks = project.list_aws_cmek()
        assert isinstance(cmeks, Page)
        assert cmeks.page == 1
        assert len(cmeks.items) == 2
        assert cmeks.total == 2
        assert cmeks.page_size == cmeks.total
        self.assert_awscmek_1(cmeks.items[0])
        self.assert_awscmek_2(cmeks.items[1])

    def test_iter_aws_cmek(self):
        for cmek in project.iter_aws_cmek():
            self.assert_awscmek_properties(cmek)
            if cmek.region == "us-east-1":
                self.assert_awscmek_1(cmek)
            elif cmek.region == "us-west-2":
                self.assert_awscmek_2(cmek)
            else:
                assert False


class TestCluster:
    @staticmethod
    def assert_cluster_dedicated_properties(cluster: Cluster):
        assert cluster.id == "2"
        assert cluster.name == "Cluster1"
        assert cluster.create_timestamp == 1656991448
        assert cluster.config.port == 4000
        assert cluster.config.components.tidb.node_size == "8C16G"
        assert cluster.config.components.tidb.node_quantity == 2
        assert cluster.config.components.tikv.node_size == "8C32G"
        assert cluster.config.components.tikv.node_quantity == 3
        assert cluster.config.components.tikv.storage_size_gib == 1024
        assert cluster.status.tidb_version == "v7.1.0"
        assert cluster.status.cluster_status.value == "AVAILABLE"
        assert cluster.status.node_map.tidb[0].to_object() == {
            "node_name": "tidb-0",
            "availability_zone": "us-west-2a",
            "node_size": "8C16G",
            "vcpu_num": 8,
            "ram_bytes": "17179869184",
            "status": "NODE_STATUS_AVAILABLE"
        }
        assert cluster.status.node_map.tiflash[0].to_object() == {
            "node_name": "tiflash-0",
            "availability_zone": "us-west-2a",
            "node_size": "8C64G",
            "vcpu_num": 8,
            "ram_bytes": "68719476736",
            "storage_size_gib": 1024,
            "status": "NODE_STATUS_AVAILABLE"
        }
        assert cluster.status.connection_strings.default_user == "root"
        assert cluster.status.connection_strings.standard.host == "tidb.test.us-east-1.shared.aws.tidbcloud.com"
        assert cluster.status.connection_strings.standard.port == cluster.status.connection_strings.vpc_peering.port \
               == 4000
        assert cluster.status.connection_strings.vpc_peering.host \
               == "private-tidb.test.us-east-1.shared.aws.tidbcloud.com"
        assert repr(cluster) == f"<Cluster id={cluster.id} name={cluster.name} type={cluster.cluster_type.value} " \
                                f"create_at={timestamp_to_string(cluster.create_timestamp)}>"

    @staticmethod
    def assert_cluster_developer_properties(cluster: Cluster):
        assert cluster.id == "3456"
        assert cluster.name == "serverless-0"
        assert cluster.create_timestamp == 1606472018
        assert cluster.config.port == cluster.status.connection_strings.standard.port \
               == cluster.status.connection_strings.vpc_peering.port == 4000
        assert cluster.config.components.tidb.node_size == cluster.config.components.tikv.node_size \
               == cluster.config.components.tiflash.node_size == "Shared0"
        assert cluster.config.components.tidb.node_quantity == cluster.config.components.tikv.node_quantity \
               == cluster.config.components.tiflash.node_quantity == 1
        assert cluster.config.components.tikv.storage_size_gib == cluster.config.components.tiflash.storage_size_gib == 0
        assert cluster.status.tidb_version == "v7.1.0"
        assert cluster.status.cluster_status.value == "AVAILABLE"
        assert cluster.status.node_map.tidb == cluster.status.node_map.tikv == cluster.status.node_map.tiflash == []
        assert cluster.status.connection_strings.default_user == "test.root"
        assert cluster.status.connection_strings.standard.host == "gateway01.prod.aws.tidbcloud.com"
        assert cluster.status.connection_strings.vpc_peering.host == "gateway01-privatelink.prod.aws.tidbcloud.com"

    def test_iter_clusters(self):
        for cluster in project.iter_clusters():
            assert isinstance(cluster, Cluster)
            if cluster.cluster_type.value == "DEDICATED":
                TestCluster.assert_cluster_dedicated_properties(cluster)
            elif cluster.cluster_type.value == "DEVELOPER":
                TestCluster.assert_cluster_developer_properties(cluster)
            else:
                assert False

    def test_list_clusters(self):
        clusters = project.list_clusters()
        assert isinstance(clusters, Page)
        assert len(clusters.items) == clusters.total == 2
        assert clusters.page == 1
        assert clusters.page_size == 10
        for cluster in clusters.items:
            assert isinstance(cluster, Cluster)
            assert cluster.project_id == "2"
            if cluster.cluster_type.value == "DEDICATED":
                TestCluster.assert_cluster_dedicated_properties(cluster)
            elif cluster.cluster_type.value == "DEVELOPER":
                TestCluster.assert_cluster_developer_properties(cluster)
            else:
                assert False

    def test_get_cluster(self):
        cluster = project.get_cluster(cluster_id="2")
        assert isinstance(cluster, Cluster)
        TestCluster.assert_cluster_dedicated_properties(cluster)

    def test_create_cluster(self):
        config = CreateClusterConfig()
        config \
            .set_name("test-serverless") \
            .set_cluster_type("DEVELOPER") \
            .set_cloud_provider("aws") \
            .set_region("us-west-2") \
            .set_root_password("password") \
            .add_ip_access(cidr="0.0.0.0/0") \
            .add_ip_access(cidr="1.1.1.1/1")
        cluster = project.create_cluster(config=config)
        assert isinstance(cluster, Cluster)
        assert repr(cluster) == f"<Cluster id={cluster.id} Unknown status>"
        cluster.wait_for_available(interval_sec=1)
        assert cluster.status.cluster_status.value == "AVAILABLE"
        assert cluster.name == "test-serverless"
        assert cluster.cluster_type.value == "DEVELOPER"
        assert cluster.cloud_provider.value == "AWS"
        assert cluster.region == "us-west-2"
        assert cluster.config.port == cluster.status.connection_strings.standard.port \
               == cluster.status.connection_strings.vpc_peering.port == 4000
        assert cluster.status.tidb_version == "v0.0.0"
        assert repr(cluster) == f"<Cluster id={cluster.id} name={cluster.name} type={cluster.cluster_type.value} " \
                                f"create_at={timestamp_to_string(cluster.create_timestamp)}>"
        assert project.get_cluster(cluster_id=cluster.id).to_object() == cluster.to_object()
