class TiDBCloudException(Exception):
    pass


class TiDBCloudResponseException(TiDBCloudException):
    def __init__(self, status, code=None, message=None, raw=None):
        self._status = status
        self._code = code
        self._message = message
        self._raw = raw

    @property
    def status(self):
        return self._status

    @property
    def code(self):
        return self._code

    @property
    def message(self):
        return self._message

    @property
    def raw(self):
        return self._raw

    def __str__(self):
        return "status: {}, code: {}, message: {}".format(self._status, self._code, self._message)
