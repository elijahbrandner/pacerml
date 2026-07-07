"""
train_model.py

This file trains the first machine learning model for PacerML.

For Sprint 3, the goal is to build a baseline transaction categorization model.
The model uses transaction descriptions to predict spending categories such as
food, transportation, shopping, utilities, entertainment, subscriptions, income,
healthcare, housing, and savings.

This is intentionally simple and practical for the prototype. Later versions of
the project could include more features such as transaction amount, date, user
history, and budget behavior.
"""

import os

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from preprocess import preprocess_transactions


# Path to the sample training dataset.
DATA_PATH = "data/sample_transactions.csv"

# Path where the trained model will be saved.
MODEL_PATH = "models/category_model.pkl"


def train_category_model(data_path: str = DATA_PATH) -> Pipeline:
    """
    Train a transaction categorization model.

    Parameters:
        data_path (str): Path to the transaction CSV file.

    Returns:
        Pipeline: A trained scikit-learn pipeline.

    Model approach:
        1. TF-IDF converts transaction descriptions into numeric features.
        2. Logistic Regression learns patterns between descriptions and categories.

    Why this matters:
        Machine learning models cannot directly understand text. TF-IDF converts
        words into numbers, and Logistic Regression uses those numbers to predict
        the most likely spending category.
    """

    # Load and clean the transaction dataset using our preprocessing pipeline.
    df = preprocess_transactions(data_path)

    # X is the input feature.
    # For the baseline model, we are only using the transaction description.
    X = df["description"]

    # y is the target label the model is trying to predict.
    # In this case, it is the known transaction category.
    y = df["category"]

    # Split the dataset into training and testing sets.
    # The training set teaches the model, while the test set checks how well it
    # performs on data it has not seen before.
    #
    # stratify=y helps keep category distribution similar in both splits.
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )

    # Create a machine learning pipeline.
    # A pipeline keeps the text vectorizer and model together so they can be
    # trained, saved, and loaded as one object.
    model = Pipeline(
        steps=[
            (
                "tfidf",
                TfidfVectorizer(
                    stop_words="english",
                    lowercase=True,
                ),
            ),
            (
                "classifier",
                LogisticRegression(
                    max_iter=1000,
                    random_state=42,
                ),
            ),
        ]
    )

    # Train the model using the training data.
    model.fit(X_train, y_train)

    # Generate predictions on the test data.
    y_pred = model.predict(X_test)

    # Evaluate the model using accuracy and weighted F1 score.
    accuracy = accuracy_score(y_test, y_pred)
    weighted_f1 = f1_score(y_test, y_pred, average="weighted")

    # Print results so they can be shown in the demo and documented later.
    print("Model training complete.")
    print(f"Accuracy: {accuracy:.2f}")
    print(f"Weighted F1 Score: {weighted_f1:.2f}")
    print()
    print("Classification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))

    # Make sure the models folder exists.
    os.makedirs("models", exist_ok=True)

    # Save the trained pipeline to disk.
    # This creates a reusable model artifact for prediction.
    joblib.dump(model, MODEL_PATH)

    print(f"Model saved to: {MODEL_PATH}")

    return model


# This block runs only when the file is executed directly.
# Run it from the terminal with:
# python src/train_model.py
if __name__ == "__main__":
    train_category_model()