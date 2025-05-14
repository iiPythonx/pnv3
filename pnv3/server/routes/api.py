# Copyright (c) 2025 iiPython

# Modules
from typing import Annotated

from pydantic import BaseModel
from fastapi import APIRouter, Cookie
from fastapi.responses import Response, JSONResponse

from pnv3.server import app, db

# Initialization
api = APIRouter(prefix = "/v1")

class HostPayload(BaseModel):
    hostname: str
    password: str

class FilenamePayload(BaseModel):
    filename: str

class WritePayload(FilenamePayload):
    content: str

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
        return JSONResponse({"code": 401, "data": {"message": "Invalid hostname or password."}}, status_code = 401)

    return JSONResponse({"code": 200, "data": {"token": token}})

@api.get("/{host:str}/pages")
async def api_pages(host: str) -> JSONResponse:
    content = db.fetch_pages(host)
    if content is None:
        return JSONResponse({"code": 404, "data": {"message": "Specified host does not exist."}}, status_code = 404)

    return JSONResponse({"code": 200, "data": {"pages": content}})

@api.get("/{host:str}/page/{page:str}", response_model = None)
async def api_page(host: str, page: str) -> JSONResponse | Response:
    content = db.fetch_page(host, page)
    if content is None:
        return JSONResponse({"code": 404, "data": {"message": "Specified page does not exist."}}, status_code = 404)

    return Response(content)

@api.post("/create")
async def api_create(data: FilenamePayload, authorization: Annotated[str | None, Cookie()] = None) -> JSONResponse:
    if authorization is None:
        return JSONResponse({"code": 401, "data": {"message": "No authorization cookie was sent!"}}, status_code = 401)

    hostname = await db.validate_token(authorization)
    if hostname is None:
        return JSONResponse({"code": 403, "data": {"message": "Invalid authorization cookie."}}, status_code = 403)

    message = db.create_page(hostname, data.filename)
    if message is not None:
        return JSONResponse({"code": 400, "data": {"message": message}}, status_code = 400)

    return JSONResponse({"code": 200})

@api.post("/delete")
async def api_delete(data: FilenamePayload, authorization: Annotated[str | None, Cookie()] = None) -> JSONResponse:
    if authorization is None:
        return JSONResponse({"code": 401, "data": {"message": "No authorization cookie was sent!"}}, status_code = 401)

    hostname = await db.validate_token(authorization)
    if hostname is None:
        return JSONResponse({"code": 403, "data": {"message": "Invalid authorization cookie."}}, status_code = 403)

    message = db.delete_page(hostname, data.filename)
    if message is not None:
        return JSONResponse({"code": 400, "data": {"message": message}}, status_code = 400)

    return JSONResponse({"code": 200})

@api.post("/write")
async def api_write(data: WritePayload, authorization: Annotated[str | None, Cookie()] = None) -> JSONResponse:
    if authorization is None:
        return JSONResponse({"code": 401, "data": {"message": "No authorization cookie was sent!"}}, status_code = 401)

    hostname = await db.validate_token(authorization)
    if hostname is None:
        return JSONResponse({"code": 403, "data": {"message": "Invalid authorization cookie."}}, status_code = 403)

    message = db.write_page(hostname, **data.model_dump())
    if message is not None:
        return JSONResponse({"code": 400, "data": {"message": message}}, status_code = 400)

    return JSONResponse({"code": 200})

app.include_router(api)
