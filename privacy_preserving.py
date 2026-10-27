"""
privacy_preserving.py

Add-on privacy-preserving utilities for pandas datasets.
This file is separate so your existing app.py, data_cleaning.py,
userdatabase.py, and utils.py do not need to be edited.

Usage:
    from privacy_preserving import privacy_preserve

    private_df = privacy_preserve(df)
    private_df.to_csv("privacy_preserved_dataset.csv", index=False)

Important:
- This creates a privacy-reduced copy; it does not modify the original DataFrame.
- Pseudonymization is not the same as guaranteed anonymity.
- Review the output before sharing it, especially for rare or identifying values.
"""

import hashlib
import re
from typing import Iterable, Optional

import pandas as pd


# Column names likely to contain direct identifiers or sensitive details.
IDENTIFIER_KEYWORDS = (
    "name",
    "email",
    "phone",
    "mobile",
    "telephone",
    "address",
    "passport",
    "aadhaar",
    "aadhar",
    "ssn",
    "social_security",
    "student_id",
    "employee_id",
    "customer_id",
    "user_id",
    "roll_no",
    "roll number",
    "date_of_birth",
    "dob",
)

EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)
PHONE_PATTERN = re.compile(r"(?<!\w)\+?\d[\d .()\-]{7,}\d(?!\w)")


def _stable_token(value, secret: str = "change-this-secret") -> str:
    """Return a stable pseudonymous token for a non-empty value."""
    if pd.isna(value) or str(value).strip() == "":
        return value
    raw = f"{secret}:{str(value).strip().lower()}".encode("utf-8")
    return "ID_" + hashlib.sha256(raw).hexdigest()[:12]


def _is_identifier_column(column_name: str) -> bool:
    normalized = re.sub(r"[^a-z0-9]+", "_", str(column_name).lower()).strip("_")
    return any(keyword.replace(" ", "_") in normalized for keyword in IDENTIFIER_KEYWORDS)


def _mask_text(value):
    """Mask email addresses and phone-like sequences inside text values."""
    if pd.isna(value):
        return value

    text = str(value)
    text = EMAIL_PATTERN.sub("[EMAIL_REDACTED]", text)
    text = PHONE_PATTERN.sub("[PHONE_REDACTED]", text)
    return text


def privacy_preserve(
    df: pd.DataFrame,
    columns_to_pseudonymize: Optional[Iterable[str]] = None,
    columns_to_drop: Optional[Iterable[str]] = None,
    secret: str = "change-this-secret",
    mask_emails_and_phones: bool = True,
) -> pd.DataFrame:
    """
    Return a privacy-reduced copy of a DataFrame.

    Defaults:
    - Pseudonymizes columns whose names look like direct identifiers.
    - Masks email addresses and phone-like strings in object/string columns.
    - Keeps all columns unless columns_to_drop is explicitly supplied.

    Optional:
        columns_to_pseudonymize=["Student Name", "Roll No"]
        columns_to_drop=["Address"]
        secret="a-private-random-secret"
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")

    private_df = df.copy(deep=True)

    explicit_columns = set(columns_to_pseudonymize or [])
    missing_columns = explicit_columns.difference(private_df.columns)
    if missing_columns:
        raise ValueError(
            "These columns were not found: " + ", ".join(sorted(missing_columns))
        )

    columns_to_process = {
        column for column in private_df.columns
        if _is_identifier_column(str(column))
    }
    columns_to_process.update(explicit_columns)

    for column in columns_to_process:
        private_df[column] = private_df[column].map(
            lambda value: _stable_token(value, secret=secret)
        )

    if mask_emails_and_phones:
        # Do not run text masking on already-pseudonymized identifier columns.
        for column in private_df.select_dtypes(include=["object", "string"]).columns:
            if column not in columns_to_process:
                private_df[column] = private_df[column].map(_mask_text)

    if columns_to_drop:
        missing_drop_columns = set(columns_to_drop).difference(private_df.columns)
        if missing_drop_columns:
            raise ValueError(
                "These columns to drop were not found: "
                + ", ".join(sorted(missing_drop_columns))
            )
        private_df = private_df.drop(columns=list(columns_to_drop))

    return private_df


def privacy_report(original_df: pd.DataFrame, private_df: pd.DataFrame) -> dict:
    """Return a small report of the transformation, without printing row data."""
    return {
        "original_rows": int(original_df.shape[0]),
        "original_columns": int(original_df.shape[1]),
        "output_rows": int(private_df.shape[0]),
        "output_columns": int(private_df.shape[1]),
        "columns_changed_or_removed": [
            column for column in original_df.columns
            if column not in private_df.columns
            or not original_df[column].equals(private_df[column])
        ],
    }


if __name__ == "__main__":
    # Optional standalone test using a tiny example.
    sample = pd.DataFrame({
        "Student Name": ["Asha Devi", "Ravi Singh"],
        "Email": ["asha@example.com", "ravi@example.com"],
        "Phone": ["9876543210", "9123456780"],
        "Marks": [82, 76],
    })

    protected = privacy_preserve(sample, secret="replace-with-your-own-secret")
    print("Privacy-preserved sample:")
    print(protected.to_string(index=False))
