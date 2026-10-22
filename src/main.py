"""
Project Caesar - FastAPI Backend
Roman-themed DevOps dashboard
"""
import os
import platform
import socket
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Project Caesar", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (CSS, JS, images)
static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/", response_class=HTMLResponse)
async def serve_index():
    html_path = Path(__file__).parent / "static" / "index.html"
    return HTMLResponse(content=html_path.read_text(encoding="utf-8"))


@app.get("/api/status")
async def get_status():
    """Return live pod / environment information to display on the dashboard."""
    return JSONResponse({
        "legion": os.getenv("POD_NAME", socket.gethostname()),
        "cohort": os.getenv("POD_NAMESPACE", "local"),
        "node": os.getenv("NODE_NAME", platform.node()),
        "version": os.getenv("APP_VERSION", "dev"),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status": "VICTORIOUS",
    })


@app.get("/health")
async def health():
    return {"status": "ok"}
