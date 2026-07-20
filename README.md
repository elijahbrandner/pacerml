# PacerML

PacerML is a local MLOps budgeting prototype that uses transaction data to generate financial insights. The project focuses on transaction categorization, budget risk scoring, and financial health grading.

This project was created for SWE-452 as a practical proof of concept. The goal is not to build a full banking application or polished financial dashboard. Instead, PacerML demonstrates the core machine learning workflow behind a budgeting-focused MLOps system.

## Project Overview

PacerML takes sample transaction data, cleans and preprocesses it, trains a baseline machine learning model, predicts transaction categories, calculates budget risk, and assigns a financial health score and letter grade.

The current Sprint prototype includes:

- Synthetic transaction dataset generation
- Transaction data preprocessing
- Baseline transaction categorization model
- Model evaluation using accuracy and weighted F1 score
- Saved model artifact
- Category prediction script
- Rule-based budget risk scoring
- Financial health score and A-F grade logic
- Full prototype demo script
- Basic validation tests

## Current Scope

The Sprint 3 prototype focuses on the core ML workflow. The following features are intentionally outside the current scope:

- Full user authentication
- Real bank account integration
- Real personal financial data
- Fully deployed production cloud infrastructure
- Polished dashboard UI
- Advanced model retraining automation
- Full-scale monitoring and alerting
- Complete CI/CD deployment to AWS

These features may be considered future enhancements, but the current goal is to keep the prototype practical and focused.

## Project Structure

```text
pacerml/
├── data/
│   └── sample_transactions.csv
├── models/
│   └── category_model.pkl
├── src/
│   ├── budget_risk.py
│   ├── demo.py
│   ├── generate_dataset.py
│   ├── health_score.py
│   ├── predict.py
│   ├── preprocess.py
│   └── train_model.py
├── tests/
│   └── test_outputs.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Technology Stack

- Python
- pandas
- NumPy
- scikit-learn
- joblib
- pytest
- GitHub

## Setup Instructions

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/pacerml.git
cd pacerml
```

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

If using a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Generate the Synthetic Dataset

The project uses synthetic data instead of real financial data.

Run:

```bash
python3 src/generate_dataset.py
```

This creates a balanced transaction dataset with categories such as:

- food
- transportation
- subscriptions
- shopping
- utilities
- entertainment
- housing
- healthcare
- income
- savings

## Preprocess the Data

Run:

```bash
python3 src/preprocess.py
```

The preprocessing pipeline validates the required columns, removes duplicates, handles missing values, standardizes text fields, converts dates, and prepares transaction records for model training.

## Train the Model

Run:

```bash
python3 src/train_model.py
```

The model uses TF-IDF vectorization and Logistic Regression to classify transaction descriptions into spending categories.

Current model performance:

```text
Accuracy: 0.83
Weighted F1 Score: 0.83
```

The trained model is saved locally to:

```text
models/category_model.pkl
```

## Run Category Predictions

Run:

```bash
python3 src/predict.py
```

This loads the saved model and predicts categories for sample transaction descriptions.

Example output:

```text
Starbucks Latte -> food
Chevron Fuel Station -> transportation
Amazon Online Order -> shopping
Electric Utility Payment -> utilities
Monthly Rent -> housing
Payroll Deposit -> income
```

## Run Budget Risk Scoring

Run:

```bash
python3 src/budget_risk.py
```

The budget risk logic classifies spending behavior as:

- Low
- Medium
- High

The risk score compares actual budget usage against expected usage based on the current day of the month.

## Run Financial Health Scoring

Run:

```bash
python3 src/health_score.py
```

The financial health scoring system produces:

- Financial health score from 0 to 100
- Letter grade from A to F
- Budget risk level

Grade scale:

```text
A: 90-100
B: 80-89
C: 70-79
D: 60-69
F: Below 60
```

## Run the Full Prototype Demo

Run:

```bash
python3 src/demo.py
```

The demo script shows the full Sprint 3 prototype workflow:

1. Transaction category predictions
2. Budget risk summary
3. Financial health summary

This is the recommended script for the Sprint 3 video walkthrough.

## Run Tests

Run:

```bash
python3 -m pytest
```

Current test result:

```text
10 passed
```

The tests validate:

- Budget risk output labels
- Budget risk summary fields
- Financial health score range
- Score-to-grade conversion
- Financial health summary fields
- Preprocessing output

## Sprint 3 Status

The Sprint 3 prototype successfully demonstrates the core PacerML workflow. The system can generate synthetic transaction data, preprocess the data, train a baseline ML model, evaluate model performance, predict transaction categories, calculate budget risk, assign financial health grades, and validate key outputs with automated tests.

## Sprint 4 API Prototype

Sprint 4 adds a FastAPI backend that exposes the core PacerML prototype through local API endpoints. This turns the Sprint 3 command-line prototype into a simple ML service.

### Run the API

Before running the API, make sure dependencies are installed:

```bash
python3 -m pip install -r requirements.txt
```

Train the model so the model artifact exists:

```bash
python3 src/train_model.py
```

Start the API server:

```bash
uvicorn app.main:app --reload
```

Open the Swagger API documentation in a browser:

```text
http://127.0.0.1:8000/docs
```

### API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Confirms the API is running |
| POST | `/categorize` | Predicts a transaction category |
| POST | `/budget-risk` | Returns Low, Medium, or High budget risk |
| POST | `/financial-health` | Returns financial health score, grade, and risk |

### Example Category Request

```json
{
  "description": "Starbucks Latte"
}
```

Example response:

```json
{
  "description": "Starbucks Latte",
  "predicted_category": "food"
}
```

### Example Budget Risk Request

```json
{
  "total_expenses": 1600,
  "monthly_budget": 2500,
  "current_day": 15,
  "days_in_month": 30
}
```

Example response includes:

```json
{
  "risk_level": "Medium"
}
```

### Example Financial Health Request

```json
{
  "total_expenses": 1600,
  "monthly_budget": 2500,
  "total_income": 3000,
  "total_savings": 200,
  "current_day": 15,
  "days_in_month": 30
}
```

Example response includes:

```json
{
  "financial_health_score": 80,
  "financial_health_grade": "B",
  "budget_risk": "Medium"
}
```

## Continuous Integration

Sprint 4 also adds a GitHub Actions workflow for basic CI validation. The workflow installs project dependencies, generates the dataset, trains the model, and runs the automated test suite.

Local tests can be run with:

```bash
python3 -m pytest
```

Current local test result:

```text
10 passed
```


