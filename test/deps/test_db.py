import pytest
from fastapi import HTTPException, status
from jose import jwt
from sqlalchemy.orm import Session
from unittest.mock import MagicMock, patch
from app.deps.db import get_current_user, require_role
from app.models.user import User, Role
from app.config.security import SECRET_KEY, ALGORITHM

# Mock data
mock_user = User(id=1, email="test@example.com", role=Role.admin)
mock_token_payload = {
    "sub": mock_user.email,
    "user_id": mock_user.id,
    "role": mock_user.role.value
}
mock_token = jwt.encode(mock_token_payload, SECRET_KEY, algorithm=ALGORITHM)

# Test get_current_user
def test_get_current_user_valid_token():
    db = MagicMock(spec=Session)
    db.query.return_value.filter.return_value.first.return_value = mock_user

    with patch("app.deps.db.jwt.decode", return_value=mock_token_payload):
        user = get_current_user(token=mock_token, db=db)
        assert user == mock_user

def test_get_current_user_invalid_token():
    db = MagicMock(spec=Session)

    with patch("app.deps.db.jwt.decode", side_effect=Exception):
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(token="invalid_token", db=db)
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_current_user_user_not_found():
    db = MagicMock(spec=Session)
    db.query.return_value.filter.return_value.first.return_value = None

    with patch("app.deps.db.jwt.decode", return_value=mock_token_payload):
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(token=mock_token, db=db)
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED

# Test require_role
def test_require_role_valid_role():
    dependency = require_role(Role.ADMIN)
    current_user = MagicMock(role=Role.ADMIN)

    result = dependency(current_user=current_user)
    assert result == current_user

def test_require_role_invalid_role():
    dependency = require_role(Role.ADMIN)
    current_user = MagicMock(role=Role.USER)

    with pytest.raises(HTTPException) as exc_info:
        dependency(current_user=current_user)
    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN