import os

os.environ["DATABASE_URL"] = "sqlite:///./test_medical_recommendations.db"
os.environ["SECRET_KEY"] = "test-secret"
os.environ["FIRST_ADMIN_EMAIL"] = "admin@example.com"
os.environ["FIRST_ADMIN_PASSWORD"] = "admin12345"

import pytest
from fastapi.testclient import TestClient

from app.core.database import Base, SessionLocal, engine
from app.core.security import get_password_hash
from app.main import app
from app.models.entities import User


@pytest.fixture()
def client() -> TestClient:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        db.add(
            User(
                email="admin@example.com",
                hashed_password=get_password_hash("admin12345"),
                is_admin=True,
            )
        )
        db.commit()

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture()
def admin_headers(client: TestClient) -> dict[str, str]:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@example.com", "password": "admin12345"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
