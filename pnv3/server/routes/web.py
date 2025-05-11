# Copyright (c) 2025 iiPython

# Modules
from pathlib import Path

from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pnv3.server import app

# Initialization
SOURCE = Path(__file__).parents[1] / "frontend"
TEMPLATES = Jinja2Templates(directory = SOURCE)

# Routing
@app.get("/", response_class = HTMLResponse)
async def route_index(request: Request):
    return TEMPLATES.TemplateResponse(
        request,
        "index.html"
    )

# Handle static assets
app.mount("/", StaticFiles(directory = SOURCE / "assets"), name = "assets")
