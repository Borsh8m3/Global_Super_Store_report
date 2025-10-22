from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parents[1] / "Global_Superstore2.csv"
EXPECTED_COLUMNS = [
    "Row ID",
    "Order ID",
    "Order Date",
    "Ship Date",
    "Ship Mode",
    "Customer ID",
    "Customer Name",
    "Segment",
    "City",
    "State",
    "Country",
    "Postal Code",
    "Market",
    "Region",
    "Product ID",
    "Category",
    "Sub-Category",
    "Product Name",
    "Sales",
    "Quantity",
    "Discount",
    "Profit",
    "Shipping Cost",
    "Order Priority",
]
CRITICAL_COLUMNS = [
    "Order ID",
    "Order Date",
    "Ship Date",
    "Customer ID",
    "Product ID",
    "Sales",
    "Quantity",
]


def load_dataset() -> tuple[list[dict[str, str]], list[str]]:
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Dataset not found at {DATA_FILE}")

    for encoding in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            with DATA_FILE.open(newline="", encoding=encoding) as csvfile:
                reader = csv.DictReader(csvfile)
                rows = list(reader)
                fieldnames = reader.fieldnames or []
            break
        except UnicodeDecodeError:
            continue
    else:  # pragma: no cover - defensive fallback
        raise UnicodeDecodeError("Unable to decode dataset with supported encodings")

    return rows, fieldnames


def test_dataset_has_expected_structure():
    rows, fieldnames = load_dataset()

    # Ensure the CSV contains all expected columns in the correct order.
    assert fieldnames == EXPECTED_COLUMNS

    # Verify there are no duplicate row identifiers.
    row_id_counts = Counter(row["Row ID"] for row in rows)
    duplicates = [row_id for row_id, count in row_id_counts.items() if count > 1]
    assert not duplicates, f"Dataset contains duplicate Row ID values: {duplicates[:5]}"


def test_dataset_has_no_missing_values_in_critical_columns():
    rows, _ = load_dataset()

    missing_columns = Counter()
    for row in rows:
        for column in CRITICAL_COLUMNS:
            value = row.get(column)
            if value is None or str(value).strip() == "":
                missing_columns[column] += 1

    assert not missing_columns, (
        "Critical columns contain missing values: "
        + ", ".join(f"{column} ({count})" for column, count in missing_columns.items())
    )
