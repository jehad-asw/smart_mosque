import pytest
from datetime import datetime, timedelta
from jose import jwt
from app.config.security import (
    hash_password, verify_password, create_access_token,
    create_refresh_token, verify_token, validate_password,
    create_token_pair, revoke_token, SECRET_KEY, REFRESH_SECRET_KEY,
    ALGORITHM, PASSWORD_REGEX
)

def test_password_hashing():
    password = "TestPassword123!"
    hashed = hash_password(password)
    assert verify_password(password, hashed)
    assert not verify_password("wrong_password", hashed)

def test_password_validation():
    # Valid passwords
    assert validate_password("StrongPass123!")
    assert validate_password("Complex@Pass99")
    
    # Invalid passwords
    assert not validate_password("weak")  # Too short
    assert not validate_password("NoSpecialChar123")  # No special char
    assert not validate_password("NoNumber@abc")  # No number
    assert not validate_password("12345@789")  # No letter

def test_access_token_creation():
    data = {"sub": "test@example.com", "role": "student"}
    token = create_access_token(data)
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded["sub"] == data["sub"]
    assert decoded["role"] == data["role"]
    assert decoded["token_type"] == "access"
    assert "exp" in decoded

def test_refresh_token_creation():
    data = {"sub": "test@example.com", "role": "student"}
    token = create_refresh_token(data)
    decoded = jwt.decode(token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded["sub"] == data["sub"]
    assert decoded["role"] == data["role"]
    assert decoded["token_type"] == "refresh"
    assert "exp" in decoded

def test_token_pair_creation():
    data = {"sub": "test@example.com", "role": "student"}
    access_token, refresh_token = create_token_pair(data)
    
    # Verify access token
    access_decoded = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    assert access_decoded["token_type"] == "access"
    
    # Verify refresh token
    refresh_decoded = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
    assert refresh_decoded["token_type"] == "refresh"

def test_token_expiration():
    data = {"sub": "test@example.com"}
    expired_token = create_access_token(
        data, expires_delta=timedelta(minutes=-10)
    )
    with pytest.raises(jwt.ExpiredSignatureError):
        verify_token(expired_token)

def test_token_revocation():
    data = {"sub": "test@example.com"}
    token = create_access_token(data)
    
    # Token should be valid initially
    assert verify_token(token)
    
    # Revoke token
    revoke_token(token)
    
    # Token should be invalid after revocation
    with pytest.raises(jwt.JWTError) as exc:
        verify_token(token)
    assert "Token has been revoked" in str(exc.value)

def test_invalid_token():
    invalid_token = "invalid.token.string"
    with pytest.raises(jwt.JWTError):
        verify_token(invalid_token)

def test_password_regex():
    import re
    # Test password regex pattern
    valid_passwords = [
        "StrongPass123!",
        "Complex@Pass99",
        "Test123$Test",
        "Abcd123!@#"
    ]
    invalid_passwords = [
        "weak",  # Too short
        "NoSpecialChar123",
        "NoNumber@abc",
        "12345@789",
        "no_upper_case@123"
    ]
    
    for password in valid_passwords:
        assert re.match(PASSWORD_REGEX, password)
    
    for password in invalid_passwords:
        assert not re.match(PASSWORD_REGEX, password)