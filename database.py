"""
database.py — In-memory database untuk Lembar API
Ganti dengan PostgreSQL/SQLite di production menggunakan SQLAlchemy.
"""

# ── Tabel Buku ─────────────────────────────────────────────────────
BOOKS: list[dict] = [
    {"id": 1,  "title": "Siddhartha",            "author": "Hermann Hesse",          "category": "Fiksi",              "price": 89000,  "stock": 12, "cover": "📖", "rating": 4.8, "sold": 234,  "desc": "Perjalanan spiritual seorang pemuda mencari makna hidup di India kuno."},
    {"id": 2,  "title": "Sapiens",               "author": "Yuval Noah Harari",      "category": "Non-fiksi",          "price": 145000, "stock": 8,  "cover": "🌍", "rating": 4.9, "sold": 512,  "desc": "Sejarah singkat umat manusia dari zaman batu hingga era modern."},
    {"id": 3,  "title": "Filosofi Teras",        "author": "Henry Manampiring",      "category": "Non-fiksi",          "price": 98000,  "stock": 20, "cover": "🏛️", "rating": 4.7, "sold": 890,  "desc": "Filsafat Stoa untuk menghadapi tantangan hidup sehari-hari."},
    {"id": 4,  "title": "Laskar Pelangi",        "author": "Andrea Hirata",          "category": "Fiksi",              "price": 79000,  "stock": 15, "cover": "🌈", "rating": 4.8, "sold": 1200, "desc": "Kisah perjuangan anak-anak Belitung menggapai mimpi."},
    {"id": 5,  "title": "Atomic Habits",         "author": "James Clear",            "category": "Pengembangan Diri", "price": 119000, "stock": 5,  "cover": "⚡", "rating": 4.9, "sold": 678,  "desc": "Cara mudah membangun kebiasaan baik dan menghentikan kebiasaan buruk."},
    {"id": 6,  "title": "Dune",                  "author": "Frank Herbert",          "category": "Fiksi",              "price": 165000, "stock": 7,  "cover": "🏜️", "rating": 4.7, "sold": 345,  "desc": "Epic science fiction tentang ekologi, politik, dan agama di planet gurun."},
    {"id": 7,  "title": "Bumi Manusia",          "author": "Pramoedya Ananta Toer",  "category": "Fiksi",              "price": 95000,  "stock": 18, "cover": "🌏", "rating": 4.9, "sold": 456,  "desc": "Kisah cinta dan perjuangan di era kolonial Belanda."},
    {"id": 8,  "title": "The Subtle Art",        "author": "Mark Manson",            "category": "Pengembangan Diri", "price": 108000, "stock": 11, "cover": "🎯", "rating": 4.6, "sold": 789,  "desc": "Pendekatan jujur dan segar tentang menjalani kehidupan yang baik."},
    {"id": 9,  "title": "Pulang",                "author": "Tere Liye",              "category": "Fiksi",              "price": 72000,  "stock": 25, "cover": "🏠", "rating": 4.7, "sold": 934,  "desc": "Perjalanan seorang pria melintasi dunia bawah tanah untuk menemukan jati dirinya."},
    {"id": 10, "title": "Brief History of Time", "author": "Stephen Hawking",        "category": "Sains",              "price": 135000, "stock": 6,  "cover": "🌌", "rating": 4.8, "sold": 267,  "desc": "Penjelasan fisika modern yang accessible untuk pembaca umum."},
    {"id": 11, "title": "Normal People",         "author": "Sally Rooney",           "category": "Fiksi",              "price": 88000,  "stock": 9,  "cover": "💬", "rating": 4.5, "sold": 312,  "desc": "Hubungan kompleks dua remaja Irlandia dari SMA hingga universitas."},
    {"id": 12, "title": "Ikigai",                "author": "Héctor García",          "category": "Pengembangan Diri", "price": 92000,  "stock": 14, "cover": "🌸", "rating": 4.7, "sold": 567,  "desc": "Rahasia orang Jepang untuk hidup bahagia dan panjang umur."},
]

# ── Tabel Users ────────────────────────────────────────────────────
USERS: dict[str, dict] = {
    "aya@lembar.id": {
        "name": "Aya",
        "email": "aya@lembar.id",
        "password": "lembar123",
        "role": "admin",
    }
}

# ── Tabel Tokens (session) ─────────────────────────────────────────
TOKENS: dict[str, str] = {}   # token → email

# ── Tabel Pesanan ──────────────────────────────────────────────────
ORDERS: list[dict] = []