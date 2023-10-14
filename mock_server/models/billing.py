from flask import Blueprint, jsonify, Response
from httpx import HTTPStatusError

from mock_server.server_state import CONFIG
from mock_server.services.org_service import OrgService
from tidbcloudy.context import Context
from tidbcloudy.specification import BillingMonthSummary


def create_billing_blueprint():
    bp = Blueprint("billing", __name__)

    org_service = OrgService()
    contex = Context("", "", {})

    @bp.errorhandler(HTTPStatusError)
    def handle_status_error(exc: HTTPStatusError):
        return jsonify({"error": exc.response.text}), exc.response.status_code

    @bp.route("<string:month>", methods=["GET"])
    def tidbcloudy_get_monthly_bill(month: str) -> [Response, int]:
        billings = [BillingMonthSummary.from_object(contex, item) for item in CONFIG["billings"]]
        billing = org_service.get_monthly_bill(billings, month)
        resp = billing.to_object()
        return resp, 200

    return bp
