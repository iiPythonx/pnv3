# pnv3

A revival of the long dead PyNet v3 project.  
Because I couldn't let it die just yet.

## Setup

Clone the GitHub repository, that's about it.  
A `uv` based launch script will be provided someday to replace `python3 -m`.

## Running the Client

```sh
python3 -m pnv3.client
```

## Running the Server (not available yet)

```sh
uv venv
uv pip install -e .
source .venv/bin/python3
python3 -m pnv3.server
```
