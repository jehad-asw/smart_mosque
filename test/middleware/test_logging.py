import pytest
from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.datastructures import URL
from app.middleware.logging import LoggingMiddleware
import logging

@pytest.mark.asyncio
async def test_logging_middleware_anonymous_user(caplog):
    async def mock_call_next(request: Request):
        return Response("OK")

    middleware = LoggingMiddleware(mock_call_next)
    request = Request(
        {
            "type": "http",
            "method": "GET",
            "path": "/test",
            "headers": [],
            "query_string": b"",
        }
    )
    request._url = URL("http://testserver/test")

    with caplog.at_level(logging.INFO):
        response = await middleware.dispatch(request, mock_call_next)

    assert response.status_code == 200
    assert "GET http://testserver/test by Anonymous completed in" in caplog.text


@pytest.mark.asyncio
async def test_logging_middleware_authenticated_user(caplog):
    async def mock_call_next(request: Request):
        return Response("OK")

    middleware = LoggingMiddleware(mock_call_next)
    request = Request(
        {
            "type": "http",
            "method": "POST",
            "path": "/test",
            "headers": [],
            "query_string": b"",
        }
    )
    request._url = URL("http://testserver/test")
    request.state.user = {"sub": "test_user"}

    with caplog.at_level(logging.INFO):
        response = await middleware.dispatch(request, mock_call_next)

    assert response.status_code == 200
    assert "POST http://testserver/test by test_user completed in" in caplog.text