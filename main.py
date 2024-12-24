# from json import dumps
from json import loads
import json
import os
from fastapi import FastAPI
import pyodbc
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
import sqlalchemy
from app.routes import product

DB_SERVER = os.getenv('DB_SERVER')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

CONN_STR = f'Driver={{ODBC Driver 18 for SQL Server}};Server=tcp:{DB_SERVER}.database.windows.net,1433;Database={DB_NAME};Uid={DB_USER};Pwd={DB_PASSWORD};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     print(pyodbc.drivers())
#     app.conn = pyodbc.connect(CONN_STR)
#     app.conn.add_output_converter(-151, lambda x: str(x))

#     yield

#     app.conn.close()

# load documentation
tags_metadata = []
with open('./doc.json') as fd:
    tags_metadata = json.load(fd)
# end load documentation

app = FastAPI(openapi_tags=tags_metadata)  # , lifespan=lifespan)
app.conn_str = f"mssql+pyodbc:///?odbc_connect={sqlalchemy.engine.url.quote_plus(CONN_STR)}"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ou une liste d'origines spécifiques
    allow_credentials=True,
    allow_methods=["*"],  # Ou une liste de méthodes spécifiques
    allow_headers=["*"],  # Ou une liste d'en-têtes spécifiques
)

app.include_router(product.router)


@app.get("/")
async def root():
    return {"message": f"Hello World {os.getenv('DB')}"}
