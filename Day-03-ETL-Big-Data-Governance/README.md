# Day 3 — ETL, Big Data Processing, Data Warehouses & Governance

**Module:** Telecom Data, SQL, Python & ETL  
**Focus:** ETL pipelines, scalable processing, data architecture, privacy and governance  
**Status:** Completed

# 1. Day 3 objective

Day 3 moved from individual data-cleaning operations toward **repeatable data pipelines and production-oriented thinking**.

The central idea:

```text
Multiple raw sources
        ↓
Extract
        ↓
Transform
        ↓
Load
        ↓
Governed analytical dataset
```

The day also introduced how telecom organisations handle data at scale and how sensitive customer data must be protected.

---

# 2. ETL

ETL means:

**Extract → Transform → Load**

## Extract

Collect raw data from different sources.

Possible sources:

- SQL databases
- CSV files
- JSON logs
- APIs
- Network monitoring systems
- Billing systems
- Customer-service systems

## Transform

Make the data analysis-ready.

Typical operations:

- Remove duplicates
- Handle missing values
- Convert data types
- Standardise formats
- Calculate derived metrics
- Join datasets
- Validate data

## Load

Store the transformed dataset in a destination such as:

- Data warehouse
- Database
- CSV
- Analytical storage

---

# 3. ETL Exercise — Customer complaint integration

The course scenario combines customer information from a SQL database with complaints stored in a CSV file.

```python
import pandas as pd
from sqlalchemy import create_engine

connection = create_engine('sqlite:///telecom.db')

customers = pd.read_sql(
    'SELECT * FROM customers',
    connection
)

complaints = pd.read_csv('complaints.csv')
```

This is the **Extract** stage.

---

## Transform

Remove records without customer IDs:

```python
customers.dropna(
    subset=['customer_id'],
    inplace=True
)

complaints.dropna(
    subset=['customer_id'],
    inplace=True
)
```

Then merge the datasets:

```python
merged = customers.merge(
    complaints,
    on='customer_id',
    how='left'
)
```

The common key is:

```text
customer_id
```

---

## Load

Save the resulting dataset:

```python
merged.to_csv(
    'etl_output.csv',
    index=False
)
```

The resulting pipeline is:

```text
SQLite customers
      +
complaints.csv
      ↓
   Extract
      ↓
    Clean
      ↓
    Merge
      ↓
    Load
      ↓
etl_output.csv
```

---

# 4. Why ETL matters in telecom

A telecom operator has many independent systems.

For example:

```text
CRM
 ↓
Customer information

Network
 ↓
Usage information

Billing
 ↓
Revenue/payment information

Support
 ↓
Complaint information
```

Analytics becomes much more useful when these are connected.

For example:

```text
Customer
   +
Usage
   +
Billing
   +
Complaints
   ↓
Master analytical dataset
   ↓
Churn analysis
```

---

# 5. Automated ETL

Manual scripts do not scale well.

The course introduced automation tools such as:

- Apache Airflow
- Apache NiFi
- KNIME
- Python scheduling

Automation provides:

### Consistency

The same steps run repeatedly.

### Accuracy

Validation can happen automatically.

### Scalability

Growing data volumes can be processed systematically.

### Time savings

Analysts spend less time repeating data preparation.

---

# 6. Automated ETL exercise

A simple scheduler was demonstrated using Python.

```python
import pandas as pd
import schedule
import time

def etl_job():

    print("Starting ETL...")

    df = pd.read_csv("telecom_raw.csv")

    df.dropna(inplace=True)

    df['date'] = pd.to_datetime(df['date'])

    df.to_csv(
        "telecom_cleaned.csv",
        index=False
    )

    print("ETL completed successfully.")

schedule.every(10).seconds.do(etl_job)

while True:
    schedule.run_pending()
    time.sleep(1)
```

This simulates an automatically repeating ETL process.

In production, orchestration systems such as Airflow can provide:

- Dependencies
- Scheduling
- Failure handling
- Logging
- Alerts
- Workflow management

---

# 7. Data Warehouse

A data warehouse stores structured and organised data designed primarily for analytics.

Characteristics:

- Structured tables
- Defined schema
- Fast analytical queries
- Reporting/BI oriented
- Cleaned and validated data

Examples introduced:

- Google BigQuery
- Snowflake

Typical users:

- Business analysts
- Executives
- BI systems

---

# 8. Data Lake

A data lake stores raw data in many formats.

Possible data:

- CSV
- JSON
- XML
- Images
- Audio
- Video
- Logs

Characteristics:

- Flexible
- Large-scale storage
- Raw data can be retained for future analysis
- Useful for data science and ML

Examples introduced:

- Amazon S3
- Azure Data Lake Storage
- Hadoop HDFS

---

# 9. Data Warehouse vs Data Lake

| Feature | Data Warehouse | Data Lake |
|---|---|---|
| Data | Structured | Any format |
| Schema | Schema-on-write | Schema-on-read |
| Main use | BI/reporting | Data science/raw storage |
| Querying | Usually fast | Depends on processing |
| Storage | More structured/optimised | Lower-cost raw storage |
| Users | Analysts/executives | Data scientists/engineers |
| Examples | BigQuery, Snowflake | S3, ADLS, HDFS |

Modern architectures can use both:

```text
Raw data
   ↓
Data Lake
   ↓
Processing
   ↓
Data Warehouse
   ↓
BI / Analytics
```

---

# 10. Why telecom requires scalable processing

The course introduced an example scale of:

- 50M+ daily CDRs
- Around 500 GB of daily raw usage data
- Around 10K queries/hour at peak

A normal laptop cannot simply load every large dataset into memory.

This creates the need for scalable processing techniques.

---

# 11. Parallel processing

Instead of processing:

```text
10 million records
     ↓
one-by-one
```

data can be divided:

```text
10 million
   ↓
┌──────┬──────┬──────┬──────┐
1M     1M     1M     1M ...
```

and processed simultaneously across multiple compute resources.

---

# 12. Batch vs streaming

## Batch processing

Data is processed periodically in groups.

Example:

```text
Every night
 ↓
Process previous day's billing data
```

## Streaming

Data is processed continuously as it arrives.

Example:

```text
Transaction arrives
 ↓
Immediately analyse
 ↓
Fraud detection
```

### Telecom examples

Batch:

- Daily reports
- Billing refresh

Streaming:

- Real-time fraud detection
- Network monitoring

---

# 13. Memory vs speed trade-off

Loading everything into RAM can be fast, but requires sufficient memory.

For large files:

```text
Read everything
    ↓
High RAM requirement
```

Alternative:

```text
Read small chunks
    ↓
Lower memory usage
    ↓
Process incrementally
```

---

# 14. Big Data processing exercise

The course demonstrates chunked Pandas processing.

```python
import pandas as pd

chunks = pd.read_csv(
    'big_telecom_data.csv',
    chunksize=100000
)

total_usage = 0
heavy_users = 0

for chunk in chunks:

    total_usage += chunk['data_used_gb'].sum()

    heavy_users += (
        chunk['data_used_gb'] > 50
    ).sum()

print(f"Total data usage: {total_usage} GB")
print(f"Heavy users (>50GB): {heavy_users}")
```

Instead of loading the entire dataset:

```text
50 million rows
```

at once, the file is processed:

```text
100,000 rows
        ↓
process
        ↓
100,000 rows
        ↓
process
        ↓
...
```

This keeps memory usage manageable.

---

# 15. Connection to distributed systems

The same basic idea appears in distributed systems.

The course introduced:

### Apache Spark

Distributed big-data processing framework.

### Hadoop

An early major distributed storage/processing ecosystem.

### Dask

Python-oriented parallel computing that extends familiar Pandas-style workflows.

The course uses chunked Pandas because the same underlying idea can be understood on a normal laptop.

---

# 16. Data Governance

Telecom data can contain sensitive information such as:

- Phone numbers
- Locations
- Customer information
- Usage history
- Communication-related information

Therefore, data must be governed carefully.

Data governance includes:

### Policies and standards

Rules defining how data should be used.

### Access control

Users should only access information required for their role.

### Data quality

Data should be:

- Accurate
- Complete
- Consistent

### Audit trails

Records of:

- Who accessed data
- When it was accessed
- What was accessed

### Lifecycle management

Rules governing:

- Retention
- Archiving
- Deletion

---

# 17. Privacy protection techniques

## Role-Based Access Control — RBAC

Different roles receive different levels of access.

Example:

```text
Junior Analyst
      ↓
Anonymised data

Senior Analyst
      ↓
Partially masked data

Authorised compliance role
      ↓
Sensitive identifiable data
```

---

## Encryption

Protect data:

- At rest
- In transit

---

## Anonymisation / masking

Instead of exposing:

```text
Name: Rahul Sharma
Phone: 9876543210
```

a non-essential analytical view might show:

```text
Name: ANONYMIZED
Phone: 987-XXX-XXXX
```

---

## Audit logging

Record data access events so organisations can investigate misuse or breaches.

---

# 18. Role-based access exercise

The course demonstrates a simplified Python version:

```python
import pandas as pd

def get_customer_data(role):

    df = pd.read_csv("customer_data.csv")

    if role == "junior_analyst":

        df['name'] = "ANONYMIZED"
        df['phone'] = "XXXXX"
        df['address'] = "HIDDEN"

    elif role == "senior_analyst":

        df['phone'] = (
            df['phone'].str[:3] +
            "-XXX-XXXX"
        )

    return df
```

The purpose is to demonstrate the concept of **different data views for different roles**.

In production systems, this type of enforcement is normally implemented through proper IAM/database access-control mechanisms rather than relying only on a Python function.

---

# 19. Regulations discussed in the course

The course introduced:

- TRAI-related telecom regulation in India
- GDPR in Europe
- CCPA in California

### Important

Regulatory requirements are jurisdiction-specific and can change. Treat the course slides as an introduction and consult the current official regulation/policy text when using these rules in a real project.

---

# 20. Day 3 overall pipeline

Everything learned today connects:

```text
Multiple Sources
      ↓
     ETL
      ↓
Clean + Transform
      ↓
Integrated Dataset
      ↓
Warehouse / Lake
      ↓
Scalable Processing
      ↓
Governed Data
      ↓
Analytics / ML
```

---

# 21. Day 3 takeaways

- ETL means Extract, Transform and Load.
- ETL combines data from different systems into analysis-ready datasets.
- Automation makes ETL repeatable and scalable.
- Data warehouses are designed for structured analytical workloads.
- Data lakes can store raw data in many formats.
- Telecom data volumes require scalable processing.
- Batch and streaming solve different timing requirements.
- Chunk processing reduces memory requirements.
- Spark, Hadoop and Dask provide scalable processing approaches.
- Telecom data requires strong governance and privacy controls.
- RBAC limits data visibility based on job role.
- Encryption, masking and audit logging help protect sensitive information.

## One-line summary

**Day 3 taught me how raw telecom data can be transformed into a repeatable, scalable and governed analytical pipeline.**
