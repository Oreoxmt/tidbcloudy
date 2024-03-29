import uuid
from datetime import datetime
from typing import List, Union

from httpx import HTTPStatusError, Request, Response

from tidbcloudy.cluster import Cluster
from tidbcloudy.context import Context
from tidbcloudy.specification import CloudSpecification, ClusterStatus, TiDBComponent, TiFlashComponent, TiKVComponent

VALID_COMPONENTS = {
    "tidb": {"class": TiDBComponent, "attributes": {"node_size", "node_quantity"}},
    "tikv": {"class": TiKVComponent, "attributes": {"node_size", "node_quantity", "storage_size_gib"}},
    "tiflash": {"class": TiFlashComponent, "attributes": {"node_size", "node_quantity", "storage_size_gib"}},
}


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
    def create_project_aws_cmek(projects: List[dict], project_id: str, body: dict) -> None:
        project_index = ProjectService._get_project_index_by_id(projects, project_id)
        if project_index is None or projects[project_index].get("aws_cmek_enabled") is False:
            raise HTTPStatusError(
                "", request=Request("POST", ""), response=Response(400, text="aws cmek is not enabled")
            )
        project_cmek = projects[project_index].get("aws_cmek", [])
        for create_cmek in body.get("specs", []):
            current_cmek = {
                "region": create_cmek["region"],
                "kms_arn": create_cmek["kms_arn"],
            }
            project_cmek.append(current_cmek)
        projects[project_index].update({"aws_cmek": project_cmek})

    @staticmethod
    def list_provider_regions(provider_regions: List[CloudSpecification]) -> List[CloudSpecification]:
        return provider_regions

    @staticmethod
    def list_clusters(clusters: List[Cluster], project_id: str, page: int, page_size: int) -> [List[Cluster], int]:
        current_clusters = []
        for cluster in clusters:
            if cluster.project_id == project_id:
                current_clusters.append(cluster)
        return_clusters = current_clusters[page_size * (page - 1) : page_size * page]
        total = len(current_clusters)
        return return_clusters, total

    def create_cluster(self, project_id: str, body: dict) -> Cluster:
        body["id"] = str(uuid.uuid4().int % (10**19))
        body["project_id"] = project_id
        body["create_timestamp"] = str(int(datetime.now().timestamp()))
        body["status"] = {
            "tidb_version": "v0.0.0",
            "cluster_status": ClusterStatus.AVAILABLE.value,
            "connection_strings": {
                "default_user": "root",
                "standard": {"host": "gateway01.prod.aws.tidbcloud.com", "port": 4000},
                "vpc_peering": {"host": "gateway01-privatelink.prod.aws.tidbcloud.com", "port": 4000},
            },
        }
        if body["config"].get("port") is None:
            body["config"]["port"] = 4000
        new_cluster = Cluster.from_object(self._context, body)
        return new_cluster

    @staticmethod
    def get_cluster(clusters: List[Cluster], project_id: str, cluster_id: str) -> Cluster:
        for cluster in clusters:
            if cluster.project_id == project_id and cluster.id == cluster_id:
                return cluster
        raise HTTPStatusError(
            "", request=Request("GET", ""), response=Response(400, text=f"Cluster {cluster_id} not found")
        )

    def delete_cluster(self, clusters: List[Cluster], project_id: str, cluster_id: str) -> List[Cluster]:
        delete_cluster = self.get_cluster(clusters, project_id, cluster_id)
        clusters.remove(delete_cluster)
        return clusters

    @staticmethod
    def _get_component(cluster: Cluster, component_name: str):
        if component_name not in VALID_COMPONENTS:
            raise HTTPStatusError(
                "",
                request=Request("GET", ""),
                response=Response(400, text=f"Component {component_name} is not supported"),
            )
        component = getattr(cluster.config.components, component_name)
        if component is None:
            init_component = VALID_COMPONENTS[component_name]["class"]
            component = init_component()
            setattr(cluster.config.components, component_name, component)
        return component

    @staticmethod
    def _update_components(cluster: Cluster, components_config: dict) -> Cluster:
        for component, config in components_config.items():
            valid_attrs = VALID_COMPONENTS.get(component, {}).get("attributes", set())
            for attribute, value in config.items():
                if attribute not in valid_attrs:
                    raise HTTPStatusError(
                        "",
                        request=Request("POST", ""),
                        response=Response(400, text=f"Attribute {attribute} is not supported"),
                    )
                setattr(ProjectService._get_component(cluster, component), attribute, value)
        return cluster

    @staticmethod
    def _pause_resume_cluster(cluster: Cluster, config) -> Cluster:
        if not isinstance(config, bool):
            raise HTTPStatusError(
                "", request=Request("POST", ""), response=Response(400, text="The paused config must be a boolean")
            )
        current_status = cluster.status.cluster_status
        if config and current_status == ClusterStatus.AVAILABLE:
            cluster.status.cluster_status = ClusterStatus.PAUSED
        elif not config and current_status == ClusterStatus.PAUSED:
            cluster.status.cluster_status = ClusterStatus.AVAILABLE
        else:
            raise HTTPStatusError(
                "", request=Request("POST", ""), response=Response(400, text="The cluster cannot be paused or resumed")
            )
        return cluster

    def update_cluster(self, clusters: List[Cluster], project_id: str, cluster_id: str, body: dict) -> List[Cluster]:
        update_cluster = self.get_cluster(clusters, project_id, cluster_id)
        config = body.get("config", {})
        components = config.get("components", {})
        update_cluster = ProjectService._update_components(update_cluster, components)
        is_paused_config = config.get("paused")
        if is_paused_config is not None:
            ProjectService._pause_resume_cluster(update_cluster, is_paused_config)
        for index, cluster in enumerate(clusters):
            if cluster.project_id == project_id and cluster.id == cluster_id:
                clusters[index] = update_cluster
                break
        return clusters
