from typing import Iterator, List

from tidbcloudy.context import Context
from tidbcloudy.project import Project
from tidbcloudy.specification import CloudSpecification
from tidbcloudy.util.page import Page


class TiDBCloud:
    def __init__(self, public_key: str, private_key: str):
        self._context = Context(public_key, private_key)

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
