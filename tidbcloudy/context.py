from requests.auth import HTTPDigestAuth
import requests
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
        self._session = requests.Session()
        self._session.auth = HTTPDigestAuth(public_key, private_key)
        self._base_url = base_url
        if self._base_url[-1] != "/":
            self._base_url += "/"

    def _call_api(self, method: str, path: str, **kwargs) -> dict:
        resp = self._session.request(method=method, url=self._base_url + path, **kwargs)
        if resp.ok:
            return resp.json()
        try:
            content = resp.json()
            raise TiDBCloudResponseException(
                resp.status_code, content.get("code"),
                resp.reason if content.get("message") is None else content["message"])
        except requests.exceptions.JSONDecodeError:
            content = resp.text
            raise TiDBCloudResponseException(resp.status_code, message=content)

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
