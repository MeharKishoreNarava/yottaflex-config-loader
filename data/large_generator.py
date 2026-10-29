import csv
import random

def generate_large_dataset(num_records=100000, output_path="data/large_input.csv"):
    random.seed(42)
    statuses = ["PENDING", "COMPLETED", "CANCELLED", "REFUNDED", "UNKNOWN_STATUS"]
    
    print(f"Generating {num_records} synthetic records...")
    with open(output_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["order_id", "customer_id", "order_date", "amount", "status"])
        
        for i in range(1, num_records + 1):
            order_id = f"ORD-{i:06d}"
            # Introduce missing customer ID for 1% of records
            customer_id = f"CUST-{random.randint(1, 5000):04d}" if random.random() > 0.01 else ""
            order_date = f"2026-10-{random.randint(1, 28):02d}"
            
            # Introduce negative or extreme amounts for testing business rules
            r = random.random()
            if r < 0.02:
                amount = -50.0  # Invalid negative amount
            elif r < 0.05:
                amount = None   # Missing amount
            else:
                amount = round(random.uniform(10.0, 5000.0), 2)
                
            status = random.choice(statuses)
            
            # Introduce duplicate keys for 2% of records
            if r > 0.98 and i > 10:
                order_id = f"ORD-{random.randint(1, 10):06d}"
                
            writer.writerow([order_id, customer_id, order_date, amount, status])
            
    print(f"Dataset successfully generated at {output_path}")

if __name__ == "__main__":
    generate_large_dataset()