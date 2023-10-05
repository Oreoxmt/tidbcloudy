from flask import Blueprint, Response

from mock_server.server_state import CONFIG
from mock_server.services.project_service import ProjectService
from tidbcloudy.context import Context
from tidbcloudy.specification import CloudSpecification


def create_clusters_blueprint():
    bp = Blueprint("clusters", __name__)

    pro_service = ProjectService()
    contex = Context("", "", {})

    @bp.route("/provider/regions", methods=["GET"])
    def tidbcloudy_provider() -> [Response, int]:
        provider_regions = [CloudSpecification.from_object(contex, item) for item in CONFIG["provider_regions"]]
        provider_regions_obj = pro_service.list_provider_regions(provider_regions)
        return {"items": [item.to_object() for item in provider_regions_obj]}

    return bp
