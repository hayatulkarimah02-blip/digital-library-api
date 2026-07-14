"""
utils/auth.py — Token helper & dependency untuk FastAPI
"""

from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from database import TOKENS, USERS

security = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """Dependency: validasi token dan return user yang sedang login."""
    if not credentials:
        raise HTTPException(status_code=401, detail="Token tidak ditemukan")

    email = TOKENS.get(credentials.credentials)
    if not email:
        raise HTTPException(status_code=401, detail="Token tidak valid atau sudah expired")

    user = USERS.get(email)
    if not user:
        raise HTTPException(status_code=401, detail="User tidak ditemukan")

    return user


def require_admin(user: dict = Depends(get_current_user)):
    """Dependency: pastikan user punya role admin."""
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Akses ditolak: butuh role admin")
    return user