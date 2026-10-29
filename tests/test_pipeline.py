import os
import json
import pytest
import pandas as pd
from src.validator import validate_record
from src.loader import ConfigDrivenLoader

@pytest.fixture
def sample_config(tmp_path):
    config = {
        "dataset_name": "test_dataset",
        "source_path": str(tmp_path / "input.csv"),
        "target_path": str(tmp_path / "target.parquet"),
        "reject_path": str(tmp_path / "rejects.jsonl"),
        "audit_log_path": str(tmp_path / "audit.log"),
        "file_format": "csv",
        "primary_keys": ["order_id"],
        "schema": {"order_id": "string", "amount": "float", "status": "string"},
        "business_rules": {
            "min_amount": 0.0,
            "allowed_statuses": ["COMPLETED", "PENDING"]
        }
    }
    return config

def test_validator_happy_path(sample_config):
    row = {"order_id": "1", "amount": 50.0, "status": "COMPLETED"}
    errors = validate_record(row, sample_config)
    assert len(errors) == 0

def test_validator_missing_primary_key(sample_config):
    row = {"order_id": "", "amount": 50.0, "status": "COMPLETED"}
    errors = validate_record(row, sample_config)
    assert len(errors) > 0

def test_validator_business_rule_failure(sample_config):
    row = {"order_id": "2", "amount": -10.0, "status": "COMPLETED"}
    errors = validate_record(row, sample_config)
    assert any("Amount" in err for err in errors)

def test_pipeline_execution(tmp_path, sample_config):
    # Create mock input CSV
    input_file = sample_config["source_path"]
    df = pd.DataFrame([
        {"order_id": "A1", "customer_id": "C1", "order_date": "2026-10-01", "amount": 100.0, "status": "COMPLETED"},
        {"order_id": "A2", "customer_id": "C2", "order_date": "2026-10-01", "amount": -5.0, "status": "PENDING"}, # Invalid amount
        {"order_id": "A1", "customer_id": "C1", "order_date": "2026-10-01", "amount": 100.0, "status": "COMPLETED"}  # Duplicate
    ])
    df.to_csv(input_file, index=False)
    
    # Save config
    config_file = tmp_path / "pipeline_config.json"
    with open(config_file, "w") as f:
        json.dump(sample_config, f)
        
    loader = ConfigDrivenLoader(str(config_file))
    metrics = loader.run_pipeline()
    
    assert metrics["input_rows"] == 3
    assert metrics["rejected_rows"] == 1
    assert metrics["duplicates_removed"] == 1
    assert metrics["final_target_rows"] == 1