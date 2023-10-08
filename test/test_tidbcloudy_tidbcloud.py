import pytest

import tidbcloudy
from test_server_config import TEST_SERVER_CONFIG
from tidbcloudy.exception import TiDBCloudResponseException
from tidbcloudy.project import Project
from tidbcloudy.specification import BillingMonthSummary, CloudSpecification
from tidbcloudy.util.page import Page
from tidbcloudy.util.timestamp import timestamp_to_string

api = tidbcloudy.TiDBCloud(public_key="", private_key="", server_config=TEST_SERVER_CONFIG)


class TestProject:
    project_init_num = 2

    @staticmethod
    def assert_project_properties(project: Project):
        assert isinstance(project, Project)
        assert isinstance(project.id, str)
        assert project.id.isdigit() and int(project.id) > 0
        assert isinstance(project.org_id, str)
        assert isinstance(project.name, str)
        assert isinstance(project.cluster_count, int)
        assert isinstance(project.user_count, int)
        assert isinstance(project.create_timestamp, int)
        assert project.create_timestamp > 0 and len(str(project.create_timestamp)) == 10
        assert isinstance(project.aws_cmek_enabled, bool)

    @staticmethod
    def assert_project_1(project: Project):
        TestProject.assert_project_properties(project)
        assert repr(
            project) == "<Project id=1 name=default_project aws_cmek_enabled=False create_at=2022-07-05 11:24:08>"
        assert project.id == "1"
        assert project.org_id == "1"
        assert project.name == "default_project"
        assert project.cluster_count == 4
        assert project.user_count == 10
        assert project.create_timestamp == 1656991448
        assert project.aws_cmek_enabled is False

    def test_list_projects_init(self):
        projects = api.list_projects(page=1, page_size=1)
        assert isinstance(projects, Page)
        assert projects.page == 1
        assert projects.page_size == 1
        assert projects.total == TestProject.project_init_num
        assert len(projects.items) == 1
        for project in projects.items:
            self.assert_project_1(project)

    def test_create_project(self):
        project = api.create_project(name="test_project", aws_cmek_enabled=True, update_from_server=True)
        self.assert_project_properties(project)
        assert repr(
            project) == (f"<Project id={project.id} name=test_project aws_cmek_enabled=True "
                         f"create_at={timestamp_to_string(project.create_timestamp)}>")
        assert project.org_id == "1"
        assert project.name == "test_project"
        assert project.cluster_count == 0
        assert project.user_count == 1
        assert project.aws_cmek_enabled is True
        current_projects = api.list_projects(page=1, page_size=1)
        assert current_projects.total == TestProject.project_init_num + 1

    def test_get_project(self):
        project = api.get_project(project_id="1", update_from_server=False)
        assert repr(project) == "<Project id=1 name=None aws_cmek_enabled=None create_at=>"
        project = api.get_project(project_id="1", update_from_server=True)
        self.assert_project_1(project)

    def test_iter_projects(self):
        for project in api.iter_projects():
            self.assert_project_properties(project)


class TestProviderRegions:
    @staticmethod
    def assert_provider_regions_dedicated(spec: CloudSpecification):
        assert repr(spec) == "<Specification cluster_type=DEDICATED cloud_provider=AWS region=us-west-2>"

    @staticmethod
    def assert_provider_regions_developer(spec: CloudSpecification):
        assert repr(spec) == "<Specification cluster_type=DEVELOPER cloud_provider=AWS region=us-west-2>"

    def test_list_provider_regions(self):
        provider_regions = api.list_provider_regions()
        assert len(provider_regions) == 2
        for spec in provider_regions:
            assert isinstance(spec, CloudSpecification)
            if spec.cluster_type.value == "DEDICATED":
                TestProviderRegions.assert_provider_regions_dedicated(spec)
            elif spec.cluster_type.value == "DEVELOPER":
                TestProviderRegions.assert_provider_regions_developer(spec)
            else:
                assert False


class TestBilling:
    @staticmethod
    def assert_billing(billing: BillingMonthSummary):
        assert isinstance(billing, BillingMonthSummary)
        assert repr(billing) == "<BillingMonthSummary month=2023-10>"
        assert billing.overview.to_object() == {
            "billedMonth": "2023-10",
            "credits": "1.00",
            "discounts": "2.00",
            "runningTotal": "3.00",
            "totalCost": "4.00"
        }
        assert billing.summaryByProject.otherCharges[0].to_object() == {
            "chargeName": "Support Plan",
            "credits": "0.10",
            "discounts": "0.20",
            "runningTotal": "0.30",
            "totalCost": "0.40"
        }
        assert billing.summaryByProject.projects[0].to_object() == {
            "credits": "3.00",
            "discounts": "0.50",
            "projectName": "prod-project",
            "runningTotal": "1.00",
            "totalCost": "4.00"
        }
        assert billing.summaryByService[0].to_object() == {
            "credits": "2.00",
            "discounts": "3.00",
            "runningTotal": "5.00",
            "serviceCosts": [
                {}
            ],
            "serviceName": "TiDB Dedicated",
            "totalCost": "4.00"
        }

    def test_get_monthly_bill(self):
        current_bill = api.get_monthly_bill(month="202309")
        assert current_bill.overview.billedMonth == "2023-09"
        current_bill = api.get_monthly_bill(month="2023-10")
        assert current_bill.overview.billedMonth == "2023-10"
        current_bill = api.get_monthly_bill(month="202310")
        assert current_bill.overview.billedMonth == "2023-10"
        TestBilling.assert_billing(current_bill)
        with pytest.raises(TiDBCloudResponseException) as exc_info:
            api.get_monthly_bill(month="202308")
        assert exc_info.value.status == 400
