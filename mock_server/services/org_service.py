import uuid
from datetime import datetime
from typing import List, Union

from mock_server.server_state import CONFIG
from tidbcloudy.context import Context
from tidbcloudy.project import Project
from tidbcloudy.specification import BillingMonthSummary


class OrgService:
    def __init__(self):
        self.org_id = CONFIG["org_id"]
        self._context = Context("", "", {})

    @staticmethod
    def list_projects(projects: List[Project], page: int, page_size: int) -> List[Project]:
        return_projects = projects[(page - 1) * page_size: page * page_size]
        return return_projects

    def create_project(self, body: dict) -> Project:
        new_project = Project.from_object(self._context, {
            "id": str(uuid.uuid4().int % (10 ** 19)),
            "org_id": self.org_id,
            "name": body["name"],
            "aws_cmek_enabled": body["aws_cmek_enabled"] if "aws_cmek_enabled" in body else False,
            "cluster_count": 0,
            "user_count": 1,
            "create_timestamp": str(int(datetime.now().timestamp()))
        })
        return new_project

    @staticmethod
    def get_monthly_bill(billings: List[BillingMonthSummary], month: str) -> Union[None, BillingMonthSummary]:
        for billing in billings:
            if billing.overview.billedMonth == month:
                return billing
        return None
