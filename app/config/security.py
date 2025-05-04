from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Dict, Optional, Union, Tuple
import os
import secrets
from pydantic import BaseModel, constr
from collections import defaultdict

# Replace Redis-based session and token management with in-memory storage
revoked_tokens = defaultdict(int)
user_sessions = defaultdict(dict)
failed_login_attempts = defaultdict(list)

# Replace Redis functions with in-memory implementations
def add_to_revoked_tokens(token: str, ttl: int):
    revoked_tokens[token] = ttl

def is_token_revoked(token: str) -> bool:
    return token in revoked_tokens

def add_failed_login_attempt(email: str, ttl: int):
    failed_login_attempts[email].append(datetime.utcnow().timestamp())

def get_failed_attempts(email: str) -> int:
    now = datetime.utcnow().timestamp()
    failed_login_attempts[email] = [
        attempt for attempt in failed_login_attempts[email]
        if now - attempt < ttl
    ]
    return len(failed_login_attempts[email])

def clear_failed_attempts(email: str):
    if email in failed_login_attempts:
        del failed_login_attempts[email]

def store_user_session(user_id: str, token: str, ttl: int):
    user_sessions[user_id] = {"token": token, "expires_at": datetime.utcnow().timestamp() + ttl}

def get_user_session(user_id: str):
    session = user_sessions.get(user_id)
    if session and session["expires_at"] > datetime.utcnow().timestamp():
        return session["token"]
    return None

def remove_user_session(user_id: str):
    if user_id in user_sessions:
        del user_sessions[user_id]

# Security settings
SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY", secrets.token_urlsafe(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

# Password requirements
MIN_PASSWORD_LENGTH = 8
PASSWORD_REGEX = r"^(?=.*[A-Za-z])(?=.*\d).{8,}$"

# Rate limiting settings
MAX_LOGIN_ATTEMPTS = 5
LOGIN_TIMEOUT_MINUTES = 15

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12
)

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    email: str
    user_id: int
    role: str
    exp: datetime

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed: str) -> bool:
    return pwd_context.verify(plain_password, hashed)

def validate_password(password: str) -> bool:
    """Validate password meets security requirements"""
    import re
    if len(password) < MIN_PASSWORD_LENGTH:
        return False
    if not re.match(PASSWORD_REGEX, password):
        return False
    return True

def create_token_pair(data: dict) -> Tuple[str, str]:
    """Create both access and refresh tokens"""
    access_token = create_access_token(data)
    refresh_token = create_refresh_token(data)
    
    # Store user session
    if "user_id" in data:
        store_user_session(
            str(data["user_id"]),
            access_token,
            ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    
    return access_token, refresh_token

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "token_type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
    to_encode.update({"exp": expire, "token_type": "refresh"})
    return jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str, is_refresh_token: bool = False) -> Dict:
    """Verify token and return payload"""
    if is_token_revoked(token):
        raise JWTError("Token has been revoked")
        
    try:
        secret = REFRESH_SECRET_KEY if is_refresh_token else SECRET_KEY
        payload = jwt.decode(token, secret, algorithms=[ALGORITHM])
        
        # Verify token type
        if payload.get("token_type") != ("refresh" if is_refresh_token else "access"):
            raise JWTError("Invalid token type")
            
        return payload
    except JWTError as e:
        raise JWTError(f"Token validation failed: {str(e)}")

def revoke_token(token: str):
    """Add token to revoked tokens in Redis"""
    try:
        # Decode token to get expiration
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp = payload.get("exp")
        if exp:
            # Calculate remaining time
            now = datetime.utcnow().timestamp()
            ttl = max(int(exp - now), 0)  # Ensure positive TTL
            add_to_revoked_tokens(token, ttl)
            
            # If revoking access token, also remove user session
            if "user_id" in payload:
                remove_user_session(str(payload["user_id"]))
    except JWTError:
        # If token is invalid, still add it to revoked tokens with default expiry
        add_to_revoked_tokens(token, ACCESS_TOKEN_EXPIRE_MINUTES * 60)

def check_rate_limit(email: str) -> None:
    """Check if user has exceeded login attempts using Redis"""
    attempts = get_failed_attempts(email)
    if attempts >= MAX_LOGIN_ATTEMPTS:
        raise JWTError(f"Too many login attempts. Please try again after {LOGIN_TIMEOUT_MINUTES} minutes")

def record_failed_attempt(email: str):
    """Record failed login attempt in Redis"""
    add_failed_login_attempt(email, LOGIN_TIMEOUT_MINUTES * 60)

def clear_rate_limit(email: str):
    """Clear failed login attempts for email"""
    clear_failed_attempts(email)
