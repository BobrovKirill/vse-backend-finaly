from fastapi.testclient import TestClient


def test_admin_login_and_me(client: TestClient, admin_headers: dict[str, str]) -> None:
    response = client.get("/api/v1/auth/me", headers=admin_headers)

    assert response.status_code == 200
    assert response.json()["email"] == "admin@example.com"


def test_admin_routes_require_token(client: TestClient) -> None:
    response = client.get("/api/v1/admin/packages")

    assert response.status_code == 403


def test_create_question_validates_options(client: TestClient, admin_headers: dict[str, str]) -> None:
    response = client.post(
        "/api/v1/admin/questions",
        headers=admin_headers,
        json={
            "text": "Есть ли у вас хроническая усталость?",
            "answer_options": [{"text": "Да", "score": 1}],
        },
    )

    assert response.status_code == 422


def test_public_submission_returns_best_package(client: TestClient, admin_headers: dict[str, str]) -> None:
    basic_package = _create_package(client, admin_headers, "Базовый чек-ап", "5000.00")
    cardio_package = _create_package(client, admin_headers, "Кардио пакет", "9000.00")

    question_response = client.post(
        "/api/v1/admin/questions",
        headers=admin_headers,
        json={
            "text": "Что беспокоит сильнее всего?",
            "question_type": "single",
            "position": 1,
            "answer_options": [
                {
                    "text": "Общая слабость",
                    "package_id": basic_package["id"],
                    "score": 2,
                    "position": 1,
                },
                {
                    "text": "Одышка и давление",
                    "package_id": cardio_package["id"],
                    "score": 5,
                    "position": 2,
                },
            ],
        },
    )
    assert question_response.status_code == 201
    question = question_response.json()

    public_questions = client.get("/api/v1/public/questions")
    assert public_questions.status_code == 200
    assert len(public_questions.json()) == 1

    selected_option = question["answer_options"][1]
    submit_response = client.post(
        "/api/v1/public/submissions",
        json={
            "contact_name": "Иван",
            "contact_phone": "+79990000000",
            "answers": [
                {
                    "question_id": question["id"],
                    "answer_option_ids": [selected_option["id"]],
                }
            ],
        },
    )

    assert submit_response.status_code == 200
    result = submit_response.json()
    assert result["recommended_package"]["id"] == cardio_package["id"]
    assert result["total_score"] == 5


def test_submission_rejects_option_from_another_question(
    client: TestClient,
    admin_headers: dict[str, str],
) -> None:
    package = _create_package(client, admin_headers, "Терапевт", "3000.00")
    first_question = _create_question(client, admin_headers, package["id"], "Первый вопрос?")
    second_question = _create_question(client, admin_headers, package["id"], "Второй вопрос?")

    wrong_option_id = second_question["answer_options"][0]["id"]
    response = client.post(
        "/api/v1/public/submissions",
        json={
            "answers": [
                {
                    "question_id": first_question["id"],
                    "answer_option_ids": [wrong_option_id],
                }
            ]
        },
    )

    assert response.status_code == 400
    assert "does not belong" in response.json()["detail"]


def _create_package(client: TestClient, headers: dict[str, str], title: str, price: str) -> dict:
    response = client.post(
        "/api/v1/admin/packages",
        headers=headers,
        json={
            "title": title,
            "description": "Описание медицинского пакета",
            "price": price,
            "included_services": "Консультация, анализы, заключение",
        },
    )
    assert response.status_code == 201
    return response.json()


def _create_question(client: TestClient, headers: dict[str, str], package_id: int, text: str) -> dict:
    response = client.post(
        "/api/v1/admin/questions",
        headers=headers,
        json={
            "text": text,
            "answer_options": [
                {"text": "Да", "package_id": package_id, "score": 1},
                {"text": "Нет", "package_id": package_id, "score": 0},
            ],
        },
    )
    assert response.status_code == 201
    return response.json()
