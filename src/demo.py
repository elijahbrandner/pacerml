"""
demo.py

This file provides one complete Sprint 3 demo for PacerML.

The purpose of this script is to show the main prototype workflow in one place:

1. Load the trained transaction categorization model.
2. Predict categories for new sample transactions.
3. Calculate budget risk.
4. Calculate a financial health score.
5. Convert the score into an A-F grade.

This is the best file to run during the Sprint 3 video walkthrough because it
demonstrates the core prototype without needing a full website or dashboard.
"""

from predict import predict_multiple_categories
from budget_risk import summarize_budget_risk
from health_score import summarize_financial_health


def run_category_prediction_demo() -> None:
    """
    Demonstrate transaction category prediction.

    This uses the trained model saved in models/category_model.pkl.
    The model predicts categories based on transaction descriptions.
    """

    sample_transactions = [
        "Starbucks Latte",
        "Chevron Fuel Station",
        "Netflix Monthly Payment",
        "Amazon Online Order",
        "Electric Utility Payment",
        "Movie Tickets",
        "Monthly Rent",
        "CVS Prescription",
        "Payroll Deposit",
        "Transfer to Savings Account",
    ]

    predictions = predict_multiple_categories(sample_transactions)

    print("1. Transaction Category Predictions")
    print("-----------------------------------")

    for description, category in predictions:
        print(f"{description} -> {category}")


def run_budget_risk_demo() -> None:
    """
    Demonstrate budget risk classification.

    This uses rule-based logic to compare current spending against expected
    spending pace for the month.
    """

    total_expenses = 1600
    monthly_budget = 2500
    current_day = 15

    summary = summarize_budget_risk(
        total_expenses=total_expenses,
        monthly_budget=monthly_budget,
        current_day=current_day,
    )

    print()
    print("2. Budget Risk Summary")
    print("----------------------")
    print(f"Total Expenses: ${summary['total_expenses']}")
    print(f"Monthly Budget: ${summary['monthly_budget']}")
    print(f"Remaining Budget: ${summary['remaining_budget']}")
    print(f"Actual Usage: {summary['actual_usage_percent']}%")
    print(f"Expected Usage: {summary['expected_usage_percent']}%")
    print(f"Risk Level: {summary['risk_level']}")


def run_financial_health_demo() -> None:
    """
    Demonstrate financial health scoring.

    This calculates a 0-100 score and converts that score into an A-F grade.
    """

    total_expenses = 1600
    monthly_budget = 2500
    total_income = 3000
    total_savings = 200
    current_day = 15

    summary = summarize_financial_health(
        total_expenses=total_expenses,
        monthly_budget=monthly_budget,
        total_income=total_income,
        total_savings=total_savings,
        current_day=current_day,
    )

    print()
    print("3. Financial Health Summary")
    print("---------------------------")
    print(f"Total Expenses: ${summary['total_expenses']}")
    print(f"Monthly Budget: ${summary['monthly_budget']}")
    print(f"Total Income: ${summary['total_income']}")
    print(f"Total Savings: ${summary['total_savings']}")
    print(f"Budget Risk: {summary['budget_risk']}")
    print(f"Financial Health Score: {summary['financial_health_score']}")
    print(f"Financial Health Grade: {summary['financial_health_grade']}")


def main() -> None:
    """
    Run the full PacerML Sprint 3 demo.
    """

    print("PacerML Sprint 3 Prototype Demo")
    print("===============================")
    print()

    run_category_prediction_demo()
    run_budget_risk_demo()
    run_financial_health_demo()

    print()
    print("Demo complete.")


if __name__ == "__main__":
    main()