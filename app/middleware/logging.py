from starlette.middleware.base import BaseHTTPMiddleware
import time
from fastapi import Request
import logging


class LoggingMiddleware(BaseHTTPMiddleware):
     async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        user = getattr(request.state, "user", None)
        user_info = user.get("sub") if user else "Anonymous"
        response = await call_next(request)
        duration = time.time() - start_time
        logging.info(f"{request.method} {request.url} by {user_info} completed in {duration:.2f}s")
        return response