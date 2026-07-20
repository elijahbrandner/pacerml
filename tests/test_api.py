"""
test_api.py

API tests for the PacerML Sprint 4 prototype.

These tests validate that the FastAPI endpoints return successful responses
and include the expected output fields.
"""

import sys
from pathlib import Path

from fastapi.testclient import TestClient

# Allow tests to import the FastAPI app from the app folder.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_PATH = PROJECT_ROOT / "app"
SRC_PATH = PROJECT_ROOT / "src"

sys.path.append(str(APP_PATH))
sys.path.append(str(SRC_PATH))

from main import app


client = TestClient(app)


def test_health_endpoint():
    """
    Test that the health endpoint returns a successful API status.
    """

    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "ok"
    assert "message" in data


def test_categorize_endpoint():
    """
    Test that the categorize endpoint returns a predicted category.
    """

    response = client.post(
        "/categorize",
        json={
            "description": "Starbucks Latte"
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert data["description"] == "Starbucks Latte"
    assert "predicted_category" in data
    assert isinstance(data["predicted_category"], str)


def test_budget_risk_endpoint():
    """
    Test that the budget risk endpoint returns a valid risk level.
    """

    response = client.post(
        "/budget-risk",
        json={
            "total_expenses": 1600,
            "monthly_budget": 2500,
            "current_day": 15,
            "days_in_month": 30,
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert "risk_level" in data
    assert data["risk_level"] in ["Low", "Medium", "High"]
    assert "actual_usage_percent" in data
    assert "expected_usage_percent" in data


def test_financial_health_endpoint():
    """
    Test that the financial health endpoint returns score, grade, and risk.
    """

    response = client.post(
        "/financial-health",
        json={
            "total_expenses": 1600,
            "monthly_budget": 2500,
            "total_income": 3000,
            "total_savings": 200,
            "current_day": 15,
            "days_in_month": 30,
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert "financial_health_score" in data
    assert "financial_health_grade" in data
    assert "budget_risk" in data

    assert 0 <= data["financial_health_score"] <= 100
    assert data["financial_health_grade"] in ["A", "B", "C", "D", "F"]
    assert data["budget_risk"] in ["Low", "Medium", "High"]