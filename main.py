from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="API Digital Library")

# --- PENGATURAN CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
#         SCHEMAS / MODEL INPUT DATA
# ==========================================

class LoginRequest(BaseModel):
    username: str
    password: str

class BookCreateRequest(BaseModel):
    title: str
    category: str
    price: float
    stock: int

class UpdatePriceRequest(BaseModel):
    price: float

class UpdateStockRequest(BaseModel):
    stock: int

class OrderCreateRequest(BaseModel):
    book_id: int
    quantity: int
    customer_name: str


# ==========================================
#               ROUTES / API
# ==========================================

@app.get("/")
def root():
    return {"app": "API Digital Library", "status": "running"}

# --- 1. GRUP AUTH (AUTENTIKASI) ---
@app.post("/api/auth/login")
def login(data: LoginRequest):
    if data.username == "aya@library.com" and data.password == "aya123":
        return {
            "status": "success",
            "access_token": "dummy_jwt_token_for_aya",
            "token_type": "bearer"
        }
    raise HTTPException(status_code=401, detail="Username atau password salah!")

@app.post("/api/auth/logout")
def logout():
    return {"message": "Sesi logout berhasil dihapus dari server."}

@app.get("/api/auth/me")
def get_profile():
    return {
        "username": "aya@library.com",
        "role": "Administrator",
        "name": "Sang Admin Perpus"
    }

# --- 2. GRUP BOOKS & CATEGORIES ---
@app.get("/api/books")
def get_books(category: Optional[str] = None, search: Optional[str] = None, sort: Optional[str] = None, min_price: Optional[float] = None, max_price: Optional[float] = None):
    return {
        "message": "Daftar Buku",
        "filters_applied": {"category": category, "search": search, "sort": sort, "min_price": min_price, "max_price": max_price},
        "data": []
    }

@app.get("/api/books/{book_id}")
def get_book_detail(book_id: int):
    return {"book_id": book_id, "title": "Buku Contoh", "price": 50000, "stock": 5}

@app.post("/api/books")
def create_book(book: BookCreateRequest):
    return {"message": "Buku baru berhasil ditambahkan!", "data": book}

@app.patch("/api/books/{book_id}/price")
def update_price(book_id: int, data: UpdatePriceRequest):
    return {"message": f"Harga buku ID {book_id} berhasil diubah menjadi Rp {data.price}"}

@app.patch("/api/books/{book_id}/stock")
def update_stock(book_id: int, data: UpdateStockRequest):
    return {"message": f"Stok buku ID {book_id} berhasil diupdate menjadi {data.stock} pcs"}

@app.delete("/api/books/{book_id}")
def delete_book(book_id: int):
    return {"message": f"Buku dengan ID {book_id} berhasil dihapus dari sistem."}

@app.get("/api/categories")
def get_categories():
    return {"categories": ["Koding", "Novel", "Sains", "Komik"]}

# --- 3. GRUP ORDERS & STATS ---
@app.post("/api/orders")
def checkout_order(order: OrderCreateRequest):
    return {"message": "Pesanan berhasil dibuat!", "invoice_id": "INV-99231", "detail": order}

@app.get("/api/orders")
def get_all_orders():
    return {"message": "Daftar Rekap Semua Pesanan Admin", "total_orders": 0, "orders": []}

@app.get("/api/orders/{order_id}")
def get_order_detail(order_id: str):
    return {"order_id": order_id, "status": "Paid", "total_payment": 150000}

@app.get("/api/stats")
def get_store_stats():
    return {
        "total_revenue": 5000000,
        "low_stock_warning": ["Buku Contoh"],
        "total_books_sold": 100
    }