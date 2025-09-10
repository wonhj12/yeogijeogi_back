import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from logging import info
from firebase_admin import initialize_app, credentials

from app.core.config import get_settings
from app.db.mongodb import MongoDB
from app.routers import root, user
from app.routers import test


@asynccontextmanager
async def db_lifespan(_: FastAPI):
    settings = get_settings()
    if not settings.firebase_auth:
        raise Exception("Firebase Credential Location not found in .env")
    if not os.path.isfile(f"./{settings.firebase_auth}"):
        raise Exception(
            f"Firebase Credential File not found in {settings.firebase_auth}"
        )
    cred = credentials.Certificate(settings.firebase_auth)
    initialize_app(cred)
    info("Connected to Firebase")

    db = MongoDB()
    await db.connect_database()
    await db.check_status()
    info("Connected to database")

    yield

    db.get_client().close()


app = FastAPI(lifespan=db_lifespan)

app.include_router(root.router)
app.include_router(user.router)
app.include_router(test.router)
