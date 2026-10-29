"""Autentikasi: hashing password (bcrypt), JWT, dan dependency pengguna aktif."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

import db
from config import get_settings

settings = get_settings()

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 12  # 12 jam

_bearer = HTTPBearer(auto_error=False)

_UNAUTHORIZED = {"WWW-Authenticate": "Bearer"}


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except ValueError:
        return False


def create_access_token(user_id: str, username: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "username": username,
        "iat": now,
        "exp": now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=ALGORITHM)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> dict:
    """Decode Bearer token dan kembalikan baris pengguna dari PostgreSQL."""
    if credentials is None:
        raise HTTPException(status_code=401, detail="Token tidak ditemukan", headers=_UNAUTHORIZED)
    try:
        payload = jwt.decode(credentials.credentials, settings.jwt_secret, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401,
            detail="Token tidak valid atau kedaluwarsa",
            headers=_UNAUTHORIZED,
        )
    user = await db.get_user_by_id(payload.get("sub", ""))
    if user is None:
        raise HTTPException(status_code=401, detail="Pengguna tidak ditemukan", headers=_UNAUTHORIZED)
    return user
