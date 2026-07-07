"""
generate_dataset.py

This script generates a synthetic transaction dataset for the PacerML prototype.

The original dataset was too small for reliable model training, so this script
creates a larger labeled dataset with repeated merchant/category patterns.

For Sprint 3, this keeps the project practical because we are not using real
banking data or personal financial information.
"""

import random
from datetime import datetime, timedelta

import pandas as pd


# Set a random seed so the generated dataset is repeatable.
random.seed(42)


# Each category has sample merchant descriptions that commonly belong to it.
CATEGORY_MERCHANTS = {
    "food": [
        "Starbucks Coffee",
        "Safeway Grocery Store",
        "Chipotle",
        "McDonalds",
        "Costco Wholesale",
        "Trader Joes",
        "Local Restaurant",
        "Subway Sandwiches",
        "Panda Express",
        "Whole Foods Market",
        "Taco Bell",
        "Dunkin Donuts",
        "Foodland Farms",
        "Pizza Hut",
        "Sushi Restaurant",
    ],
    "transportation": [
        "Shell Gas Station",
        "Chevron Gas",
        "Texaco Fuel",
        "Uber Ride",
        "Lyft Ride",
        "Bus Pass",
        "Parking Garage",
        "Auto Repair Shop",
        "Car Wash",
        "Metro Transit",
        "Airport Shuttle",
        "Gas Station Mini Mart",
        "Vehicle Registration",
        "Tire Shop",
        "Taxi Service",
    ],
    "subscriptions": [
        "Netflix Subscription",
        "Spotify Premium",
        "Hulu Subscription",
        "Disney Plus",
        "YouTube Premium",
        "Apple Music",
        "Amazon Prime",
        "Adobe Creative Cloud",
        "iCloud Storage",
        "Xbox Game Pass",
        "PlayStation Plus",
        "Canva Pro",
        "Notion Plus",
        "Gym App Subscription",
        "Streaming Service",
    ],
    "shopping": [
        "Amazon Marketplace",
        "Target Store",
        "Walmart Supercenter",
        "Best Buy",
        "Old Navy",
        "Nordstrom Rack",
        "GameStop",
        "Apple Store",
        "Nike Store",
        "Home Depot",
        "Ross Dress For Less",
        "Marshalls",
        "Etsy Purchase",
        "Online Retail Store",
        "Electronics Store",
    ],
    "utilities": [
        "Electric Company Bill",
        "Water Utility Bill",
        "Internet Service Provider",
        "Gas Utility Bill",
        "Phone Bill",
        "Trash Service",
        "Cable Company",
        "Sewer Utility",
        "Home Internet Bill",
        "Cell Phone Provider",
        "Energy Service",
        "Utility AutoPay",
        "Broadband Payment",
        "City Water Department",
        "Power Company",
    ],
    "entertainment": [
        "Movie Theater",
        "Concert Tickets",
        "Bowling Alley",
        "Arcade",
        "Mini Golf",
        "Theme Park",
        "Museum Tickets",
        "Sports Event Tickets",
        "Escape Room",
        "Comedy Club",
        "Eventbrite Tickets",
        "Gaming Cafe",
        "Karaoke Night",
        "Live Music Venue",
        "Recreation Center",
    ],
    "housing": [
        "Rent Payment",
        "Apartment Rent",
        "Mortgage Payment",
        "Property Management",
        "HOA Payment",
        "Storage Unit Rent",
        "Renter Insurance",
        "Home Insurance",
        "Apartment Deposit",
        "Landlord Payment",
        "Housing Fee",
        "Room Rental",
        "Dorm Housing Payment",
        "Lease Payment",
        "Property Tax Payment",
    ],
    "healthcare": [
        "Health Insurance",
        "Longs Drugs Pharmacy",
        "Dental Clinic",
        "Doctor Office",
        "Urgent Care",
        "Vision Center",
        "CVS Pharmacy",
        "Walgreens Pharmacy",
        "Physical Therapy",
        "Medical Copay",
        "Hospital Billing",
        "Prescription Refill",
        "Eye Exam",
        "Clinic Visit",
        "Chiropractor",
    ],
    "income": [
        "Paycheck Deposit",
        "Direct Deposit Payroll",
        "Freelance Payment",
        "Refund Deposit",
        "Scholarship Deposit",
        "Bonus Payment",
        "Part Time Job Pay",
        "Venmo Received",
        "Zelle Received",
        "Tax Refund",
        "Cash Deposit",
        "Reimbursement",
        "Interest Payment",
        "Side Hustle Income",
        "Commission Payment",
    ],
    "savings": [
        "Savings Transfer",
        "Emergency Fund Transfer",
        "Roth IRA Contribution",
        "Investment Transfer",
        "Brokerage Deposit",
        "High Yield Savings Transfer",
        "Automatic Savings",
        "Retirement Contribution",
        "Vacation Fund Transfer",
        "Money Market Deposit",
        "Transfer to Savings",
        "Fidelity Contribution",
        "Ally Savings Transfer",
        "Future Fund Transfer",
        "Long Term Savings",
    ],
}


# Amount ranges help make transactions look more realistic by category.
AMOUNT_RANGES = {
    "food": (5, 150),
    "transportation": (10, 180),
    "subscriptions": (5, 40),
    "shopping": (20, 350),
    "utilities": (35, 250),
    "entertainment": (15, 180),
    "housing": (700, 1800),
    "healthcare": (20, 300),
    "income": (500, 2500),
    "savings": (50, 700),
}


def generate_transactions(records_per_category: int = 25) -> pd.DataFrame:
    """
    Generate synthetic transaction records.

    Parameters:
        records_per_category (int): Number of transactions to create per category.

    Returns:
        pd.DataFrame: Synthetic labeled transaction dataset.
    """

    rows = []
    transaction_counter = 1
    start_date = datetime(2026, 6, 1)

    user_ids = ["user-001", "user-002", "user-003", "user-004"]
    monthly_budgets = {
        "user-001": 2500,
        "user-002": 1800,
        "user-003": 3200,
        "user-004": 2200,
    }

    for category, merchants in CATEGORY_MERCHANTS.items():
        min_amount, max_amount = AMOUNT_RANGES[category]

        for _ in range(records_per_category):
            user_id = random.choice(user_ids)
            merchant = random.choice(merchants)

            # Spread dates across the month.
            transaction_date = start_date + timedelta(days=random.randint(0, 29))

            # Generate a realistic amount for the category.
            amount = round(random.uniform(min_amount, max_amount), 2)

            # Income and savings are not normal expenses.
            if category == "income":
                transaction_type = "income"
            elif category == "savings":
                transaction_type = "transfer"
            else:
                transaction_type = "expense"

            rows.append(
                {
                    "transaction_id": f"txn-{transaction_counter:04d}",
                    "user_id": user_id,
                    "transaction_date": transaction_date.strftime("%Y-%m-%d"),
                    "description": merchant,
                    "amount": amount,
                    "transaction_type": transaction_type,
                    "category": category,
                    "monthly_budget": monthly_budgets[user_id],
                }
            )

            transaction_counter += 1

    df = pd.DataFrame(rows)

    # Shuffle rows so categories are mixed instead of grouped together.
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    return df


if __name__ == "__main__":
    output_path = "data/sample_transactions.csv"

    dataset = generate_transactions(records_per_category=25)
    dataset.to_csv(output_path, index=False)

    print("Synthetic dataset generated.")
    print(f"Rows created: {len(dataset)}")
    print(f"Saved to: {output_path}")
    print(dataset.head())