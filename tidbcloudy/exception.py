class TiDBCloudException(Exception):
    pass


class TiDBCloudResponseException(TiDBCloudException):
    def __init__(self, status, message=None, raw=None):
        self._status = status
        self._message = message
        self._raw = raw

    @property
    def status(self):
        return self._status

    @property
    def message(self):
        return self._message

    @property
    def raw(self):
        return self._raw

    def __str__(self):
        return "status: {}, message: {}".format(self._status, self._message)
