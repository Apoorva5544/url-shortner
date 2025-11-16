# 🔗 URL Shortener API (FastAPI + SQLite)

A lightweight and efficient URL Shortening service built using **FastAPI**, **SQLite**, and **Python**.
This project provides a simple REST API to generate short codes for long URLs and redirect users when the short link is accessed.
It also includes **rate limiting**, **click tracking**, and an easy-to-understand codebase suitable for learning and small deployments.

#  Tech Stack

Python 3.11+

FastAPI

SQLite

Uvicorn

Pydantic

HTTPException & RedirectResponse

---

##  Features

* **Shorten any URL** into a compact code
* **Automatic redirection** using `/s/{code}`
* **Rate limiting by IP address** (prevents abuse)
* **SQLite storage** with click count tracking
* **FastAPI-powered**, clean and async-friendly
* Lightweight — no external dependencies beyond FastAPI

---

##  Project Structure

```
.
├── main.py              # FastAPI application with routes
├── db.py                # SQLite database helpers
├── utils.py             # URL validation + code generator
├── rate_limiter.py      # In-memory rate limiting
└── requirements.txt
```

---

##  Installation & Setup

### 1️ Clone the repository

```bash
git clone <repo-url>
cd url-shortener
```

### 2️ Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3️ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️ Run the server

```bash
uvicorn main:app --reload
```

Server starts at:

```
http://localhost:8000
```

---

##  API Endpoints

### **POST /shorten**

Shortens a long URL.

#### Request Body

```json
{
  "url": "https://example.com/some/long/link"
}
```

#### Response

```json
{
  "code": "AbC123",
  "short_url": "http://localhost:8000/s/AbC123"
}
```

---

### **GET /s/{code}**

Redirects to the original long URL.
Also increments click count in the database.

Returns **404** if the code doesn't exist.

---

## 🗄️ Database Schema

```
urls (
  code TEXT PRIMARY KEY,
  original_url TEXT NOT NULL,
  clicks INTEGER DEFAULT 0
)
```

---

##  Rate Limiting

Each IP address is allowed a limited number of shorten requests per minute.
If exceeded, the API returns:

```
429 Too Many Requests
```

---

##  Testing with curl

### Shorten a URL

```bash
curl -X POST "http://127.0.0.1:8000/shorten" \
     -H "Content-Type: application/json" \
     -d "{\"url\": \"https://google.com\"}"
```

### Follow short URL

```bash
curl -I "http://127.0.0.1:8000/s/AbC123"
```

---

##  Notes

* This service **does not compress the URL**, it generates a **short unique code** that acts as a key.
* Links remain short and clean — ideal for sharing.
* Designed for learning and small self-hosted tools.

---

##  Future Enhancements (Optional)

* Custom alias support
* Expiry time for links
* Dashboard with analytics
* User authentication for managing URLs

---


Just tell me!
