from fastapi import FastAPI
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import engine
from app.core.security import get_password_hash
from app.models.entities import User
from app.api.v1 import admin, auth
from app.api.v1.public import public


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name)
    app.include_router(auth.router, prefix="/api/v1")
    app.include_router(admin.router, prefix="/api/v1")
    app.include_router(public.router, prefix="/api/v1")

    @app.on_event("startup")
    def startup() -> None:
        _ensure_first_admin()

    return app


def _ensure_first_admin() -> None:
    settings = get_settings()
    with Session(engine) as db:
        existing = db.execute(
            select(User).where(User.email == settings.first_admin_email)
        ).scalar_one_or_none()
        if existing is not None:
            return
        db.add(
            User(
                email=settings.first_admin_email,
                hashed_password=get_password_hash(settings.first_admin_password),
                is_admin=True,
            )
        )
        db.commit()


app = create_app()
