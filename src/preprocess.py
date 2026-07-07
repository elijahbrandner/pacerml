# Elijah Brandner
# PacerML
# Preprocess.py
# July 6 2026

# This file contains the preprocessing pipeline for PacerML.

# The purpose of preprocessing is to take raw transaction data from a CSV file,
# validate that the required fields exist, clean inconsistent or invalid data,
# and prepare the dataset for machine learning model training.

# Pandas is an open source library helpful for data manipulation, cleaning and analysis
import pandas as pd


# These are the columns that every transaction CSV must include.
# If any of these columns are missing, the preprocessing pipeline should stop
# and return an error instead of training on incomplete data.

REQUIRED_COLUMNS = [
    "transaction_id",
    "user_id",
    "transaction_date",
    "description",
    "amount",
    "transaction_type",
    "category",
    "monthly_budget",
]



def load_transactions(file_path: str) -> pd.DataFrame:
    """
    Loads transaction data from a CSV file.
    Parameters:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Raw transaction data loaded into a pandas DataFrame.

    Raises:
        FileNotFoundError: If the CSV file path does not exist.
        ValueError: If the CSV file is empty or cannot be parsed.

    Why this matters:
        The ML pipeline needs transaction data in a structured table format.
        Pandas DataFrames make it easier to clean, transform, and prepare
        the data for model training.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except pd.errors.EmptyDataError:
        raise ValueError("The CSV file is empty.")
    except pd.errors.ParserError:
        raise ValueError("The CSV file could not be parsed.")


def validate_columns(df: pd.DataFrame) -> None:
    """
    Validate that the dataset contains all required columns.

    Parameters:
        df (pd.DataFrame): Transaction dataset.

    Returns:
        None

    Raises:
        ValueError: If one or more required columns are missing.

    Why this matters:
        The model expects specific columns such as description, amount,
        transaction type, and category. If these fields are missing, the
        training process would fail or produce unreliable results.
    """

     # Create a list of required columns that are not present in the dataset.
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]

    # Stop the pipeline if any required columns are missing.
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")


def clean_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and standardize transaction data for model training.

    Parameters:
        df (pd.DataFrame): Raw transaction dataset.

    Returns:
        pd.DataFrame: Cleaned transaction dataset.

    Main cleaning steps:
        1. Validate required columns.
        2. Remove duplicate transactions.
        3. Remove rows missing critical values.
        4. Convert transaction dates into datetime format.
        5. Standardize text fields.
        6. Convert amount and monthly budget fields into numbers.
        7. Remove invalid budget values.
        8. Add date-based features for future model training.

    Why this matters:
        Machine learning models perform better when the input data is clean,
        consistent, and structured. This function reduces common data quality
        problems before training begins.    
        """
    
    # First, make sure the dataset has every required column.
    validate_columns(df)

    # Make a copy of the original DataFrame so we do not accidentally modify
    # the raw dataset directly.
    cleaned_df = df.copy()

    # Remove duplicate transactions using transaction_id.
    # This prevents the same purchase from being counted multiple times.    
    cleaned_df = cleaned_df.drop_duplicates(subset=["transaction_id"])

    # Remove rows missing critical fields
    # These fields are required for training, scoring, and evaluation.
    cleaned_df = cleaned_df.dropna(
        subset=[
            "transaction_id",
            "user_id",
            "transaction_date",
            "description",
            "amount",
            "transaction_type",
            "category",
            "monthly_budget",
        ]
    )

    # Convert transaction_date from text into a real datetime object.
    # errors="coerce" turns invalid dates into NaT, which can be removed later.
    cleaned_df["transaction_date"] = pd.to_datetime(
        cleaned_df["transaction_date"], errors="coerce"
    )

    # Remove rows where the date could not be converted properly.
    cleaned_df = cleaned_df.dropna(subset=["transaction_date"])

    # Standardize the transaction description.
    # Lowercasing and stripping spaces helps the model treat similar merchant
    # names more consistently.
    cleaned_df["description"] = (
        cleaned_df["description"]
        .astype(str)
        .str.lower()
        .str.strip()
    )

    # Standardize transaction_type values such as "expense", "income", or "transfer".
    cleaned_df["transaction_type"] = (
        cleaned_df["transaction_type"]
        .astype(str)
        .str.lower()
        .str.strip()
    )

    # Standardize category labels such as "food", "shopping", or "utilities".
    cleaned_df["category"] = (
        cleaned_df["category"]
        .astype(str)
        .str.lower()
        .str.strip()
    )

    # Convert numeric columns
    # Invalid numbers become NaN and are removed in the next step.
    cleaned_df["amount"] = pd.to_numeric(cleaned_df["amount"], errors="coerce")
    cleaned_df["monthly_budget"] = pd.to_numeric(
        cleaned_df["monthly_budget"], errors="coerce"
    )

    # Remove invalid numeric rows
    cleaned_df = cleaned_df.dropna(subset=["amount", "monthly_budget"])

    # Remove impossible budget values
    cleaned_df = cleaned_df[cleaned_df["monthly_budget"] > 0]

    # Add date-based features that may be useful for later models.
    # These features are not required for the first simple model, but they
    # prepare the dataset for future budget risk prediction improvements.    cleaned_df["day_of_month"] = cleaned_df["transaction_date"].dt.day
    cleaned_df["day_of_week"] = cleaned_df["transaction_date"].dt.dayofweek
    cleaned_df["month"] = cleaned_df["transaction_date"].dt.month

    # Return the final cleaned dataset.
    return cleaned_df


def preprocess_transactions(file_path: str) -> pd.DataFrame:
    """
    Run the full preprocessing pipeline.

    Parameters:
        file_path (str): Path to the transaction CSV file.

    Returns:
        pd.DataFrame: Cleaned transaction dataset.

    Pipeline flow:
        1. Load raw transaction data.
        2. Clean and validate transaction data.
        3. Return cleaned dataset for training or prediction.
    """

    # Load raw data from the CSV file.
    df = load_transactions(file_path)

    # Clean and standardize the raw data.
    cleaned_df = clean_transactions(df)
    return cleaned_df

# This block only runs when this file is executed directly.
# It allows us to test preprocessing from the terminal by running:
# python src/preprocess.py
if __name__ == "__main__":
    # Path to the sample transaction dataset.
    data_path = "data/sample_transactions.csv"

    # Run the preprocessing pipeline.
    cleaned_transactions = preprocess_transactions(data_path)

    # Print a simple confirmation message.
    print("Preprocessing complete.")

    # Show how many rows remain after cleaning.
    print(f"Rows after cleaning: {len(cleaned_transactions)}")

    # Display the first few cleaned rows so we can visually confirm the output.
    print(cleaned_transactions.head())