import time

from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.types import ASGIApp


class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000

        client_ip = self._client_ip(request)
        logger.info(
            "client_ip={} method={} path={} status={} duration_ms={:.2f} "
            "user_agent={!r} content_type={!r} api_key_present={}",
            client_ip,
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
            request.headers.get("user-agent", "-"),
            request.headers.get("content-type", "-"),
            "X-API-Key" in request.headers,
        )
        return response

    @staticmethod
    def _client_ip(request: Request) -> str:
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()

        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip.strip()

        return request.client.host if request.client else "-"
