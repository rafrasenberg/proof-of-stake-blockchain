from starlette.middleware.base import BaseHTTPMiddleware

from blockchain.utils.logger import logger


class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        logger.info(
            f"{request.method} {response.status_code} {request.url.path}",
            extra={
                "http": {
                    "method": request.method,
                    "url": str(request.url),
                    "status_code": response.status_code,
                }
            },
        )
        return response
