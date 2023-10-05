from typing import List, Union

from tidbcloudy.context import Context
from tidbcloudy.specification import CloudSpecification


class ProjectService:
    def __init__(self):
        self._context = Context("", "", {})

    @staticmethod
    def _get_project_by_id(projects: List[dict], project_id: str) -> dict:
        for project in projects:
            if project["id"] == project_id:
                return project
        return {}

    @staticmethod
    def _get_project_index_by_id(projects: List[dict], project_id: str) -> Union[int, None]:
        for index, project in enumerate(projects):
            if project["id"] == project_id:
                return index
        return None

    @staticmethod
    def list_project_aws_cmeks(projects: List[dict], project_id: str) -> Union[list, List[dict]]:
        project = ProjectService._get_project_by_id(projects, project_id)
        if project:
            return project.get("aws_cmek", [])

    @staticmethod
    def create_project_aws_cmek(projects: List[dict], project_id: str, body: dict) -> bool:
        project_index = ProjectService._get_project_index_by_id(projects, project_id)
        if project_index is None or projects[project_index].get("aws_cmek_enabled") is False:
            return False
        project_cmek = projects[project_index].get("aws_cmek", [])
        for create_cmek in body.get("specs", []):
            current_cmek = {
                "region": create_cmek["region"],
                "kms_arn": create_cmek["kms_arn"],
            }
            project_cmek.append(current_cmek)
        projects[project_index].update({"aws_cmek": project_cmek})
        return True

    @staticmethod
    def list_provider_regions(provider_regions: List[CloudSpecification]) -> List[CloudSpecification]:
        return provider_regions
