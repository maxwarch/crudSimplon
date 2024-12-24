# from json import dumps
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
import pymongo
from pymongo.errors import ServerSelectionTimeoutError
import urllib
from app.routes import product
    
@asynccontextmanager
async def lifespan(app: FastAPI):
    username = urllib.parse.quote_plus(os.getenv('DB_USER'))
    password = urllib.parse.quote_plus(os.getenv('DB_PWD'))
    db = os.getenv('DB')
    uri = os.getenv('DB_URI')

    uri = f"{uri % (username, password, db)}"
    app.client = AsyncIOMotorClient(uri)
    app.db = app.client.get_database(os.getenv('DB'))
    
    try:
        ping_response = await app.db.command("ping")
        if int(ping_response["ok"]) != 1:
            raise Exception("Problem connecting to database cluster.")
        else:
            print("Connected to database cluster.")

    except ServerSelectionTimeoutError as e:
        print(e)
    
    yield

    app.client.close()
    
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Ou une liste d'origines spécifiques
    allow_credentials=True,
    allow_methods=["*"], # Ou une liste de méthodes spécifiques
    allow_headers=["*"], # Ou une liste d'en-têtes spécifiques
)

app.include_router(product.router)


@app.get("/")
async def root():
    return {"message": f"Hello World {os.getenv('DB')}"} 