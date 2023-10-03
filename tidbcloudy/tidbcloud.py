from typing import Iterator, List

from tidbcloudy.baseURL import V1BETA1
from tidbcloudy.context import Context
from tidbcloudy.project import Project
from tidbcloudy.specification import BillingMonthSummary, CloudSpecification
from tidbcloudy.util.page import Page
from tidbcloudy.util.timestamp import get_current_year_month


class TiDBCloud:
    def __init__(self, public_key: str, private_key: str):
        self._context = Context(public_key, private_key)

    def create_project(self, name: str, aws_cmek_enabled: bool = False, update_from_server: bool = False) -> Project:
        """
        Create a project.
        Args:
            name: the project name.
            aws_cmek_enabled: whether to enable AWS Customer-Managed Encryption Keys.
            update_from_server: whether to update the project info after creating.

        Returns:
            If the update_from_server is False, return a Project object with only the context and project_id.
            If the update_from_server is True, return a Project object with all the info.

        Examples:
            .. code-block:: python
                import tidbcloudy
                api = tidbcloudy.TiDBCloud(public_key="your_public_key", private_key="your_private_key")
                project = api.create_project(name="your_project_name", aws_cmek_enabled=False, update_from_server=True)
                print(project)
        """
        config = {
            "name": name,
            "aws_cmek_enabled": aws_cmek_enabled
        }
        resp = self._context.call_post(path="projects", json=config)
        project_id = resp["id"]
        if update_from_server:
            return self.get_project(project_id=project_id, update_from_server=True)
        return Project(context=self._context, id=project_id)

    def get_project(self, project_id: str, update_from_server: bool = False) -> Project:
        """
        Get the project object by project_id.
        Args:
            project_id: the project id.
            update_from_server: whether to update the project info.

        Returns:
            If the update_from_server is False, return a Project object with only the context and project_id.
            If the update_from_server is True, return a Project object with all the info.

        Examples:
            .. code-block:: python
                import tidbcloudy
                api = tidbcloudy.TiDBCloud(public_key="your_public_key", private_key="your_private_key")
                project = api.get_project("your_project_id", update_from_server=True)
        """
        project = Project(context=self._context, id=project_id)
        if update_from_server:
            for item in self.iter_projects():
                if item.id == project_id:
                    return item
            raise ValueError("Project {} not found".format(project_id))
        return project

    def list_projects(self, page: int = None, page_size: int = None) -> Page[Project]:
        """
        List all projects.
        Args:
            page: the page number.
            page_size: the page size of each page.

        Returns:
            the projects list.

        Examples:
            .. code-block:: python
                import tidbcloudy
                api = tidbcloudy.TiDBCloud(public_key="your_public_key", private_key="your_private_key")
                projects = api.list_projects()
                total = projects.total
                for project in projects.items:
                    print(project) # This is a Project object

        """
        query = {}
        if page is not None:
            query["page"] = page
        if page_size is not None:
            query["page_size"] = page_size
        resp = self._context.call_get(path="projects", params=query)
        return Page(
            [Project.from_object(self._context, item) for item in resp["items"]],
            page, page_size, resp["total"])

    def iter_projects(self, page_size: int = 10) -> Iterator[Project]:
        """
        Iterate all projects.
        Args:
            page_size: the page size of each page.

        Returns:
            the projects iterator.

        Examples:
            .. code-block:: python
                import tidbcloudy
                api = tidbcloudy.TiDBCloud(public_key="your_public_key", private_key="your_private_key")
                for project in api.iter_projects():
                    print(project) # This is a Project object

        """
        page = 1
        total = None
        while total is None or (page - 1) * page_size < total:
            projects = self.list_projects(page=page, page_size=page_size)
            total = projects.total
            for project in projects.items:
                yield project
            page += 1

    def list_provider_regions(self) -> List[CloudSpecification]:
        """
        List all provider regions.
        Returns:
            the provider regions list.

        Examples:
            .. code-block:: python
                import tidbcloudy
                api = tidbcloudy.TiDBCloud(public_key="your_public_key", private_key="your_private_key")
                regions = api.list_provider_regions()
                for spec in api.list_provider_regions():
                    print(spec) # This is a CloudSpecification object

        """
        resp = self._context.call_get(path="clusters/provider/regions")
        return [CloudSpecification.from_object(obj=item) for item in resp["items"]]

    def get_monthly_bill(self, month: str) -> BillingMonthSummary:
        """
        Get the monthly billing.
        Args:
            month: the month of the bill, format: YYYY-MM or YYYYMM.
        Returns:
            the monthly billing.

        Examples:
            .. code-block:: python
                import tidbcloudy
                api = tidbcloudy.TiDBCloud(public_key="your_public_key", private_key="your_private_key")
                billing = api.get_monthly_bill(month="2023-08")
                print(billing)

        """
        if "-" not in month and len(month) == 6:
            month = f"{month[:4]}-{month[4:]}"
        path = f"bills/{month}"
        resp = self._context.call_get(path=path, base_url=V1BETA1.BILLING.value)
        return BillingMonthSummary.from_object(self._context, resp)

    def get_current_month_bill(self) -> BillingMonthSummary:
        """
        Get the billing of current month.
        Returns:
            the current month billing.

        Examples:
            .. code-block:: python
                import tidbcloudy
                api = tidbcloudy.TiDBCloud(public_key="your_public_key", private_key="your_private_key")
                billing = api.get_current_month_bill()
                print(billing)

        """
        return self.get_monthly_bill(month=get_current_year_month())
