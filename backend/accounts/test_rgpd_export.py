"""Tests J3-bis — export RGPD Art. 15/20."""

import csv
import io
import json

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from accounts.models import DataRequest
from quizzes.models import Question, Quiz

pytestmark = pytest.mark.django_db


@pytest.fixture
def user():
    return User.objects.create_user(
        username="hugo.petit@test.local",
        email="hugo.petit@test.local",
        password="motdepasse123",
        first_name="Hugo",
        last_name="Petit",
    )


@pytest.fixture
def other_user():
    return User.objects.create_user(
        username="alice@test.local",
        email="alice@test.local",
        password="motdepasse123",
    )


@pytest.fixture
def auth_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def quiz(user, other_user):
    owned = Quiz.objects.create(user=user, title="Droit numérique", source_text="Cours RGPD")
    other = Quiz.objects.create(user=other_user, title="Quiz privé Alice", source_text="Secret Alice")
    for i in range(1, 11):
        Question.objects.create(
            quiz=owned,
            index=i,
            prompt=f"Question Hugo {i}",
            options=["A", "B", "C", "D"],
            correct_index=i % 4,
            selected_index=(i + 1) % 4,
        )
        Question.objects.create(
            quiz=other,
            index=i,
            prompt=f"Question Alice {i}",
            options=["A", "B", "C", "D"],
            correct_index=0,
        )
    return owned


def test_export_json_contains_user_data_only(auth_client, user, quiz):
    response = auth_client.get("/api/accounts/me/export/?format=json")
    assert response.status_code == 200
    assert response["Content-Type"].startswith("application/json")
    assert response["Content-Disposition"].startswith("attachment")
    payload = json.loads(response.content)

    assert payload["account"]["email"] == "hugo.petit@test.local"
    assert payload["generated_quizzes"][0]["title"] == "Droit numérique"
    assert "Quiz privé Alice" not in response.content.decode("utf-8")
    assert "audit_logs" in payload
    assert DataRequest.objects.filter(user=user, status=DataRequest.Status.RESPONDED).exists()


def test_export_csv_is_machine_readable(auth_client, quiz):
    response = auth_client.get("/api/accounts/me/export/?format=csv")
    assert response.status_code == 200
    assert response["Content-Type"].startswith("text/csv")
    rows = list(csv.DictReader(io.StringIO(response.content.decode("utf-8-sig"))))
    assert len(rows) == 10
    assert rows[0]["quiz_title"] == "Droit numérique"


def test_export_requires_authentication():
    response = APIClient().get("/api/accounts/me/export/")
    assert response.status_code in (401, 403)
