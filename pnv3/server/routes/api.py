# Copyright (c) 2025 iiPython

# Modules
from typing import Annotated

from pydantic import BaseModel
from fastapi import APIRouter, Cookie, Depends
from fastapi.responses import Response, JSONResponse

from pnv3.server import app, db

# Initialization
api = APIRouter(prefix = "/v1")

# Models
class HostPayload(BaseModel):
    hostname: str
    password: str

class FilenamePayload(BaseModel):
    filename: str

class WritePayload(FilenamePayload):
    content: str

class SearchPayload(BaseModel):
    query: str

# Utilities
def response(code: int, data: dict) -> JSONResponse:
    return JSONResponse({"code": code, "data": data}, status_code = code)

async def get_authorized_hostname(authorization: Annotated[str | None, Cookie()] = None) -> JSONResponse | str:
    if authorization is None:
        return response(401, {"message": "No authorization cookie was sent!"})

    hostname = await db.validate_token(authorization)
    if hostname is None:
        return response(403, {"message": "Invalid authorization cookie."})

    return hostname

# Handle routing
@api.post("/register")
async def api_register(host: HostPayload) -> JSONResponse:
    token, message = await db.register_host(**host.model_dump())
    if token is None:
        return response(400, {"message": message})

    return response(200, {"token": token})

@api.post("/login")
async def api_login(host: HostPayload) -> JSONResponse:
    token = await db.validate_host(**host.model_dump())
    if token is None:
        return response(401, {"message": "Invalid hostname or password."})

    return response(200, {"token": token})

@api.get("/{host:str}/pages")
async def api_pages(host: str) -> JSONResponse:
    content = await db.fetch_pages(host)
    if content is None:
        return response(404, {"message": "Specified host does not exist."})

    return response(200, {"pages": content})

@api.get("/{host:str}/page/{page:str}", response_model = None)
async def api_page(host: str, page: str) -> JSONResponse | Response:
    content = db.fetch_page(host, page)
    if content is None:
        return response(404, {"message": "Specified page does not exist."})

    return Response(content)

@api.post("/create")
async def api_create(data: FilenamePayload, hostname: str = Depends(get_authorized_hostname)) -> JSONResponse:
    message = await db.create_page(hostname, data.filename)
    if message is not None:
        return JSONResponse({"code": 400, "data": {"message": message}}, status_code = 400)

    return JSONResponse({"code": 200})

@api.post("/delete")
async def api_delete(data: FilenamePayload, hostname: str = Depends(get_authorized_hostname)) -> JSONResponse:
    message = await db.delete_page(hostname, data.filename)
    if message is not None:
        return JSONResponse({"code": 400, "data": {"message": message}}, status_code = 400)

    return JSONResponse({"code": 200})

@api.post("/write")
async def api_write(data: WritePayload, hostname: str = Depends(get_authorized_hostname)) -> JSONResponse:
    message = db.write_page(hostname, **data.model_dump())
    if message is not None:
        return JSONResponse({"code": 400, "data": {"message": message}}, status_code = 400)

    return JSONResponse({"code": 200})

@api.post("/search")
async def api_search(data: SearchPayload) -> JSONResponse:
    return JSONResponse({"code": 200, "data": await db.search_pages(data.query)})

app.include_router(api)
