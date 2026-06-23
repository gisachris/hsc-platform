import logging
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("api.middleware")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(
            f"Method: {request.method} | "
            f"Path: {request.url.path} | "
            f"Status Code: {response.status_code} | "
            f"Duration: {process_time:.4f}s"
        )
        response.headers["X-Process-Time"] = f"{process_time:.4f}s"
        return response
