import os
import json
import uuid
from datetime import datetime
import pandas as pd
from src.validator import validate_record

class ConfigDrivenLoader:
    def __init__(self, config_path):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
            
    def run_pipeline(self):
        run_id = f"run_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
        start_time = datetime.utcnow().isoformat()
        
        source_path = self.config["source_path"]
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"Source file not found at {source_path}")
            
        print(f"[{run_id}] Starting pipeline execution for dataset: {self.config['dataset_name']}")
        
        # Read input source
        df = pd.read_csv(source_path)
        input_count = len(df)
        
        valid_rows = []
        rejected_rows = []
        
        # Iterate and validate row-by-row
        for _, row in df.iterrows():
            row_dict = row.to_dict()
            errors = validate_record(row_dict, self.config)
            
            if errors:
                row_dict["run_id"] = run_id
                row_dict["rejection_reason"] = "; ".join(errors)
                rejected_rows.append(row_dict)
            else:
                row_dict["run_id"] = run_id
                row_dict["processed_at"] = start_time
                valid_rows.append(row_dict)
                
        valid_df = pd.DataFrame(valid_rows)
        
        # Handle Duplicates / Idempotency based on primary keys
        if not valid_df.empty:
            pkeys = self.config["primary_keys"]
            # Keep the latest record if duplicates exist
            initial_valid_count = len(valid_df)
            valid_df = valid_df.drop_duplicates(subset=pkeys, keep="last")
            duplicates_dropped = initial_valid_count - len(valid_df)
        else:
            duplicates_dropped = 0
            
        # Target Publishing (Idempotent Upsert pattern)
        target_path = self.config["target_path"]
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        
        if os.path.exists(target_path) and not valid_df.empty:
            existing_df = pd.read_parquet(target_path)
            # Combine existing and new data, dropping older duplicates
            combined_df = pd.concat([existing_df, valid_df]).drop_duplicates(subset=pkeys, keep="last")
            combined_df.to_parquet(target_path, index=False)
            output_count = len(combined_df)
        elif not valid_df.empty:
            valid_df.to_parquet(target_path, index=False)
            output_count = len(valid_df)
        else:
            output_count = 0
            
        # Write Rejects to Quarantine
        reject_path = self.config["reject_path"]
        os.makedirs(os.path.dirname(reject_path), exist_ok=True)
        with open(reject_path, "a", encoding="utf-8") as f:
            for rej in rejected_rows:
                f.write(json.dumps(rej) + "\n")
                
        end_time = datetime.utcnow().isoformat()
        
        # Log Operational Metrics
        audit_log = {
            "run_id": run_id,
            "dataset": self.config["dataset_name"],
            "start_time": start_time,
            "end_time": end_time,
            "input_rows": input_count,
            "valid_rows_processed": len(valid_rows),
            "duplicates_removed": duplicates_dropped,
            "rejected_rows": len(rejected_rows),
            "final_target_rows": output_count,
            "status": "SUCCESS"
        }
        
        audit_path = self.config["audit_log_path"]
        os.makedirs(os.path.dirname(audit_path), exist_ok=True)
        with open(audit_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(audit_log) + "\n")
            
        print(f"[{run_id}] Pipeline completed successfully. Metrics: {json.dumps(audit_log, indent=2)}")
        return audit_log

if __name__ == "__main__":
    loader = ConfigDrivenLoader("config/pipeline_config.json")
    loader.run_pipeline()