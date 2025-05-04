from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from app.config.security import verify_token, Token
from app.deps.db import get_db
from fastapi.responses import JSONResponse
import time
from typing import Optional

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Public paths that don't require authentication
        public_paths = {
            "/auth/login",
            "/auth/register",
            "/auth/register/teacher",
            "/auth/register/student",
            "/auth/register/parent",
            "/docs",
            "/redoc",
            "/openapi.json"
        }
        
        if request.url.path in public_paths:
            return await call_next(request)

        try:
            # Check for token in headers
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Missing or invalid authorization header",
                    headers={"WWW-Authenticate": "Bearer"}
                )

            token = auth_header.split(" ")[1]
            
            # Verify token
            try:
                payload = verify_token(token)
                # Add user info to request state for later use
                request.state.user = payload
            except Exception as e:
                # If access token is expired, check for refresh token
                refresh_token = request.cookies.get("refresh_token")
                if refresh_token and request.url.path != "/auth/refresh":
                    # Redirect to refresh endpoint
                    return JSONResponse(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        content={
                            "detail": "Token expired",
                            "code": "token_expired",
                            "should_refresh": True
                        }
                    )
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=str(e),
                    headers={"WWW-Authenticate": "Bearer"}
                )

            response = await call_next(request)
            return response

        except HTTPException as exc:
            return JSONResponse(
                status_code=exc.status_code,
                content={"detail": exc.detail},
                headers=exc.headers
            )
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "Internal server error"}
            )
