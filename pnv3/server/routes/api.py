# Copyright (c) 2025 iiPython

# Modules
from pydantic import BaseModel
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from pnv3.server import app, db

# Initialization
api = APIRouter(prefix = "/v1")

class HostPayload(BaseModel):
    hostname: str
    password: str

# Handle routing
@api.post("/register")
async def api_register(host: HostPayload) -> JSONResponse:
    token, message = await db.register_host(**host.model_dump())
    if token is None:
        return JSONResponse({"code": 400, "data": {"message": message}}, status_code = 400)

    return JSONResponse({"code": 200, "data": {"token": token}})

@api.post("/login")
async def api_login(host: HostPayload) -> JSONResponse:
    token = await db.validate_host(**host.model_dump())
    if token is None:
        return JSONResponse({"code": 403, "data": {"message": "Invalid hostname or password."}}, status_code = 403)

    return JSONResponse({"code": 200, "data": {"token": token}})

app.include_router(api)
