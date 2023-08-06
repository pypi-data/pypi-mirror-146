import logging
from typing import TYPE_CHECKING, Dict, Union, Generator, Any

from aiohttp import abc, hdrs, web
from aiohttp.web_exceptions import HTTPMethodNotAllowed

if TYPE_CHECKING:
    from cenao.app import Application, AppFeature


class ViewError(Exception):
    code: int
    status: int = 500
    reason_format: str = ''

    @classmethod
    def name(cls) -> str:
        return cls.__name__[:-5]

    def __repr__(self):
        return '<{} code={} reason={!r}>'.format(
            self.__class__.__name__, self.code, self.reason()
        )

    def reason(self):
        return self.reason_format.format(*self.args)

    def error_msg(self):
        return '{:d}: {}'.format(self.code, self.reason())


class ClientError(ViewError):
    code = 4000
    status = 400
    reason_format = 'Unknown client error'


class ClientUnauthorizedError(ViewError):
    code = 4001
    status = 401
    reason_format = 'Unauthorized error'


class ClientForbiddenError(ViewError):
    code = 4003
    status = 403
    reason_format = 'Forbidden error'


class ClientMethodNotAllowedError(ViewError):
    code = 4005
    status = 405
    reason_format = 'Method not allowed error'


class ClientConflictError(ViewError):
    code = 4009
    status = 409
    reason_format = 'Conflict error'


class ServerError(ViewError):
    code = 5000
    status = 500
    reason_format = 'Unknown server error'


class View(abc.AbstractView):
    ROUTE: str

    logger: logging.Logger
    ft: 'AppFeature'

    @property
    def app(self) -> 'Application':
        return self.ft.app

    @classmethod
    def init(cls, ft: 'AppFeature'):
        cls.ft = ft
        cls.logger = logging.getLogger(cls.__name__)

    @property
    def remote_ip(self) -> str:
        if xff := self.request.headers.get('X-FORWARDED-FOR', ''):
            return xff
        if xri := self.request.headers.get('X-REAL-IP', ''):
            return xri
        return self.request.remote

    async def _iter(self) -> web.StreamResponse:
        if self.request.method not in hdrs.METH_ALL:
            self._raise_allowed_methods()
        method = getattr(self, self.request.method.lower(), None)
        if method is None:
            self._raise_allowed_methods()

        try:
            resp = await method()
        except ViewError as ve:
            self.logger.warning('Got an error while handling request: %r', ve)
            return web.json_response({
                'ok': False,
                'code': ve.code,
                'error': ve.error_msg(),
                'reason': ve.reason(),
            }, status=ve.status)
        except Exception:
            self.logger.exception('Got an exception while handling request')
            e = ServerError()
            return web.json_response({
                'ok': False,
                'code': e.code,
                'error': e.error_msg(),
                'reason': e.reason(),
            }, status=e.status)
        if resp is None:
            return web.json_response({'ok': True})

        if isinstance(resp, dict):
            return web.json_response({'ok': True, 'result': resp})

        return resp

    def __await__(self) -> Generator[Any, None, abc.StreamResponse]:
        return self._iter().__await__()

    def _raise_allowed_methods(self) -> None:
        allowed_methods = {m for m in hdrs.METH_ALL if hasattr(self, m.lower())}
        raise HTTPMethodNotAllowed(self.request.method, allowed_methods)

    async def get(self) -> Union[Dict, None, web.Response]:
        pass

    async def post(self) -> Union[Dict, None, web.Response]:
        pass

    async def put(self) -> Union[Dict, None, web.Response]:
        pass

    async def delete(self) -> Union[Dict, None, web.Response]:
        pass
