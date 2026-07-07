"""
health_score.py

This file calculates the financial health score and letter grade for PacerML.

For Sprint 3, the score is calculated using a rule-based approach. This keeps
the prototype simple, explainable, and practical.

The financial health score ranges from 0 to 100.

Grade scale:
    A: 90-100
    B: 80-89
    C: 70-79
    D: 60-69
    F: Below 60
"""

from budget_risk import classify_budget_risk


def calculate_savings_rate(total_savings: float, total_income: float) -> float:
    """
    Calculate the user's savings rate.

    Parameters:
        total_savings (float): Total amount transferred to savings.
        total_income (float): Total income received.

    Returns:
        float: Savings rate as a decimal.

    Example:
        total_savings = 300
        total_income = 3000
        return value = 0.10
    """

    # If income is zero or negative, savings rate cannot be calculated safely.
    if total_income <= 0:
        return 0.0

    return total_savings / total_income


def calculate_financial_health_score(
    total_expenses: float,
    monthly_budget: float,
    total_income: float,
    total_savings: float,
    current_day: int,
    days_in_month: int = 30,
) -> int:
    """
    Calculate a financial health score from 0 to 100.

    Parameters:
        total_expenses (float): Total expenses so far for the month.
        monthly_budget (float): User's monthly budget.
        total_income (float): Total income so far for the month.
        total_savings (float): Total amount saved so far for the month.
        current_day (int): Current day of the month.
        days_in_month (int): Number of days in the month.

    Returns:
        int: Financial health score between 0 and 100.

    Scoring logic:
        The score starts at 100 and subtracts points for risk factors.

        Main factors:
            - Budget usage
            - Budget risk level
            - Expenses compared to income
            - Savings rate

    Why this matters:
        The letter grade gives users a simple way to understand their overall
        budget position without needing to interpret every transaction manually.
    """

    # Start with a perfect score.
    score = 100

    # Prevent invalid budget calculations.
    if monthly_budget <= 0:
        raise ValueError("Monthly budget must be greater than zero.")

    # Calculate budget usage as a decimal.
    budget_usage = total_expenses / monthly_budget

    # Get budget risk using the existing budget risk logic.
    risk_level = classify_budget_risk(
        total_expenses=total_expenses,
        monthly_budget=monthly_budget,
        current_day=current_day,
        days_in_month=days_in_month,
    )

    # Calculate expenses compared to income.
    # If income is zero, use 1.0 as a conservative fallback.
    if total_income > 0:
        expense_to_income_ratio = total_expenses / total_income
    else:
        expense_to_income_ratio = 1.0

    # Calculate savings rate.
    savings_rate = calculate_savings_rate(total_savings, total_income)

    # Budget usage penalty.
    # Higher budget usage means fewer points.
    if budget_usage >= 1.00:
        score -= 35
    elif budget_usage >= 0.90:
        score -= 25
    elif budget_usage >= 0.75:
        score -= 15
    elif budget_usage >= 0.50:
        score -= 8

    # Budget risk penalty.
    if risk_level == "High":
        score -= 25
    elif risk_level == "Medium":
        score -= 12

    # Expense-to-income penalty.
    # Spending too much of income lowers the financial health score.
    if expense_to_income_ratio >= 1.00:
        score -= 20
    elif expense_to_income_ratio >= 0.80:
        score -= 12
    elif expense_to_income_ratio >= 0.60:
        score -= 6

    # Savings adjustment.
    # Strong savings behavior improves or protects the score.
    if savings_rate >= 0.20:
        score += 5
    elif savings_rate < 0.05:
        score -= 8

    # Keep score inside the 0-100 range.
    score = max(0, min(100, score))

    return round(score)


def convert_score_to_grade(score: int) -> str:
    """
    Convert a financial health score into a letter grade.

    Parameters:
        score (int): Financial health score from 0 to 100.

    Returns:
        str: Letter grade from A to F.
    """

    if score >= 90:
        return "A"

    if score >= 80:
        return "B"

    if score >= 70:
        return "C"

    if score >= 60:
        return "D"

    return "F"


def summarize_financial_health(
    total_expenses: float,
    monthly_budget: float,
    total_income: float,
    total_savings: float,
    current_day: int,
    days_in_month: int = 30,
) -> dict:
    """
    Return a full financial health summary.

    Parameters:
        total_expenses (float): Total expenses so far.
        monthly_budget (float): User's monthly budget.
        total_income (float): Total income so far.
        total_savings (float): Total savings so far.
        current_day (int): Current day of the month.
        days_in_month (int): Total days in month.

    Returns:
        dict: Financial health score summary.

    This function is useful for the demo because it returns both the numeric
    score and the letter grade.
    """

    score = calculate_financial_health_score(
        total_expenses=total_expenses,
        monthly_budget=monthly_budget,
        total_income=total_income,
        total_savings=total_savings,
        current_day=current_day,
        days_in_month=days_in_month,
    )

    grade = convert_score_to_grade(score)

    risk_level = classify_budget_risk(
        total_expenses=total_expenses,
        monthly_budget=monthly_budget,
        current_day=current_day,
        days_in_month=days_in_month,
    )

    return {
        "total_expenses": round(total_expenses, 2),
        "monthly_budget": round(monthly_budget, 2),
        "total_income": round(total_income, 2),
        "total_savings": round(total_savings, 2),
        "financial_health_score": score,
        "financial_health_grade": grade,
        "budget_risk": risk_level,
    }


# This block runs only when this file is executed directly.
# Run it from the terminal with:
# python3 src/health_score.py
if __name__ == "__main__":
    example_users = [
        {
            "name": "Strong Budget Health",
            "total_expenses": 900,
            "monthly_budget": 2500,
            "total_income": 3000,
            "total_savings": 600,
            "current_day": 15,
        },
        {
            "name": "Average Budget Health",
            "total_expenses": 1600,
            "monthly_budget": 2500,
            "total_income": 3000,
            "total_savings": 200,
            "current_day": 15,
        },
        {
            "name": "Poor Budget Health",
            "total_expenses": 2450,
            "monthly_budget": 2500,
            "total_income": 2600,
            "total_savings": 50,
            "current_day": 15,
        },
    ]

    print("PacerML Financial Health Demo")
    print("-----------------------------")

    for user in example_users:
        summary = summarize_financial_health(
            total_expenses=user["total_expenses"],
            monthly_budget=user["monthly_budget"],
            total_income=user["total_income"],
            total_savings=user["total_savings"],
            current_day=user["current_day"],
        )

        print()
        print(user["name"])
        print(f"Total Expenses: ${summary['total_expenses']}")
        print(f"Monthly Budget: ${summary['monthly_budget']}")
        print(f"Total Income: ${summary['total_income']}")
        print(f"Total Savings: ${summary['total_savings']}")
        print(f"Budget Risk: {summary['budget_risk']}")
        print(f"Financial Health Score: {summary['financial_health_score']}")
        print(f"Financial Health Grade: {summary['financial_health_grade']}")