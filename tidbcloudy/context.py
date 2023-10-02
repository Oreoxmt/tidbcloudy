import httpx

from tidbcloudy.baseURL import V1BETA
from tidbcloudy.exception import TiDBCloudResponseException


class Context:
    def __init__(self, public_key: str, private_key: str):
        """
        Args:
            public_key: your public key to access to TiDB Cloud
            private_key: your private key to access to TiDB Cloud
        """
        self._client = httpx.Client()
        self._client.auth = httpx.DigestAuth(public_key, private_key)

    def _call_api(self, method: str, path: str, base_url: str, **kwargs) -> dict:
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

    def call_get(self, path: str, base_url: str = V1BETA.HOST.value,
                 *,
                 params: dict = None) -> dict:
        resp = self._call_api(method="GET", path=path, base_url=base_url, params=params)
        return resp

    def call_post(self, path: str, base_url: str = V1BETA.HOST.value,
                  *,
                  data: dict = None,
                  json: dict = None) -> dict:
        resp = self._call_api(method="POST", path=path, base_url=base_url, data=data, json=json)
        return resp

    def call_patch(self, path: str, base_url: str = V1BETA.HOST.value,
                   *,
                   data: dict = None,
                   json: dict = None) -> dict:
        resp = self._call_api(method="PATCH", path=path, base_url=base_url, data=data, json=json)
        return resp

    def call_delete(self, path: str, base_url: str = V1BETA.HOST.value) -> dict:
        resp = self._call_api(method="DELETE", base_url=base_url, path=path)
        return resp
