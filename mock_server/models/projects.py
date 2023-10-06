from flask import Blueprint, jsonify, request, Response

from mock_server.server_state import CONFIG
from mock_server.services.org_service import OrgService
from mock_server.services.project_service import ProjectService
from tidbcloudy.cluster import Cluster
from tidbcloudy.context import Context
from tidbcloudy.project import Project


def create_projects_blueprint():
    bp = Blueprint("projects", __name__)
    org_service = OrgService()
    pro_service = ProjectService()
    contex = Context("", "", {})

    @bp.route("", methods=["GET"])
    def tidbcloudy_list_projects() -> [Response, int]:
        projects = [Project.from_object(contex, item) for item in CONFIG["projects"]]
        page = request.args.get("page", default=1, type=int)
        page_size = request.args.get("page_size", default=10, type=int)
        return_projects = org_service.list_projects(projects, page, page_size)
        resp = jsonify({
            "items": [item.to_object() for item in return_projects],
            "total": len(projects)
        })
        return resp, 200

    @bp.route("", methods=["POST"])
    def tidbcloudy_create_project() -> [Response, int]:
        new_project = org_service.create_project(request.json)
        CONFIG["projects"].append(new_project.to_object())
        resp = jsonify({
            "id": new_project.id
        })
        return resp, 200

    @bp.route("/<string:project_id>/aws-cmek", methods=["GET"])
    def tidbcloudy_list_project_aws_cmeks(project_id) -> [Response, int]:
        projects = CONFIG["projects"]
        project_cmeks = pro_service.list_project_aws_cmeks(projects, project_id)
        resp = jsonify({
            "items": project_cmeks
        })
        return resp, 200

    @bp.route("/<string:project_id>/aws-cmek", methods=["POST"])
    def tidbcloudy_create_project_aws_cmek(project_id) -> [Response, int]:
        projects = CONFIG["projects"]
        body = request.json
        resp = pro_service.create_project_aws_cmek(projects, project_id, body)
        if resp:
            return {}, 200
        else:
            return jsonify({
                "error": "aws cmek is not enabled"
            }), 400

    @bp.route("/<string:project_id>/clusters", methods=["GET"])
    def tidbcloudy_list_clusters(project_id) -> [Response, int]:
        clusters = [Cluster.from_object(contex, item) for item in CONFIG["clusters"]]
        page = request.args.get("page", default=1, type=int)
        page_size = request.args.get("page_size", default=10, type=int)
        return_clusters, total = pro_service.list_clusters(clusters, project_id, page, page_size)
        resp = jsonify(
            {
                "items": [item.to_object() for item in return_clusters],
                "total": total
            }
        )
        return resp, 200

    @bp.route("/<string:project_id>/clusters/<string:cluster_id>", methods=["GET"])
    def tidbcloudy_get_cluster(project_id, cluster_id) -> [Response, int]:
        clusters = [Cluster.from_object(contex, item) for item in CONFIG["clusters"]]
        cluster = pro_service.get_cluster(clusters, project_id, cluster_id)
        resp = jsonify(cluster.to_object())
        return resp, 200

    return bp
