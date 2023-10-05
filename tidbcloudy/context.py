import httpx

from tidbcloudy.exception import TiDBCloudResponseException


class Context:

    def __init__(self, public_key: str, private_key: str, server_config: dict):
        """
        Args:
            public_key: your public key to access to TiDB Cloud
            private_key: your private key to access to TiDB Cloud
            server_config: the server configuration dict to access to TiDB Cloud
        """
        self._client = httpx.Client()
        self._client.auth = httpx.DigestAuth(public_key, private_key)
        self._server_config = server_config

    def _call_api(self, method: str, path: str, server: str, **kwargs) -> dict:
        base_url = self._server_config.get(server)
        if base_url[-1] != "/":
            base_url += "/"
        try:
            resp = self._client.request(method=method, url=base_url + path, **kwargs)
            resp.raise_for_status()
            return resp.json()
        except httpx.RequestError as exc:
            raise TiDBCloudResponseException(status="Error",
                                             message=f"An error occurred when requesting {exc.request.url}")
        except httpx.HTTPStatusError as exc:
            raise TiDBCloudResponseException(status=exc.response.status_code, message=exc.response.text)

    def call_get(self, server: str, path: str,
                 *,
                 params: dict = None) -> dict:
        resp = self._call_api(method="GET", path=path, server=server, params=params)
        return resp

    def call_post(self, server: str, path: str,
                  *,
                  data: dict = None,
                  json: dict = None) -> dict:
        resp = self._call_api(method="POST", path=path, server=server, data=data, json=json)
        return resp

    def call_patch(self, server: str, path: str,
                   *,
                   data: dict = None,
                   json: dict = None) -> dict:
        resp = self._call_api(method="PATCH", path=path, server=server, data=data, json=json)
        return resp

    def call_delete(self, server: str, path: str) -> dict:
        resp = self._call_api(method="DELETE", server=server, path=path)
        return resp
