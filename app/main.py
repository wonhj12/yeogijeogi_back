from fastapi import FastAPI
from contextlib import asynccontextmanager
from logging import info

from app.db.mongodb import MongoDB
from app.routers import root
from app.routers import test


@asynccontextmanager
async def db_lifespan(app: FastAPI):
    db = MongoDB()
    await db.connect_database()
    await db.check_status()
    info("Connected to database")

    yield

    db.get_client().close()


app = FastAPI(lifespan=db_lifespan)

app.include_router(root.router)
app.include_router(test.router)
