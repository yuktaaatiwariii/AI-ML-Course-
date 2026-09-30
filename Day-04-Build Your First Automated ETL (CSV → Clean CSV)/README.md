# Exercise 4: Build Your First Automated ETL (CSV → Clean CSV)

## 1. Objective

The objective of this exercise was to build a basic automated ETL pipeline using Python and pandas to clean telecom usage data and save the cleaned records into a new CSV file.

ETL stands for:

**Extract → Transform → Load**

The pipeline performs the following tasks:

1. **Extract:** Read raw telecom data from `telecom_raw.csv`.
2. **Transform:** Clean missing values, standardize region names, parse dates, remove duplicate records, and handle invalid numeric ranges.
3. **Load:** Save the cleaned data to `output/telecom_cleaned.csv`.
4. **Schedule:** Run the ETL job automatically at a configured interval.
5. **Log:** Record the pipeline's activity, including successful runs and errors.

## 2. Tools and Libraries

* Python
* Jupyter Notebook
* pandas — data loading, cleaning, and transformation
* schedule — periodic execution of the ETL job
* os — directory and file operations
* datetime — timestamps for log entries
* time — pause between scheduler checks

Install the required packages:

```bash
pip install pandas schedule
```

## 3. Input Dataset

The raw dataset contains five sample telecom customer records.

| Column         | Description                           |
| -------------- | ------------------------------------- |
| `customer_id`  | Unique identifier for a customer      |
| `data_used_gb` | Mobile data consumed in gigabytes     |
| `calls_made`   | Number of calls made                  |
| `revenue_inr`  | Revenue generated in Indian rupees    |
| `region`       | Customer's region                     |
| `date`         | Date associated with the usage record |

The sample data intentionally contains missing numeric values, inconsistent region capitalization, and dates written in different formats. These issues are used to demonstrate data cleaning.

## 4. ETL Pipeline Workflow

```text
telecom_raw.csv
      |
      v
   EXTRACT
 Read CSV using pandas
      |
      v
  TRANSFORM
 - Normalize region text
 - Convert numeric columns
 - Fill missing numeric values
 - Parse and standardize dates
 - Remove duplicate customer/date rows
 - Clip invalid numeric ranges
      |
      v
    LOAD
 Write cleaned CSV using a temporary file
      |
      v
output/telecom_cleaned.csv
      |
      v
 Record activity in output/etl_run.log
```

## 5. Transformation Steps

### A. Standardize region names

Region values may have inconsistent capitalization, such as `delhi`, `DELHI`, and `Delhi`.

The pipeline removes surrounding whitespace and applies title case so these values are represented consistently.

### B. Convert and fill missing numeric values

The pipeline checks the numeric columns:

* `data_used_gb`
* `calls_made`
* `revenue_inr`

If a column contains non-numeric values, they are converted to numeric values where possible. Invalid values become missing values.

Missing values are filled using the median of the respective column.

The median is used because it is less affected by unusually high or low values than the mean.

### C. Parse and standardize dates

The raw data contains dates in different formats, such as:

* `2025/09/25`
* `2025-09-25`
* `25-09-2025`

The pipeline converts date values into pandas datetime values. Invalid or unrecognized dates are coerced to `NaT` and replaced with the exercise's configured default date, `2025-09-25`.

The date is then written to the output CSV in a standardized date representation.

**Data-quality note:** Replacing an invalid date with a default date preserves the row, but it does not recover the original date. In a production pipeline, invalid dates should generally be flagged for review or corrected using a trusted source.

### D. Remove duplicate records

The pipeline checks for duplicate records using the combination of:

* `customer_id`
* `date`

If multiple rows have the same customer ID and date, the first row is retained.

The number of removed duplicate rows is written to the ETL log.

### E. Clip invalid numeric ranges

The pipeline applies basic range checks:

* `data_used_gb` is limited to the range 0–100 GB.
* `revenue_inr` is prevented from going below zero.

These checks act as a simple safety net for clearly invalid values. They are not a substitute for validating values against the telecom provider's actual business rules.

## 6. Loading and File Safety

The cleaned DataFrame is first written to a temporary file:

`output/telecom_cleaned.tmp.csv`

After the temporary file is written, `os.replace()` moves it to:

`output/telecom_cleaned.csv`

This helps avoid exposing a partially written output file if the process is interrupted during writing.

## 7. Scheduling

The Python `schedule` library is used to execute the ETL job at a configured interval.

For the classroom demonstration, the job is scheduled to run every 20 seconds and stop after three executions.

The interval can be changed for other use cases. For example, the job can be configured to run daily or hourly.

**Important:** The number of scheduler checks is not the same as the number of ETL executions. The demonstration script tracks completed job executions so it stops after the intended number of runs.

## 8. Logging and Error Handling

Each ETL run writes timestamped messages to the console and to:

`output/etl_run.log`

The log can record:

* ETL job start
* Missing raw input file
* Number of duplicate rows removed
* Successful completion and number of rows written
* Errors encountered during processing

Logging makes it easier to monitor the pipeline and investigate problems.

## 9. Output Files

| File                             | Purpose                                                                                   |
| -------------------------------- | ----------------------------------------------------------------------------------------- |
| `telecom_raw.csv`                | Original input data                                                                       |
| `output/telecom_cleaned.csv`     | Cleaned output generated by the ETL pipeline                                              |
| `output/etl_run.log`             | Timestamped execution log                                                                 |
| `output/telecom_cleaned.tmp.csv` | Temporary file used during safe output writing; normally renamed after a successful write |

## 10. Verification Checklist

After running the script, verify that:

* [ ] The raw CSV is read successfully.
* [ ] Region names have consistent capitalization.
* [ ] Missing numeric values are filled where a median is available.
* [ ] Dates are parsed and written in a consistent format.
* [ ] Duplicate `(customer_id, date)` records are removed.
* [ ] Data usage is constrained to the configured range.
* [ ] Negative revenue values are clipped to zero.
* [ ] The cleaned CSV is created in the `output` folder.
* [ ] The log file contains timestamps and execution messages.
* [ ] The scheduler stops after the configured number of runs.

## 11. Key Learnings

Through this exercise, I learned how to:

* Build a basic ETL workflow using Python and pandas.
* Separate extraction, transformation, and loading into clear stages.
* Clean missing and inconsistent data programmatically.
* Standardize text and date values.
* Remove duplicates using selected columns.
* Save processed data to a CSV file.
* Use a scheduler to automate repeated execution.
* Maintain a log file for monitoring and troubleshooting.
* Use a temporary output file before replacing the final output.

## 12. Telecom Analytics Application

Telecom datasets are frequently updated with customer usage, call activity, revenue, and regional information. An automated ETL pipeline can prepare these records before they are used for reporting, dashboards, customer segmentation, churn analysis, or revenue analytics.

Automating the cleaning process reduces repetitive manual work and helps ensure that downstream analysis uses consistently formatted data.

## 13. Conclusion

This exercise demonstrated a beginner-friendly automated ETL pipeline that extracts telecom data from a CSV file, applies data-cleaning transformations, loads the cleaned records into a new CSV file, and records execution details in a log.

It provides a foundation for more advanced ETL workflows involving databases, cloud storage, data validation, and scheduled production pipelines.
