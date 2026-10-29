# Configuration-Driven Data Ingestion & Processing Pipeline

A robust, metadata-driven data engineering pipeline built in Python for scalable ingestion, schema validation, quarantine handling, idempotency, and operational observability.

---

## 1. Project Overview

This project implements a flexible data loader where dataset parameters—including source paths, input formats, column schemas, primary keys, and business validation rules—are declared in external metadata configuration files rather than hard-coded into application logic.

### Key Features
* **Configuration-Driven Architecture:** Decouples pipeline execution from dataset specifications using JSON metadata.
* **Schema & Business Validation:** Enforces missing field checks, type validation, numeric boundaries, and explicit value sets.
* **Explicit Quarantine Path:** Routes malformed or invalid records to a designated JSON Lines (`.jsonl`) quarantine store with granular failure descriptions.
* **Idempotency & Deduplication:** Ensures rerunning the pipeline on the same dataset updates existing records without introducing unintended duplicates.
* **Columnar Target Publishing:** Exports validated records to Apache Parquet format for optimal analytical performance.
* **Operational Observability:** Logs run metrics, execution timestamps, processing status, and row-level reconciliation counts to an audit log.

---

## 2. Directory Structure

```text
yottaflex-config-loader/
│
├── config/
│   └── pipeline_config.json       # Metadata declarations (schema, keys, rules)
│
├── data/
│   ├── sample_input.csv           # Small starter dataset with boundary cases
│   └── large_generator.py         # Scalable dataset generator (100,000+ records)
│
├── output/                        # Auto-generated execution outputs
│   ├── cleaned_target.parquet     # Analytical target dataset
│   ├── rejects.jsonl              # Quarantined invalid records
│   └── run_audit.log              # Operational metrics log
│
├── src/
│   ├── __init__.py
│   ├── loader.py                  # Core pipeline orchestration engine
│   └── validator.py               # Validation rules engine
│
├── tests/
│   ├── __init__.py
│   └── test_pipeline.py           # Automated unit and integration tests
│
├── prompt_history.md              # AI prompt log and disclosure
├── requirements.txt               # Dependencies
└── README.md                      # Project documentation
```

## 3. Setup & Execution Instructions (Windows Command Prompt)

Follow these steps from your Visual Studio Code cmd terminal to set up, populate, and execute the pipeline:

Step 1: Create and Activate Virtual Environment

python -m venv venv
venv\Scripts\activate.bat

Step 2: Install Project Dependencies

pip install -r requirements.txt

Step 3: Generate Scalable Dataset

Generate 100,000 synthetic records with deterministic random seed (42):

python data\large_generator.py

Step 4: Run Core Pipeline Engine

Execute the configuration-driven loader:

python -m src.loader

Step 5: Run Automated Unit Tests

Verify pipeline behavior across edge cases and negative scenarios:

python -m pytest

## 4. Configuration Metadata Reference (config/pipeline_config.json)

JSON
{
  "dataset_name": "ecommerce_orders",
  "source_path": "data/sample_input.csv",
  "target_path": "output/cleaned_target.parquet",
  "reject_path": "output/rejects.jsonl",
  "audit_log_path": "output/run_audit.log",
  "file_format": "csv",
  "primary_keys": ["order_id"],
  "schema": {
    "order_id": "string",
    "customer_id": "string",
    "order_date": "string",
    "amount": "float",
    "status": "string"
  },
  "business_rules": {
    "min_amount": 0.0,
    "allowed_statuses": ["PENDING", "COMPLETED", "CANCELLED", "REFUNDED"]
  }
}

## 5. Design Choices & Trade-Offs

* Metadata Configuration over Code Hardcoding: Declaring dataset paths, rules, and primary keys inside JSON metadata isolates processing logic from data definitions. This allows the same execution engine to process distinct datasets simply by switching configuration profiles.

* Apache Parquet for Target Storage: Choosing Parquet over flat CSV for target storage preserves data types, provides efficient columnar compression, and optimizes analytical query throughput.

* Fault-Tolerant Quarantine Mechanism: Diverting invalid rows to a dedicated .jsonl quarantine log with failure tags prevents full-pipeline failure caused by isolated row errors while keeping anomalous data fully audit-traceable.

* In-Memory Upsert Deduplication: Primary key deduplication uses in-memory Pandas dataframes (keep="last") combined with existing target Parquet data to achieve idempotent loads.

## 6. Known Limitations & Future Improvements

* RAM Constraints on Large In-Memory Batches: The current Pandas-based loader reads datasets into system RAM. For multi-gigabyte or streaming data volumes, migrating the processing layer to PySpark or DuckDB would prevent memory exhaustion.

* Local Storage Target: Storage operations currently execute on local disk paths. For cloud deployment, paths can be mapped directly to AWS S3, Azure Blob Storage, or Google Cloud Storage.

* Schema Evolution: Unannounced schema changes (such as missing or renamed columns) will trigger validation rejection. Implementing explicit schema evolution rules (e.g., auto-filling missing optional fields with defaults) would enhance flexibility.

## 7. Submission Checklist & Git Verification

Verify All Tests Pass: 

python -m pytest

Push to Public GitHub Repository:  

git init
git add .
git commit -m "feat: complete configuration-driven data pipeline implementation"
git branch -M main
git remote add origin [https://github.com/MeharKishoreNarava/yottaflex-config-loader.git](https://github.com/MeharKishoreNarava/yottaflex-config-loader.git)
git push -u origin main