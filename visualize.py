import json
import matplotlib.pyplot as plt
from run import calculate_reimbursement

def load_cases():
    with open("public_cases.json") as f:
        return json.load(f)

def main():
    cases = load_cases()
    xs, ys, zs = [], [], []
    errors = []

    for case in cases:
        d = case["input"]["trip_duration_days"]
        m = case["input"]["miles_traveled"]
        r = case["input"]["total_receipts_amount"]
        expected = case["expected_output"]
        actual = calculate_reimbursement(d, m, r)
        error = abs(actual - expected)

        xs.append(d)
        ys.append(m)
        zs.append(r)
        errors.append(error)

    # === Plot 1: Error vs Receipts ===
    plt.figure(figsize=(10, 6))
    plt.scatter(zs, errors, alpha=0.5, color='red')
    plt.xlabel("Receipts ($)")
    plt.ylabel("Absolute Error")
    plt.title("Error vs Receipts Amount")
    plt.grid(True)

    # === Plot 2: Error vs Miles ===
    plt.figure(figsize=(10, 6))
    plt.scatter(ys, errors, alpha=0.5, color='blue')
    plt.xlabel("Miles Traveled")
    plt.ylabel("Absolute Error")
    plt.title("Error vs Miles")
    plt.grid(True)

    # === Plot 3: Error vs Trip Duration ===
    plt.figure(figsize=(10, 6))
    plt.scatter(xs, errors, alpha=0.5, color='green')
    plt.xlabel("Trip Duration (Days)")
    plt.ylabel("Absolute Error")
    plt.title("Error vs Trip Duration")
    plt.grid(True)

    # Show all
    plt.show()

if __name__ == "__main__":
    main()
