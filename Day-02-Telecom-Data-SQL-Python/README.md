# Day 2 — Telecom Data, SQL & Python

**Module:** Telecom Data, SQL, Python & ETL  
**Focus:** Data types, SQL retrieval and Python/Pandas cleaning  
**Status:** Completed

# 1. Day 2 objective

Day 2 moved from telecom domain theory into practical data work.

The major idea was:

```text
Different data sources
        ↓
Different data structures
        ↓
Different processing methods
        ↓
One analytical dataset
```

The day introduced structured, semi-structured and unstructured telecom data, followed by SQL and Pandas exercises.

---

# 2. Types of telecom data

## 2.1 Structured data

Data organised into rows and columns with a defined schema.

Examples:

- CRM subscriber master
- Billing invoices
- Provisioning records
- Plan catalogues
- CSV tables

Typical tools:

- Relational databases
- SQL
- Excel
- CSV

Example:

| customer_id | plan | revenue |
|---|---|---:|
| 1001 | 5G | 599 |
| 1002 | 4G | 399 |

---

# 2.2 Semi-structured data

Data does not necessarily follow a fixed table structure but contains some organisation or self-describing structure.

Examples:

- JSON
- XML
- CDR/xDR feeds
- Network element messages
- API payloads
- Alarm streams

Example JSON:

```json
{
  "customer_id": 1001,
  "session": {
    "duration": 120,
    "data_used": 1.5
  }
}
```

This generally needs parsing/transformation before traditional tabular analysis.

---

# 2.3 Unstructured data

Data without a fixed schema.

Examples:

- Call-centre transcripts
- Free-form complaints
- Engineer notes
- Network diagrams
- Images/audio/video

Typical approaches include:

- Object storage
- NLP
- LLM-based processing

---

# 3. Why the data type matters

The wrong processing method can create inefficiency or errors.

For example:

```text
Structured CSV → SQL/Pandas
JSON → Parse first → tabular representation
Free text → NLP/LLM techniques
```

This is important because telecom organisations do not have a single universal data format.

---

# 4. SQL fundamentals

SQL is used to retrieve and analyse structured data stored in relational databases.

The main operations covered were:

- SELECT
- WHERE
- ORDER BY
- JOIN
- GROUP BY
- Aggregations

---

# 5. SQL Exercise — High-usage customers

The course exercise asks us to identify customers consuming more than 10 GB.

```sql
SELECT customer_id, data_used_in_GB
FROM usage_data
WHERE data_used_in_GB > 10
ORDER BY data_used_in_GB DESC;
```

## Explanation

### SELECT

```sql
SELECT customer_id, data_used_in_GB
```

Selects the columns we want to see.

### FROM

```sql
FROM usage_data
```

Specifies the source table.

### WHERE

```sql
WHERE data_used_in_GB > 10
```

Filters customers whose usage exceeds 10 GB.

### ORDER BY

```sql
ORDER BY data_used_in_GB DESC
```

Sorts the results from highest to lowest usage.

---

# 6. Why this SQL query matters in telecom

A high-usage customer may be relevant for:

- Upgrade campaigns
- Premium plan targeting
- Network capacity planning
- Customer segmentation

So the query is not just a technical exercise.

It converts raw usage data into a potentially useful business insight.

---

# 7. JOIN operations

Telecom data is distributed across systems.

For example:

```text
Customer database
       +
Billing database
       +
Usage database
       +
Complaint database
```

A JOIN allows related records to be combined using a common key.

Typical key:

```text
customer_id
```

Conceptually:

```text
Customer
customer_id
    │
    ├──────────────┐
    ↓              ↓
Usage          Complaints
```

This becomes essential when constructing a master analytical dataset.

---

# 8. GROUP BY and aggregation

GROUP BY allows us to calculate metrics for groups.

Examples:

```sql
AVG()
SUM()
COUNT()
MIN()
MAX()
```

Potential telecom questions:

- Average revenue by region
- Total data usage by plan
- Number of customers per segment
- Average usage by month

---

# 9. Why SQL is still important

Even when Python and BI tools are available, SQL remains important because:

- Data often lives in relational databases.
- Filtering can be performed close to the data source.
- Aggregations can be performed efficiently.
- SQL is widely used in analytical systems.
- It is the standard language for many data warehouses.

---

# 10. Python + Pandas

Pandas is a Python library for data manipulation and analysis.

A Pandas DataFrame can be thought of as a programmable table.

```text
DataFrame
 ├── rows
 ├── columns
 └── index
```

It is useful for:

- Cleaning
- Filtering
- Transformation
- Aggregation
- Merging
- Preparation for ML

---

# 11. Python Exercise — Telecom dataset cleaning

The exercise uses:

```python
import pandas as pd

df = pd.read_csv("telecom_usage.csv")
```

This loads the CSV file into a Pandas DataFrame.

---

## Remove missing values

```python
df.dropna(inplace=True)
```

Removes rows containing missing values.

### Why?

Missing data can cause problems during:

- Analysis
- Visualisation
- Machine learning

However, in real projects, blindly dropping every missing row is not always correct. Sometimes missingness itself contains useful information, or values should be imputed instead.

---

# 12. Remove duplicate records

```python
df.drop_duplicates(inplace=True)
```

Duplicate records can:

- Inflate counts
- Distort averages
- Produce incorrect ML training data

---

# 13. Standardise dates

```python
df['date'] = pd.to_datetime(df['date'])
```

This converts the date column into a proper datetime representation.

This makes operations such as:

```text
Month extraction
Date filtering
Time-series analysis
Sorting
```

much easier.

---

# 14. Preview cleaned data

```python
print(df.head())
```

`head()` displays the first few records.

The exercise also calculates:

```python
print(f"Cleaned dataset: {len(df)} records")
```

This provides the number of records remaining after cleaning.

---

# 15. Basic data-cleaning workflow

The exercise establishes this pattern:

```text
Load
 ↓
Inspect
 ↓
Handle missing values
 ↓
Remove duplicates
 ↓
Standardise data types
 ↓
Inspect cleaned result
```

This is a foundation for later ETL and machine learning.

---

# 16. Professional data-cleaning mindset

Before cleaning a real dataset, ask:

1. What does each column mean?
2. What is the grain?
3. Which values are actually missing?
4. Which duplicates are genuine duplicates?
5. Which data types are correct?
6. What should happen to invalid records?
7. Can the cleaning process be reproduced?

The objective is not simply to make a dataset smaller.

The objective is to make it **reliable and analysis-ready**.

---

# 17. Day 2 takeaways

- Telecom data can be structured, semi-structured or unstructured.
- Different data types require different processing techniques.
- SQL is essential for structured data retrieval.
- WHERE filters records.
- ORDER BY sorts records.
- JOIN combines related datasets.
- GROUP BY supports grouped analysis.
- Pandas provides a programmable environment for data cleaning.
- Missing values and duplicates can distort analysis.
- Correct data types are important.
- SQL and Python complement each other.

## One-line summary

**Day 2 taught me how to identify telecom data structures and use SQL and Python/Pandas to retrieve and clean data before further analytics.**
