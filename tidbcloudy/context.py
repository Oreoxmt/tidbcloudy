import httpx
from tidbcloudy.exception import TiDBCloudResponseException


class Context:
    def __init__(self,
                 public_key: str,
                 private_key: str,
                 *,
                 base_url: str = "https://api.tidbcloud.com/api/v1beta/"
                 ):
        """
        Args:
            public_key: your public key to access to TiDB Cloud
            private_key: your private key to access to TiDB Cloud
            base_url: the base_url of TiDB Cloud API, you can change this for internal testing.
        """
        self._client = httpx.Client()
        self._client.auth = httpx.DigestAuth(public_key, private_key)
        self._base_url = base_url
        if self._base_url[-1] != "/":
            self._base_url += "/"

    def _call_api(self, method: str, path: str, **kwargs) -> dict:
        try:
            resp = self._client.request(method=method, url=self._base_url + path, **kwargs)
            resp.raise_for_status()
            return resp.json()
        except httpx.RequestError as exc:
            raise TiDBCloudResponseException(status="Error",
                                             message=f"An error occurred when requesting {exc.request.url}")
        except httpx.HTTPStatusError as exc:
            raise TiDBCloudResponseException(status=exc.response.status_code, message=exc.response.text)

    def call_get(self, path: str, *, params: dict = None) -> dict:
        resp = self._call_api(method="GET", path=path, params=params)
        return resp

    def call_post(self, path: str, *, data: dict = None, json: dict = None) -> dict:
        resp = self._call_api(method="POST", path=path, data=data, json=json)
        return resp

    def call_patch(self, path: str, *, data: dict = None, json: dict = None) -> dict:
        resp = self._call_api(method="PATCH", path=path, data=data, json=json)
        return resp

    def call_delete(self, path) -> dict:
        resp = self._call_api(method="DELETE", path=path)
        return resp
