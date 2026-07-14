"""
routes/auth.py — Endpoint login, logout, dan info user
"""

import uuid
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException

from database import USERS, TOKENS
from models.schemas import LoginRequest
from utils.auth import get_current_user

router = APIRouter(prefix="/api/auth", tags=["Auth"])
security = HTTPBearer(auto_error=False)


@router.post("/login")
def login(req: LoginRequest):
    """Login dan dapatkan token."""
    user = USERS.get(req.email)
    if not user or user["password"] != req.password:
        raise HTTPException(status_code=401, detail="Email atau password salah")

    token = str(uuid.uuid4())
    TOKENS[token] = req.email

    return {
        "token": token,
        "user": {"name": user["name"], "email": user["email"], "role": user["role"]},
    }


@router.post("/logout")
def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Logout dan invalidate token."""
    if credentials and credentials.credentials in TOKENS:
        del TOKENS[credentials.credentials]
    return {"message": "Berhasil logout"}


@router.get("/me")
def get_me(user: dict = Depends(get_current_user)):
    """Ambil info user yang sedang login."""
    return {"name": user["name"], "email": user["email"], "role": user["role"]}