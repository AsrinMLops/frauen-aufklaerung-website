from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import psycopg2
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        database="fak_db",
        user="fak_user",
        password="fak2026!"
    )

@app.get("/")
def home():
    return {"message": "FAK Backend API läuft!"}

@app.get("/articles")
def get_articles(category: Optional[str] = None, lang: str = "de"):
    conn = get_db()
    cur = conn.cursor()
    if category:
        cur.execute(f"SELECT id, title_{lang}, content_{lang}, category, author, image_url, created_at FROM articles WHERE published=TRUE AND category=%s ORDER BY created_at DESC", (category,))
    else:
        cur.execute(f"SELECT id, title_{lang}, content_{lang}, category, author, image_url, created_at FROM articles WHERE published=TRUE ORDER BY created_at DESC")
    rows = cur.fetchall()
    conn.close()
    return [{"id": r[0], "title": r[1], "content": r[2], "category": r[3], "author": r[4], "image_url": r[5], "created_at": str(r[6])} for r in rows]

@app.get("/articles/{article_id}")
def get_article(article_id: int, lang: str = "de"):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(f"SELECT id, title_{lang}, content_{lang}, category, author, image_url, created_at FROM articles WHERE id=%s AND published=TRUE", (article_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Artikel nicht gefunden")
    return {"id": row[0], "title": row[1], "content": row[2], "category": row[3], "author": row[4], "image_url": row[5], "created_at": str(row[6])}

@app.get("/projects")
def get_projects(lang: str = "de"):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(f"SELECT id, name_{lang}, description_{lang}, year, status, image_url FROM projects ORDER BY year DESC")
    rows = cur.fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "description": r[2], "year": r[3], "status": r[4], "image_url": r[5]} for r in rows]

@app.get("/photos")
def get_photos(category: Optional[str] = None):
    conn = get_db()
    cur = conn.cursor()
    if category:
        cur.execute("SELECT id, title_de, image_url, photographer, category FROM photos WHERE category=%s ORDER BY created_at DESC", (category,))
    else:
        cur.execute("SELECT id, title_de, image_url, photographer, category FROM photos ORDER BY created_at DESC")
    rows = cur.fetchall()
    conn.close()
    return [{"id": r[0], "title": r[1], "image_url": r[2], "photographer": r[3], "category": r[4]} for r in rows]
