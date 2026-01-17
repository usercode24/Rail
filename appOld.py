from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import sqlite3
from datetime import datetime
import os
from pathlib import Path

# Initialize FastAPI
app = FastAPI()

# Get base directory
BASE_DIR = Path(__file__).parent

# Create static directory
os.makedirs("static", exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Database setup
def init_db():
    conn = sqlite3.connect("visitors.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS visits (
        id INTEGER PRIMARY KEY,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

init_db()

# Routes
@app.get("/", response_class=HTMLResponse)
async def home():
    # Record visit
    conn = sqlite3.connect("visitors.db")
    c = conn.cursor()
    c.execute("INSERT INTO visits DEFAULT VALUES")
    conn.commit()
    conn.close()
    
    # Serve HTML file
    html_path = BASE_DIR / "index.html"
    with open(html_path, "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.get("/api/stats")
async def stats():
    conn = sqlite3.connect("visitors.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM visits")
    total = c.fetchone()[0]
    conn.close()
    return {"total_visits": total, "status": "online"}

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# No if __name__ == "__main__" block needed for Railway