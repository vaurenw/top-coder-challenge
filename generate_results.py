import json
from run import calculate_reimbursement

def load_private_cases():
    with open("private_cases.json") as f:
        return json.load(f)

def main():
    cases = load_private_cases()
    results = []

    print(f"🧾 Generating results for {len(cases)} cases...")

    for i, case in enumerate(cases):
        trip_days = case["trip_duration_days"]
        miles = case["miles_traveled"]
        receipts = case["total_receipts_amount"]

        try:
            result = calculate_reimbursement(trip_days, miles, receipts)
            results.append(f"{result:.2f}")
        except Exception:
            results.append("ERROR")
            print(f"❌ Error on case {i+1}")

        if (i + 1) % 100 == 0:
            print(f"Processed {i+1} cases...")

    with open("private_results.txt", "w") as f:
        for r in results:
            f.write(r + "\n")

    print("✅ Results saved to private_results.txt")

if __name__ == "__main__":
    main()
