from fastapi.testclient import TestClient
from app.schemas.question import PublicQuestionRead


def test_admin_login_and_me(client: TestClient, admin_headers: dict[str, str]) -> None:
    response = client.get("/api/v1/auth/me", headers=admin_headers)

    assert response.status_code == 200
    assert response.json()["email"] == "admin@example.com"


def test_admin_routes_require_token(client: TestClient) -> None:
    response = client.get("/api/v1/admin/packages")

    assert response.status_code == 403


def test_create_question_validates_answers(client: TestClient, admin_headers: dict[str, str]) -> None:
    response = client.post(
        "/api/v1/admin/questions",
        headers=admin_headers,
        json={
            "text": "Есть ли у вас хроническая усталость?",
            "answers": [{"text": "Да"}],
        },
    )

    assert response.status_code == 422


def test_public_choice_returns_best_package(client: TestClient, admin_headers: dict[str, str]) -> None:
    package = _create_package(client, admin_headers, "Метаболический пакет", "9000.00")
    overweight = _create_indicator(client, admin_headers, "overweight", "Лишний вес")
    _create_package_rule(client, admin_headers, package["id"], overweight["id"], min_score=2)
    question = _create_question(client, admin_headers, overweight["id"], "Имеете ли вы лишний вес?")

    selected_answer = question["answers"][2]
    response = client.post(
        "/api/v1/public/choices",
        json={
            "contact_name": "Иван",
            "answers": [
                {
                    "question_id": question["id"],
                    "answer_ids": [selected_answer["id"]],
                }
            ],
        },
    )

    assert response.status_code == 200
    result = response.json()
    assert result["recommended_packages"][0]["package"]["id"] == package["id"]
    assert result["indicator_scores"] == [{"indicator_id": overweight["id"], "score": 2}]


def test_one_answer_can_affect_multiple_indicators(
    client: TestClient,
    admin_headers: dict[str, str],
) -> None:
    overweight = _create_indicator(client, admin_headers, "overweight", "Лишний вес")
    diabetes = _create_indicator(client, admin_headers, "diabetes", "Риск диабета")
    response = client.post(
        "/api/v1/admin/questions",
        headers=admin_headers,
        json={
            "text": "Что вас беспокоит сильнее всего?",
            "answers": [
                {
                    "text": "Лишний вес",
                    "effects": [
                        {"indicator_id": overweight["id"], "score": 3},
                        {"indicator_id": diabetes["id"], "score": 1},
                    ],
                },
                {"text": "Ничего", "effects": []},
            ],
        },
    )

    assert response.status_code == 201
    assert len(response.json()["answers"][0]["effects"]) == 2


def test_choice_returns_ranked_packages_with_structured_services(
    client: TestClient,
    admin_headers: dict[str, str],
) -> None:
    overweight = _create_indicator(client, admin_headers, "overweight", "Лишний вес")
    primary = _create_package(client, admin_headers, "Основной пакет", "9000.00")
    alternative = _create_package(client, admin_headers, "Альтернативный пакет", "6000.00")
    _create_package_rule(client, admin_headers, primary["id"], overweight["id"], min_score=2, weight=10)
    _create_package_rule(client, admin_headers, alternative["id"], overweight["id"], min_score=2, weight=5)
    service = _create_service(client, admin_headers, "Анализ глюкозы", "350.00")
    _add_package_service(client, admin_headers, primary["id"], service["id"])
    question = _create_question(client, admin_headers, overweight["id"], "Имеете ли вы лишний вес?")

    response = client.post(
        "/api/v1/public/choices",
        json={
            "answers": [
                {
                    "question_id": question["id"],
                    "answer_ids": [question["answers"][2]["id"]],
                }
            ]
        },
    )

    assert response.status_code == 200
    recommendations = response.json()["recommended_packages"]
    assert [item["package"]["id"] for item in recommendations] == [primary["id"], alternative["id"]]
    assert recommendations[0]["matched_weight"] == 10
    assert recommendations[0]["package"]["services"][0]["service"]["title"] == "Анализ глюкозы"


def test_public_answer_exposes_description_but_hides_effects(
    client: TestClient,
    admin_headers: dict[str, str],
) -> None:
    indicator = _create_indicator(client, admin_headers, "sleep", "Качество сна")
    question = client.post(
        "/api/v1/admin/questions",
        headers=admin_headers,
        json={
            "text": "Как вы обычно спите?",
            "answers": [
                {
                    "text": "Хорошо",
                    "description": "Просыпаюсь отдохнувшим",
                    "effects": [],
                },
                {
                    "text": "Плохо",
                    "description": "Часто просыпаюсь ночью",
                    "effects": [{"indicator_id": indicator["id"], "score": 2}],
                },
            ],
        },
    ).json()

    response = client.get("/api/v1/public/questions")

    assert response.status_code == 200
    public_answer = next(item for item in response.json() if item["id"] == question["id"])["answers"][1]
    assert public_answer["description"] == "Часто просыпаюсь ночью"
    assert "effects" not in public_answer


def test_public_questions_use_cache(client: TestClient, monkeypatch) -> None:
    cached_question = PublicQuestionRead(
        id=99,
        text="Вопрос из Redis",
        answers=[],
    )
    monkeypatch.setattr(
        "app.api.v1.public.public.get_cached_public_questions",
        lambda: [cached_question],
    )

    response = client.get("/api/v1/public/questions")

    assert response.status_code == 200
    assert response.json()[0]["text"] == "Вопрос из Redis"


def _create_package(client: TestClient, headers: dict[str, str], title: str, price: str) -> dict:
    response = client.post(
        "/api/v1/admin/packages",
        headers=headers,
        json={
            "title": title,
            "description": "Описание медицинского пакета",
            "price": price,
            "checkout_url": "https://clinic.example.com/order",
        },
    )
    assert response.status_code == 201
    return response.json()


def _create_indicator(client: TestClient, headers: dict[str, str], code: str, title: str) -> dict:
    response = client.post(
        "/api/v1/admin/indicators",
        headers=headers,
        json={"code": code, "title": title},
    )
    assert response.status_code == 201
    return response.json()


def _create_package_rule(
    client: TestClient,
    headers: dict[str, str],
    package_id: int,
    indicator_id: int,
    min_score: int,
    weight: int = 1,
) -> dict:
    response = client.post(
        f"/api/v1/admin/packages/{package_id}/rules",
        headers=headers,
        json={"indicator_id": indicator_id, "min_score": min_score, "weight": weight},
    )
    assert response.status_code == 201
    return response.json()


def _create_service(client: TestClient, headers: dict[str, str], title: str, price: str) -> dict:
    response = client.post(
        "/api/v1/admin/services",
        headers=headers,
        json={"title": title, "price": price},
    )
    assert response.status_code == 201
    return response.json()


def _add_package_service(
    client: TestClient,
    headers: dict[str, str],
    package_id: int,
    service_id: int,
) -> dict:
    response = client.post(
        f"/api/v1/admin/packages/{package_id}/services",
        headers=headers,
        json={"service_id": service_id},
    )
    assert response.status_code == 201
    return response.json()


def _create_question(client: TestClient, headers: dict[str, str], indicator_id: int, text: str) -> dict:
    response = client.post(
        "/api/v1/admin/questions",
        headers=headers,
        json={
            "text": text,
            "answers": [
                {"text": "Нет", "effects": []},
                {"text": "Чуть-чуть", "effects": [{"indicator_id": indicator_id, "score": 1}]},
                {"text": "Есть", "effects": [{"indicator_id": indicator_id, "score": 2}]},
                {"text": "Сильный", "effects": [{"indicator_id": indicator_id, "score": 3}]},
            ],
        },
    )
    assert response.status_code == 201
    return response.json()
