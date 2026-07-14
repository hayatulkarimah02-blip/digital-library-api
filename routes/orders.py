"""
routes/orders.py — Checkout dan manajemen pesanan
"""

import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends

from database import BOOKS, ORDERS
from models.schemas import CheckoutRequest
from utils.auth import require_admin

router = APIRouter(prefix="/api/orders", tags=["Pesanan"])


@router.post("", status_code=201)
def checkout(req: CheckoutRequest):
    """
    Buat pesanan baru.
    - Validasi stok tiap item sebelum proses
    - Kurangi stok & tambah sold setelah berhasil
    """
    order_items = []
    total = 0

    # ── Validasi semua item dulu sebelum mutasi data ───────────────
    for item in req.items:
        book = next((b for b in BOOKS if b["id"] == item.book_id), None)
        if not book:
            raise HTTPException(
                status_code=404,
                detail=f"Buku ID {item.book_id} tidak ditemukan",
            )
        if item.qty <= 0:
            raise HTTPException(
                status_code=400,
                detail=f"Jumlah item harus lebih dari 0",
            )
        if book["stock"] < item.qty:
            raise HTTPException(
                status_code=400,
                detail=f'Stok "{book["title"]}" tidak cukup (tersisa {book["stock"]})',
            )

        subtotal = book["price"] * item.qty
        total += subtotal
        order_items.append({
            "book_id":  book["id"],
            "title":    book["title"],
            "author":   book["author"],
            "price":    book["price"],
            "qty":      item.qty,
            "subtotal": subtotal,
        })

    # ── Semua valid — kurangi stok & tambah sold ───────────────────
    for item in req.items:
        book = next(b for b in BOOKS if b["id"] == item.book_id)
        book["stock"] -= item.qty
        book["sold"]  += item.qty

    order = {
        "order_id":   f"LMR-{str(uuid.uuid4())[:8].upper()}",
        "customer":   {
            "name":    req.name,
            "email":   req.email,
            "address": req.address,
        },
        "payment":    req.payment,
        "items":      order_items,
        "total":      total,
        "status":     "confirmed",
        "created_at": datetime.now().isoformat(),
    }
    ORDERS.append(order)

    return {
        "message":  "Pesanan berhasil dibuat!",
        "order_id": order["order_id"],
        "total":    total,
        "status":   "confirmed",
    }


@router.get("")
def get_all_orders(_: dict = Depends(require_admin)):
    """Lihat semua pesanan. Butuh auth admin."""
    return {"data": ORDERS, "total": len(ORDERS)}


@router.get("/{order_id}")
def get_order(order_id: str):
    """Ambil detail satu pesanan berdasarkan order_id."""
    order = next((o for o in ORDERS if o["order_id"] == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Pesanan tidak ditemukan")
    return order


@router.patch("/{order_id}/status")
def update_order_status(
    order_id: str,
    status: str,
    _: dict = Depends(require_admin),
):
    """
    Update status pesanan. Butuh auth admin.
    Status: confirmed | processing | shipped | delivered | cancelled
    """
    valid_statuses = {"confirmed", "processing", "shipped", "delivered", "cancelled"}
    if status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Status tidak valid. Pilihan: {', '.join(valid_statuses)}",
        )

    order = next((o for o in ORDERS if o["order_id"] == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Pesanan tidak ditemukan")

    order["status"] = status
    return {"message": f"Status pesanan diperbarui ke '{status}'", "data": order}