import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from firebase_admin import initialize_app, credentials

from app.core.config import get_settings
from app.utils.logging import setup_logging
from app.db.database import Base, engine
from app.db.models import (
    users,
    walk_points,
    walk_summaries,
    walks,
)  # db 정의 때문에 필요
from app.routers import course, root, user, test


@asynccontextmanager
async def db_lifespan(_: FastAPI):
    setup_logging()

    # Firebase 초기화
    settings = get_settings()
    if not settings.firebase_auth:
        raise Exception("Firebase Credential Location not found in .env")
    if not os.path.isfile(f"./{settings.firebase_auth}"):
        raise Exception(
            f"Firebase Credential File not found in {settings.firebase_auth}"
        )
    cred = credentials.Certificate(settings.firebase_auth)
    initialize_app(cred)

    # DB 연결 및 테이블 생성
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        raise Exception(f"Database connection failed: {e}")

    yield

    await engine.dispose()


app = FastAPI(lifespan=db_lifespan)

app.include_router(root.router)
app.include_router(user.router)
app.include_router(course.router)
app.include_router(test.router)
