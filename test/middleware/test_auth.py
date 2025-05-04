import pytest
from fastapi import FastAPI, Request, Response
from fastapi.testclient import TestClient
from app.middleware.auth import AuthMiddleware
from app.config.security import (
    create_access_token, create_refresh_token, 
    revoke_token, MAX_LOGIN_ATTEMPTS,
    LOGIN_TIMEOUT_MINUTES
)
import time
from datetime import timedelta

app = FastAPI()
app.add_middleware(AuthMiddleware)

@app.get("/protected")
async def protected_route():
    return {"message": "This is protected"}

@app.get("/public")
async def public_route():
    return {"message": "This is public"}

client = TestClient(app)

def test_public_route_access():
    response = client.get("/public")
    assert response.status_code == 200
    assert response.json() == {"message": "This is public"}

def test_protected_route_no_token():
    response = client.get("/protected")
    assert response.status_code == 401
    assert "Missing or invalid authorization header" in response.json()["detail"]

def test_protected_route_with_valid_token():
    token = create_access_token({"sub": "test@example.com"})
    response = client.get(
        "/protected",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

def test_protected_route_with_expired_token():
    token = create_access_token(
        {"sub": "test@example.com"},
        expires_delta=timedelta(minutes=-10)
    )
    response = client.get(
        "/protected",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 401
    assert "Token validation failed" in response.json()["detail"]

def test_protected_route_with_refresh_token():
    # Create an expired access token and valid refresh token
    access_token = create_access_token(
        {"sub": "test@example.com"},
        expires_delta=timedelta(minutes=-10)
    )
    refresh_token = create_refresh_token({"sub": "test@example.com"})
    
    # First request with expired access token
    response = client.get(
        "/protected",
        headers={"Authorization": f"Bearer {access_token}"},
        cookies={"refresh_token": refresh_token}
    )
    assert response.status_code == 401
    assert response.json()["code"] == "token_expired"
    assert response.json()["should_refresh"] == True

def test_protected_route_with_revoked_token():
    token = create_access_token({"sub": "test@example.com"})
    revoke_token(token)
    
    response = client.get(
        "/protected",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 401
    assert "Token has been revoked" in response.json()["detail"]

def test_invalid_token_format():
    response = client.get(
        "/protected",
        headers={"Authorization": "InvalidFormat token123"}
    )
    assert response.status_code == 401
    assert "Missing or invalid authorization header" in response.json()["detail"]

def test_malformed_token():
    response = client.get(
        "/protected",
        headers={"Authorization": "Bearer invalid.token.format"}
    )
    assert response.status_code == 401

def test_rate_limiting():
    # Test rate limiting by simulating multiple failed login attempts
    test_app = FastAPI()
    test_app.add_middleware(AuthMiddleware)
    test_client = TestClient(test_app)
    
    # Simulate MAX_LOGIN_ATTEMPTS failed attempts
    for _ in range(MAX_LOGIN_ATTEMPTS):
        response = test_client.post(
            "/auth/login",
            json={"email": "test@example.com", "password": "wrong"}
        )
    
    # Next attempt should be rate limited
    response = test_client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "wrong"}
    )
    assert response.status_code == 429
    assert str(LOGIN_TIMEOUT_MINUTES) in response.json()["detail"]


