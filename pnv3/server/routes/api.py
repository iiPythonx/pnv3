# Copyright (c) 2025 iiPython

# Modules
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from pnv3.server import app

# Initialization
api = APIRouter(prefix = "/v1")

# Handle routing
@api.get("/info")
async def api_info() -> JSONResponse:
    return JSONResponse({"code": 200, "data": {"success": True}})

app.include_router(api)
