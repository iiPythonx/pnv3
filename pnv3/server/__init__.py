# Copyright (c) 2025 iiPython

# Modules
from typing import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from pnv3.server.database import db

# Initialization
@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:
    await db.init()
    yield
    await db.close()

app = FastAPI(openapi_url = None, lifespan = lifespan)

# Load in routes
from pnv3.server import routes  # noqa
