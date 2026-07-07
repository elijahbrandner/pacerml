"""
budget_risk.py

This file contains the budget risk scoring logic for PacerML.

For Sprint 3, budget risk is calculated using a rule-based approach instead
of a separate machine learning model. This keeps the prototype practical while
still providing useful financial insight.

The purpose of this file is to classify a user's budget risk as:
    - Low
    - Medium
    - High

The risk level is based on how much of the monthly budget has already been used
compared to how far into the month the user is.
"""


def calculate_budget_usage(total_expenses: float, monthly_budget: float) -> float:
    """
    Calculate the percentage of the monthly budget already used.

    Parameters:
        total_expenses (float): Total expenses so far for the month.
        monthly_budget (float): User's monthly budget limit.

    Returns:
        float: Budget usage percentage as a decimal.

    Example:
        total_expenses = 1000
        monthly_budget = 2500
        return value = 0.40
    """

    # A monthly budget must be greater than zero to avoid division by zero.
    if monthly_budget <= 0:
        raise ValueError("Monthly budget must be greater than zero.")

    # Divide expenses by budget to calculate usage.
    return total_expenses / monthly_budget


def calculate_expected_usage(current_day: int, days_in_month: int = 30) -> float:
    """
    Calculate how much of the budget the user is expected to have used by now.

    Parameters:
        current_day (int): Current day of the month.
        days_in_month (int): Total number of days in the month.

    Returns:
        float: Expected budget usage percentage as a decimal.

    Example:
        current_day = 15
        days_in_month = 30
        return value = 0.50
    """

    # Validate the day values to avoid impossible calculations.
    if current_day < 1:
        raise ValueError("Current day must be at least 1.")

    if days_in_month < 1:
        raise ValueError("Days in month must be at least 1.")

    if current_day > days_in_month:
        current_day = days_in_month

    # Expected usage is based on how much of the month has passed.
    return current_day / days_in_month


def classify_budget_risk(
    total_expenses: float,
    monthly_budget: float,
    current_day: int,
    days_in_month: int = 30,
) -> str:
    """
    Classify budget risk as Low, Medium, or High.

    Parameters:
        total_expenses (float): Total expenses so far for the month.
        monthly_budget (float): User's monthly budget.
        current_day (int): Current day of the month.
        days_in_month (int): Total number of days in the month.

    Returns:
        str: Budget risk level: "Low", "Medium", or "High".

    Logic:
        - Low risk: Spending is on pace or below expected usage.
        - Medium risk: Spending is moderately above expected usage.
        - High risk: Spending is far above expected usage or budget is nearly used.

    Why this matters:
        This gives users a simple early warning system. Instead of waiting until
        the end of the month, PacerML can show whether spending is currently
        moving too fast compared to the budget.
    """

    # Calculate actual and expected budget usage.
    actual_usage = calculate_budget_usage(total_expenses, monthly_budget)
    expected_usage = calculate_expected_usage(current_day, days_in_month)

    # Difference between actual spending pace and expected spending pace.
    usage_gap = actual_usage - expected_usage

    # High risk if the user has already used almost all of the budget
    # or is significantly ahead of expected spending pace.
    if actual_usage >= 0.90 or usage_gap >= 0.25:
        return "High"

    # Medium risk if the user is somewhat above expected spending pace.
    if actual_usage >= 0.75 or usage_gap >= 0.10:
        return "Medium"

    # Low risk means spending is on pace or below expected pace.
    return "Low"


def summarize_budget_risk(
    total_expenses: float,
    monthly_budget: float,
    current_day: int,
    days_in_month: int = 30,
) -> dict:
    """
    Return a full budget risk summary.

    Parameters:
        total_expenses (float): Total expenses so far.
        monthly_budget (float): Monthly budget amount.
        current_day (int): Current day of the month.
        days_in_month (int): Total days in month.

    Returns:
        dict: Budget risk summary with usage details.

    This function is useful for demos because it returns more than just the
    risk label. It also shows the actual usage, expected usage, and remaining
    budget.
    """

    actual_usage = calculate_budget_usage(total_expenses, monthly_budget)
    expected_usage = calculate_expected_usage(current_day, days_in_month)
    risk_level = classify_budget_risk(
        total_expenses,
        monthly_budget,
        current_day,
        days_in_month,
    )

    remaining_budget = monthly_budget - total_expenses

    return {
        "total_expenses": round(total_expenses, 2),
        "monthly_budget": round(monthly_budget, 2),
        "remaining_budget": round(remaining_budget, 2),
        "actual_usage_percent": round(actual_usage * 100, 2),
        "expected_usage_percent": round(expected_usage * 100, 2),
        "risk_level": risk_level,
    }


# This block runs only when this file is executed directly.
# Run it from the terminal with:
# python3 src/budget_risk.py
if __name__ == "__main__":
    # Example scenarios for demonstration.
    example_scenarios = [
        {
            "name": "Low Risk Example",
            "total_expenses": 600,
            "monthly_budget": 2500,
            "current_day": 15,
        },
        {
            "name": "Medium Risk Example",
            "total_expenses": 1600,
            "monthly_budget": 2500,
            "current_day": 15,
        },
        {
            "name": "High Risk Example",
            "total_expenses": 2300,
            "monthly_budget": 2500,
            "current_day": 15,
        },
    ]

    print("PacerML Budget Risk Demo")
    print("------------------------")

    for scenario in example_scenarios:
        summary = summarize_budget_risk(
            total_expenses=scenario["total_expenses"],
            monthly_budget=scenario["monthly_budget"],
            current_day=scenario["current_day"],
        )

        print()
        print(scenario["name"])
        print(f"Total Expenses: ${summary['total_expenses']}")
        print(f"Monthly Budget: ${summary['monthly_budget']}")
        print(f"Remaining Budget: ${summary['remaining_budget']}")
        print(f"Actual Usage: {summary['actual_usage_percent']}%")
        print(f"Expected Usage: {summary['expected_usage_percent']}%")
        print(f"Risk Level: {summary['risk_level']}")