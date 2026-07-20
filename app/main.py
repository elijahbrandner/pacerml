"""
main.py

FastAPI backend for the PacerML Sprint 4 prototype.

This API exposes the core PacerML functionality through simple local endpoints:
- Health check
- Transaction category prediction
- Budget risk scoring
- Financial health scoring

This turns the Sprint 3 command-line prototype into a basic ML service.
"""

import sys
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel

# Allows this file to import modules from the src folder.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
sys.path.append(str(SRC_PATH))

from predict import predict_category
from budget_risk import summarize_budget_risk
from health_score import summarize_financial_health


app = FastAPI(
    title="PacerML API",
    description="Local API service for transaction categorization, budget risk scoring, and financial health grading.",
    version="1.0.0",
)


class CategoryRequest(BaseModel):
    """
    Request body for transaction category prediction.
    """

    description: str


class BudgetRiskRequest(BaseModel):
    """
    Request body for budget risk scoring.
    """

    total_expenses: float
    monthly_budget: float
    current_day: int
    days_in_month: int = 30


class FinancialHealthRequest(BaseModel):
    """
    Request body for financial health scoring.
    """

    total_expenses: float
    monthly_budget: float
    total_income: float
    total_savings: float
    current_day: int
    days_in_month: int = 30


@app.get("/health")
def health_check() -> dict:
    """
    Basic API health check.

    Returns:
        dict: API status message.
    """

    return {
        "status": "ok",
        "message": "PacerML API is running.",
    }


@app.post("/categorize")
def categorize_transaction(request: CategoryRequest) -> dict:
    """
    Predict the category of a transaction description.

    Example input:
        {
            "description": "Starbucks Latte"
        }
    """

    predicted_category = predict_category(request.description)

    return {
        "description": request.description,
        "predicted_category": predicted_category,
    }


@app.post("/budget-risk")
def get_budget_risk(request: BudgetRiskRequest) -> dict:
    """
    Calculate budget risk based on current spending pace.

    Example input:
        {
            "total_expenses": 1600,
            "monthly_budget": 2500,
            "current_day": 15
        }
    """

    summary = summarize_budget_risk(
        total_expenses=request.total_expenses,
        monthly_budget=request.monthly_budget,
        current_day=request.current_day,
        days_in_month=request.days_in_month,
    )

    return summary


@app.post("/financial-health")
def get_financial_health(request: FinancialHealthRequest) -> dict:
    """
    Calculate financial health score and grade.

    Example input:
        {
            "total_expenses": 1600,
            "monthly_budget": 2500,
            "total_income": 3000,
            "total_savings": 200,
            "current_day": 15
        }
    """

    summary = summarize_financial_health(
        total_expenses=request.total_expenses,
        monthly_budget=request.monthly_budget,
        total_income=request.total_income,
        total_savings=request.total_savings,
        current_day=request.current_day,
        days_in_month=request.days_in_month,
    )

    return summary