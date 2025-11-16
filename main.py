from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from .db import init_db, get_db
from .utils import generate_code, is_valid_url, now_iso
from .rate_limiter import allow
import sqlite3
from pydantic import BaseModel

class URLRequest(BaseModel):
    url: str

app = FastAPI(title="URL Shortener")
init_db()

def insert_url(code, original_url):
    db = get_db()
    try:
        db.execute(
            "INSERT INTO urls (code, original_url, created_at) VALUES (?, ?, ?)",
            (code, original_url, now_iso())
        )
        db.commit()
    except sqlite3.IntegrityError:
        db.close()
        raise

def get_by_code(code):
    db = get_db()
    row = db.execute("SELECT * FROM urls WHERE code = ?", (code,)).fetchone()
    db.close()
    return row

@app.post("/shorten")
async def shorten(request: URLRequest, raw_request: Request):
    ip = ip = raw_request.client.host
    if not allow(ip):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    url = request.url
    if not url or not is_valid_url(url):
        raise HTTPException(status_code=400, detail="Invalid or missing URL")

    for _ in range(5):
        code = generate_code()
        try:
            insert_url(code, url)
            short = f"http://localhost:8000/s/{code}"
            return {"code": code, "short_url": short}
        except sqlite3.IntegrityError:
            continue
    raise HTTPException(status_code=500, detail="Could not generate unique code")

@app.get("/s/{code}")
def redirect(code: str):
    row = get_by_code(code)
    if not row:
        raise HTTPException(status_code=404, detail="Code not found")
    db = get_db()
    db.execute("UPDATE urls SET clicks = clicks + 1 WHERE code = ?", (code,))
    db.commit()
    db.close()
    return RedirectResponse(row["original_url"])

@app.get("/info/{code}")
def info(code: str):
    row = get_by_code(code)
    if not row:
        raise HTTPException(status_code=404, detail="Code not found")
    return {"code": row["code"], "original_url": row["original_url"], "clicks": row["clicks"], "created_at": row["created_at"]}
