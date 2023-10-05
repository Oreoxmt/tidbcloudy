import tidbcloudy
from test_server_config import TEST_SERVER_CONFIG
from tidbcloudy.project import Project
from tidbcloudy.specification import CloudSpecification
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
