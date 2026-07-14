"""
models/schemas.py — Pydantic models untuk validasi request & response
"""

from pydantic import BaseModel


# ── Auth ───────────────────────────────────────────────────────────
class LoginRequest(BaseModel):
    email: str
    password: str


# ── Buku ───────────────────────────────────────────────────────────
class BookCreate(BaseModel):
    title: str
    author: str
    category: str
    price: int
    stock: int
    cover: str
    desc: str
    rating: float = 0.0


class UpdatePriceRequest(BaseModel):
    price: int


class UpdateStockRequest(BaseModel):
    stock: int


# ── Pesanan ────────────────────────────────────────────────────────
class OrderItem(BaseModel):
    book_id: int
    qty: int


class CheckoutRequest(BaseModel):
    name: str
    email: str
    address: str
    payment: str
    items: list[OrderItem]