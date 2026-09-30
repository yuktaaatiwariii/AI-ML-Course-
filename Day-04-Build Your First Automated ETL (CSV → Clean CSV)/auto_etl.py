
import os
import time
import pandas as pd
import schedule
from datetime import datetime

# File paths
RAW_PATH = "telecom_raw.csv"
OUT_DIR = "output"
OUT_PATH = os.path.join(OUT_DIR, "telecom_cleaned.csv")
TMP_PATH = os.path.join(OUT_DIR, "telecom_cleaned.tmp.csv")
LOG_PATH = os.path.join(OUT_DIR, "etl_run.log")

# Create output folder if it does not exist
os.makedirs(OUT_DIR, exist_ok=True)


def log(msg: str):
    """Write a timestamped message to the log file and console."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {msg}\n")

    print(f"[{ts}] {msg}")


def clean_frame(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize telecom usage data."""

    # 1. Standardize region text
    if "region" in df.columns:
        df["region"] = (
            df["region"]
            .astype("string")
            .str.strip()
            .str.title()
        )

    # 2. Convert numeric columns and fill missing values with median
    numeric_columns = ["data_used_gb", "calls_made", "revenue_inr"]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

            median_value = df[col].median()

            # If the entire column is missing, median is NaN.
            # In that case, leave missing values unchanged and log it.
            if pd.notna(median_value):
                df[col] = df[col].fillna(median_value)
            else:
                log(f"No median available for {col}; missing values remain.")

    # 3. Parse dates and replace invalid/missing dates with the default
    if "date" in df.columns:
        df["date"] = pd.to_datetime(
            df["date"],
            format="mixed",
            errors="coerce",
            dayfirst=True
        )

        df["date"] = df["date"].fillna(pd.Timestamp("2025-09-25"))

    # 4. Remove duplicates based on customer ID and date
    if {"customer_id", "date"}.issubset(df.columns):
        before = len(df)

        df = df.drop_duplicates(
            subset=["customer_id", "date"],
            keep="first"
        )

        removed = before - len(df)
        log(f"Deduplicated: removed {removed} duplicate row(s).")

    # 5. Clip invalid numeric ranges
    if "data_used_gb" in df.columns:
        df["data_used_gb"] = df["data_used_gb"].clip(
            lower=0,
            upper=100
        )

    if "revenue_inr" in df.columns:
        df["revenue_inr"] = df["revenue_inr"].clip(lower=0)

    return df


def etl_job():
    """Extract, transform, and load the telecom dataset."""

    try:
        log("Starting ETL...")

        if not os.path.exists(RAW_PATH):
            log(f"Raw file not found: {RAW_PATH}")
            return

        # EXTRACT
        df = pd.read_csv(RAW_PATH)
        log(f"Extracted {len(df)} row(s) from {RAW_PATH}.")

        # TRANSFORM
        df = clean_frame(df)

        # LOAD: write temporary file, then replace final output
        df.to_csv(TMP_PATH, index=False)
        os.replace(TMP_PATH, OUT_PATH)

        log(f"ETL completed successfully. Rows written: {len(df)}.")

    except Exception as e:
        log(f"ETL failed: {e}")


# Classroom demo: run the ETL job three times, 20 seconds apart
schedule.clear()

completed_runs = 0
maximum_runs = 3


def scheduled_etl_job():
    global completed_runs

    etl_job()
    completed_runs += 1


schedule.every(20).seconds.do(scheduled_etl_job)

log("Scheduler started. ETL is scheduled every 20 seconds.")

while completed_runs < maximum_runs:
    schedule.run_pending()
    time.sleep(0.5)

schedule.clear()
log(f"Scheduler stopped after {completed_runs} ETL execution(s).")

print("Done. Scheduler exited after", completed_runs, "ETL executions.")