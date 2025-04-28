from starlette.middleware.base import BaseHTTPMiddleware
import os
import logging
from fastapi import Request, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
from jose import jwt

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AuthMiddleware")

# Load configuration from environment variables
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")


class AuthMiddleware(BaseHTTPMiddleware):

    def __init__(self, app):
        super().__init__(app)
        self.skip_paths = ["/auth/login", "/auth/register", "/openapi.json", "/docs",
                           "/docs/oauth2-redirect", "/auth/register/teacher"]  # and maybe swagger docs!

    async def dispatch(self, request: Request, call_next):

        if request.url.path in self.skip_paths:
            # Skip auth check for these paths
            return await call_next(request)

        token = request.headers.get("Authorization")

        if not token:
            logger.warning(
                "Missing Authorization Header",
                extra={"method": request.method, "path": request.url.path}
            )
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Missing Authorization Header")

        if not token.startswith("Bearer "):
            logger.warning(
                "Invalid token prefix in Authorization Header",
                extra={"method": request.method, "path": request.url.path}
            )
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid token prefix")

        try:
            # Extract and decode the token
            token = token.split(" ")[1]
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            request.state.user = payload  # Store user info in request.state
            logger.info(
                "User authenticated",
                extra={"method": request.method, "path": request.url.path, "user": payload.get("sub", "Unknown")}
            )
        except jwt.ExpiredSignatureError:
            logger.error(
                "Token expired",
                extra={"method": request.method, "path": request.url.path}
            )
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Token expired")
        except jwt.InvalidTokenError:
            logger.error(
                "Invalid token",
                extra={"method": request.method, "path": request.url.path}
            )
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid token")
        except Exception as e:
            logger.exception(
                "Unexpected error during token validation",
                extra={"method": request.method, "path": request.url.path}
            )
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Authentication failed")

        # Proceed to the next middleware or route handler
        response = await call_next(request)
        return response
