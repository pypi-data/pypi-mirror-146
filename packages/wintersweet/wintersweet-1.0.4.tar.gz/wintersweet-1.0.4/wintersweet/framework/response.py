from fastapi.responses import UJSONResponse

from wintersweet.framework.middlewares import RequestIDMiddleware


class Response(UJSONResponse):
    def __init__(self, content=None, code=0, status_code=200, extra=None, *args, **kwargs):
        self._code = code
        self._msg = None
        try:
            self._msg = self.build_msg()
        except Exception:
            if code == 0:
                self._msg = 'Success'
            else:
                self._msg = 'Unknown Error'

        self._data = content
        self._extra = extra
        self._request_id = RequestIDMiddleware.get_request_id()

        super().__init__(content=content, status_code=status_code, *args, **kwargs)

    def build_msg(self):
        raise InterruptedError()

    @property
    def data(self):
        return self._data

    def render(self, content):
        return super().render(
            dict(code=self._code, data=content, msg=self._msg, request_id=self._request_id, extra=self._extra)
        )

    @classmethod
    def response_success(cls, data=None):

        return cls(content=data)

    @classmethod
    def response_error(cls, code=-1, status_code=400, extra=None, *args, **kwargs):
        return cls(code=code, status_code=status_code, extra=extra, *args, **kwargs)

    def __bool__(self):

        return self._code == 0


class ErrResponse(Response, Exception):
    pass
