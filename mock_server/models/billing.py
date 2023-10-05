from flask import Blueprint, Response

from mock_server.server_state import CONFIG
from mock_server.services.org_service import OrgService
from mock_server.services.project_service import ProjectService
from tidbcloudy.context import Context
from tidbcloudy.specification import BillingMonthSummary


def create_billing_blueprint():
    bp = Blueprint("billing", __name__)
    org_service = OrgService()
    contex = Context("", "", {})

    @bp.route("<string:month>", methods=["GET"])
    def tidbcloudy_get_monthly_bill(month: str) -> [Response, int]:
        billings = [BillingMonthSummary.from_object(contex, item) for item in CONFIG["billings"]]
        billing = org_service.get_monthly_bill(billings, month)
        if billing is None:
            return {
                "code": "string",
                "error": "The billing month is not found",
                "msgPrefix": "string",
                "status": 0
            }, 400
        resp = billing.to_object()
        return resp, 200

    return bp
