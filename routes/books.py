"""
routes/books.py — CRUD buku + filter, sort, statistik
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, Depends

from database import BOOKS, ORDERS
from models.schemas import BookCreate, UpdatePriceRequest, UpdateStockRequest
from utils.auth import get_current_user, require_admin

router = APIRouter(prefix="/api/books", tags=["Buku"])


@router.get("")
def get_books(
    category: Optional[str] = None,
    search: Optional[str] = None,
    sort: Optional[str] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
):
    """
    Ambil daftar buku dengan filter & sort opsional.
    - category: Fiksi | Non-fiksi | Pengembangan Diri | Sains
    - search: judul atau nama penulis
    - sort: price-asc | price-desc | rating | popular
    - min_price / max_price: filter rentang harga
    """
    books = BOOKS.copy()

    if category and category != "Semua":
        books = [b for b in books if b["category"] == category]

    if search:
        q = search.lower()
        books = [b for b in books if q in b["title"].lower() or q in b["author"].lower()]

    if min_price is not None:
        books = [b for b in books if b["price"] >= min_price]

    if max_price is not None:
        books = [b for b in books if b["price"] <= max_price]

    sort_keys = {
        "price-asc":  (lambda b: b["price"],  False),
        "price-desc": (lambda b: b["price"],  True),
        "rating":     (lambda b: b["rating"], True),
        "popular":    (lambda b: b["sold"],   True),
    }
    if sort in sort_keys:
        key_fn, reverse = sort_keys[sort]
        books.sort(key=key_fn, reverse=reverse)

    return {"data": books, "total": len(books)}


@router.get("/categories")
def get_categories():
    """Ambil daftar kategori unik yang tersedia."""
    cats = sorted(set(b["category"] for b in BOOKS))
    return {"data": cats}


@router.get("/{book_id}")
def get_book(book_id: int):
    """Ambil detail satu buku berdasarkan ID."""
    book = next((b for b in BOOKS if b["id"] == book_id), None)
    if not book:
        raise HTTPException(status_code=404, detail="Buku tidak ditemukan")
    return book


@router.post("", status_code=201)
def create_book(book: BookCreate, _: dict = Depends(require_admin)):
    """Tambah buku baru. Butuh auth admin."""
    new_id = max((b["id"] for b in BOOKS), default=0) + 1
    new_book = {"id": new_id, "sold": 0, **book.model_dump()}
    BOOKS.append(new_book)
    return {"message": "Buku berhasil ditambahkan", "data": new_book}


@router.patch("/{book_id}/price")
def update_price(
    book_id: int,
    req: UpdatePriceRequest,
    _: dict = Depends(require_admin),
):
    """Update harga buku. Butuh auth admin."""
    book = next((b for b in BOOKS if b["id"] == book_id), None)
    if not book:
        raise HTTPException(status_code=404, detail="Buku tidak ditemukan")
    if req.price <= 0:
        raise HTTPException(status_code=400, detail="Harga harus lebih dari 0")

    old_price = book["price"]
    book["price"] = req.price
    return {
        "message": f"Harga diperbarui: Rp {old_price:,} → Rp {req.price:,}",
        "data": book,
    }


@router.patch("/{book_id}/stock")
def update_stock(
    book_id: int,
    req: UpdateStockRequest,
    _: dict = Depends(require_admin),
):
    """Update stok buku. Butuh auth admin."""
    book = next((b for b in BOOKS if b["id"] == book_id), None)
    if not book:
        raise HTTPException(status_code=404, detail="Buku tidak ditemukan")
    if req.stock < 0:
        raise HTTPException(status_code=400, detail="Stok tidak boleh negatif")

    book["stock"] = req.stock
    return {"message": "Stok diperbarui", "data": book}


@router.delete("/{book_id}")
def delete_book(book_id: int, _: dict = Depends(require_admin)):
    """Hapus buku. Butuh auth admin."""
    book = next((b for b in BOOKS if b["id"] == book_id), None)
    if not book:
        raise HTTPException(status_code=404, detail="Buku tidak ditemukan")

    BOOKS.remove(book)
    return {"message": f'Buku "{book["title"]}" berhasil dihapus'}


@router.get("/stats/summary")
def get_stats(_: dict = Depends(require_admin)):
    """Statistik toko. Butuh auth admin."""
    total_revenue = sum(o["total"] for o in ORDERS)
    low_stock     = [b for b in BOOKS if b["stock"] <= 5]
    top_selling   = sorted(BOOKS, key=lambda b: b["sold"], reverse=True)[:3]

    return {
        "total_revenue":  total_revenue,
        "total_orders":   len(ORDERS),
        "total_books":    len(BOOKS),
        "low_stock_count": len(low_stock),
        "low_stock_books": low_stock,
        "top_selling":    top_selling,
    }