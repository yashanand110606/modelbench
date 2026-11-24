import logging
import time
from django.conf import settings

logger = logging.getLogger("modelbench.api")


class APILoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.monotonic()
        response = self.get_response(request)
        elapsed = (time.monotonic() - start) * 1000
        logger.info(
            "%s %s -> %d %.1fms",
            request.method,
            request.path,
            response.status_code,
            elapsed,
            extra={
                "method": request.method,
                "path": request.path,
                "status": response.status_code,
                "duration_ms": round(elapsed, 1),
                "user": getattr(request.user, "username", "anonymous"),
            },
        )
        return response
