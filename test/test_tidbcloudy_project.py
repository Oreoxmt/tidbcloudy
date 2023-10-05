import tidbcloudy
from test_server_config import TEST_SERVER_CONFIG
from tidbcloudy.specification import ProjectAWSCMEK
from tidbcloudy.util.page import Page

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
            print(cmek)
            self.assert_awscmek_properties(cmek)
            if cmek.region == "us-east-1":
                self.assert_awscmek_1(cmek)
            elif cmek.region == "us-west-2":
                self.assert_awscmek_2(cmek)
            else:
                assert False
