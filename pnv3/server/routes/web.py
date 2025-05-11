# Copyright (c) 2025 iiPython

# Modules
from pathlib import Path
from typing import Annotated

from fastapi import Request, Header
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pnv3.server import app

# Initialization
SOURCE = Path(__file__).parents[1] / "frontend"
TEMPLATES = Jinja2Templates(directory = SOURCE)

# Routing
@app.get("/", response_model = None)
async def route_index(request: Request, authorization: Annotated[str | None, Header()] = None):
    if authorization is None:
        return RedirectResponse("/auth")

    return TEMPLATES.TemplateResponse(request, "pages/dash.jinja2")

@app.get("/auth", response_class = HTMLResponse)
async def route_auth(request: Request):
    return TEMPLATES.TemplateResponse(request, "pages/auth.jinja2")

# Handle static assets
app.mount("/", StaticFiles(directory = SOURCE / "assets"), name = "assets")
