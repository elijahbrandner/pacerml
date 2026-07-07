"""
predict.py

This file loads the trained PacerML transaction categorization model
and uses it to predict categories for new transactions.

For Sprint 3, this provides a simple way to demonstrate that the trained
model can be reused after training. Instead of only showing model metrics,
we can input new transaction descriptions and return predicted categories.
"""

import os

import joblib


# Path to the saved model artifact created by train_model.py.
MODEL_PATH = "models/category_model.pkl"


def load_model(model_path: str = MODEL_PATH):
    """
    Load the trained transaction categorization model.

    Parameters:
        model_path (str): Path to the saved model file.

    Returns:
        The trained scikit-learn pipeline.

    Raises:
        FileNotFoundError: If the model file does not exist.

    Why this matters:
        In an ML system, training and prediction are usually separate steps.
        The saved model artifact allows the system to reuse the trained model
        without retraining it every time a prediction is needed.
    """

    # Check that the trained model file exists before trying to load it.
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Model file not found at {model_path}. "
            "Run python3 src/train_model.py first."
        )

    # Load the saved model pipeline from disk.
    model = joblib.load(model_path)

    return model


def predict_category(description: str, model_path: str = MODEL_PATH) -> str:
    """
    Predict the category for a single transaction description.

    Parameters:
        description (str): Merchant or transaction description.
        model_path (str): Path to the saved model file.

    Returns:
        str: Predicted transaction category.

    Example:
        "Starbucks Coffee" -> "food"
    """

    # Load the trained model.
    model = load_model(model_path)

    # The model expects a list-like input, even for one prediction.
    prediction = model.predict([description])

    # Return the first and only predicted category.
    return prediction[0]


def predict_multiple_categories(descriptions: list[str], model_path: str = MODEL_PATH):
    """
    Predict categories for multiple transaction descriptions.

    Parameters:
        descriptions (list[str]): List of merchant or transaction descriptions.
        model_path (str): Path to the saved model file.

    Returns:
        list[tuple[str, str]]: A list of descriptions paired with predictions.

    Why this matters:
        Batch prediction allows PacerML to categorize multiple uploaded
        transactions at once instead of only one transaction at a time.
    """

    # Load the trained model once.
    model = load_model(model_path)

    # Generate predictions for every description in the list.
    predictions = model.predict(descriptions)

    # Pair each original description with its predicted category.
    results = list(zip(descriptions, predictions))

    return results


# This block runs only when this file is executed directly.
# Run it from the terminal with:
# python3 src/predict.py
if __name__ == "__main__":
    # Example new transactions that are not exactly copied from the dataset.
    sample_descriptions = [
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

    # Predict categories for the sample transactions.
    prediction_results = predict_multiple_categories(sample_descriptions)

    print("PacerML Category Predictions")
    print("----------------------------")

    for description, category in prediction_results:
        print(f"{description} -> {category}")