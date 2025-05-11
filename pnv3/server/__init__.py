# Copyright (c) 2025 iiPython

# Modules
from fastapi import FastAPI

# Initialization
app = FastAPI(openapi_url = None)

# Load in routes
from pnv3.server import routes
