import json
import time
import uuid
from datetime import datetime, timezone
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import StreamingResponse


class SecurityAndRequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 1. Generate Request ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        # Measure duration
        start_time = time.time()
        response: Response = await call_next(request)
        process_time = time.time() - start_time

        # 2. Inject headers
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{process_time:.4f}s"

        # Security Headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers[
            "Content-Security-Policy"
        ] = "default-src 'self'; frame-ancestors 'none';"

        # 3. Dynamic Response Envelope Enrichment for JSON responses
        content_type = response.headers.get("content-type", "")
        if "application/json" in content_type and not isinstance(
            response, StreamingResponse
        ):
            # Read body and inject meta if necessary
            try:
                # Standard fastapi Response allows reading body if it's not streamed
                body = [section async for section in response.body_iterator]
                response.body_iterator = iterate_in_threadpool(iter(body))
                data = json.loads(body[0].decode("utf-8"))

                # Inject metadata envelope
                if isinstance(data, dict):
                    if "meta" not in data or data["meta"] is None:
                        data["meta"] = {
                            "requestId": request_id,
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                        }
                    # Re-serialize
                    new_content = json.dumps(data).encode("utf-8")
                    response.headers["Content-Length"] = str(len(new_content))
                    return Response(
                        content=new_content,
                        status_code=response.status_code,
                        headers=dict(response.headers),
                        media_type="application/json",
                    )
            except Exception:
                # Fail-safe: if something goes wrong, return original response
                pass

        return response


# Helper to re-stream body iterator if read
from anyio.to_thread import run_sync


async def iterate_in_threadpool(iterator):
    for item in iterator:
        yield item
