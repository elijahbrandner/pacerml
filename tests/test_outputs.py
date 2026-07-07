"""
test_outputs.py

Basic tests for the PacerML Sprint 3 prototype.

These tests validate that the main scoring and preprocessing functions return
expected outputs. They are intentionally simple because Sprint 3 focuses on a
working proof of concept, not a full production testing suite.
"""

import sys
from pathlib import Path

# Allow tests to import files from the src folder.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
sys.path.append(str(SRC_PATH))

from budget_risk import classify_budget_risk, summarize_budget_risk
from health_score import (
    calculate_financial_health_score,
    convert_score_to_grade,
    summarize_financial_health,
)
from preprocess import preprocess_transactions


def test_budget_risk_returns_valid_label():
    """
    Test that budget risk classification returns one of the expected labels.
    """

    risk = classify_budget_risk(
        total_expenses=1600,
        monthly_budget=2500,
        current_day=15,
    )

    assert risk in ["Low", "Medium", "High"]


def test_budget_risk_summary_contains_expected_keys():
    """
    Test that the budget risk summary returns the expected output fields.
    """

    summary = summarize_budget_risk(
        total_expenses=1600,
        monthly_budget=2500,
        current_day=15,
    )

    assert "total_expenses" in summary
    assert "monthly_budget" in summary
    assert "remaining_budget" in summary
    assert "actual_usage_percent" in summary
    assert "expected_usage_percent" in summary
    assert "risk_level" in summary


def test_financial_health_score_range():
    """
    Test that the financial health score stays between 0 and 100.
    """

    score = calculate_financial_health_score(
        total_expenses=1600,
        monthly_budget=2500,
        total_income=3000,
        total_savings=200,
        current_day=15,
    )

    assert 0 <= score <= 100


def test_grade_conversion():
    """
    Test that score-to-grade conversion works correctly.
    """

    assert convert_score_to_grade(95) == "A"
    assert convert_score_to_grade(85) == "B"
    assert convert_score_to_grade(75) == "C"
    assert convert_score_to_grade(65) == "D"
    assert convert_score_to_grade(50) == "F"


def test_financial_health_summary_contains_expected_keys():
    """
    Test that the financial health summary returns the expected output fields.
    """

    summary = summarize_financial_health(
        total_expenses=1600,
        monthly_budget=2500,
        total_income=3000,
        total_savings=200,
        current_day=15,
    )

    assert "total_expenses" in summary
    assert "monthly_budget" in summary
    assert "total_income" in summary
    assert "total_savings" in summary
    assert "financial_health_score" in summary
    assert "financial_health_grade" in summary
    assert "budget_risk" in summary


def test_preprocessing_returns_cleaned_data():
    """
    Test that preprocessing loads and cleans the sample transaction dataset.
    """

    data_path = PROJECT_ROOT / "data" / "sample_transactions.csv"

    cleaned_data = preprocess_transactions(str(data_path))

    assert len(cleaned_data) > 0
    assert "description" in cleaned_data.columns
    assert "category" in cleaned_data.columns
    assert "amount" in cleaned_data.columns
    assert cleaned_data["amount"].notnull().all()