import json
from datetime import datetime

def validate_record(row, config):
    """Validates a single record against schema and business rules."""
    errors = []
    
    # Check primary keys / required fields
    for pk in config["primary_keys"]:
        if not row.get(pk) or str(row.get(pk)).strip() == "" or str(row.get(pk)) == "nan":
            errors.append(f"Missing mandatory primary key: {pk}")
            
    # Check amount / business rules
    try:
        amount = float(row.get("amount", 0))
        if amount < config["business_rules"]["min_amount"]:
            errors.append(f"Amount {amount} is below minimum allowed value.")
    except (ValueError, TypeError):
        errors.append("Invalid or missing numeric format for amount.")
        
    # Check status validity
    status = str(row.get("status", "")).strip()
    if status not in config["business_rules"]["allowed_statuses"]:
        errors.append(f"Invalid status value: '{status}'")
        
    return errors