import json
from run import calculate_reimbursement

def load_public_cases():
    with open("public_cases.json") as f:
        return json.load(f)

def score(params, cases):
    exact = 0
    total_error = 0
    for case in cases:
        trip_days = case["input"]["trip_duration_days"]
        miles = case["input"]["miles_traveled"]
        receipts = case["input"]["total_receipts_amount"]
        expected = case["expected_output"]
        actual = calculate_reimbursement(trip_days, miles, receipts, **params)
        error = abs(actual - expected)
        total_error += error
        if error < 0.01:
            exact += 1
    return exact, total_error

def main():
    cases = load_public_cases()

    best_score = -1
    best_params = None

    for per_diem_rate in [70, 75, 80]:
     for rate_under_150 in [0.3, 0.35, 0.4]:
        for rate_above_150 in [0.05, 0.1, 0.15]:
            for bonus_5day in [30, 40, 50]:
                params = {
                    "per_diem_rate": per_diem_rate,
                    "rate_under_150": rate_under_150,
                    "rate_above_150": rate_above_150,
                    "bonus_5day": bonus_5day,
                }


    print("\n🏆 Best params:")
    print(best_params[0])
    print(f"Exact matches: {best_score}, Total error: {best_params[1]:.2f}")

if __name__ == "__main__":
    main()
