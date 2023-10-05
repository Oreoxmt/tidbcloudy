from flask import Flask

app = Flask(__name__)
app.config["SERVER_NAME"] = "127.0.0.1:5000"

from mock_server.models.projects import create_projects_blueprint
from mock_server.models.clusters import create_clusters_blueprint

project_bp = create_projects_blueprint()
cluster_bp = create_clusters_blueprint()

app.register_blueprint(project_bp, url_prefix="/api/v1beta/projects")
app.register_blueprint(cluster_bp, url_prefix="/api/v1beta/clusters")

if __name__ == "__main__":
    app.run(debug=True)
