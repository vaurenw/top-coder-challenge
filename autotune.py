import json
import itertools
from run import calculate_reimbursement
import copy

def load_public_cases():
    with open("public_cases.json") as f:
        return json.load(f)

def evaluate_case(trip_days, miles, receipts, expected):
    actual = calculate_reimbursement(trip_days, miles, receipts)
    return abs(actual - expected)

def main():
    cases = load_public_cases()
    
    # We'll modify these parameters in our tuning
    base_params = {
        'per_diem': 100,
        'bonus_5day': 50,
        'mileage_rate_under': 0.58,
        'mileage_rate_over': 0.10,
        'receipt_low_mult': 0.25,
        'receipt_mid_mult': 0.85,
        'receipt_mid_bonus': 25,
        'receipt_high_mult': 0.12,
        'receipt_default_mult': 0.65,
        'receipt_cap': 700,
        'efficiency_bonus': 45,
        'efficiency_low': 175,
        'efficiency_high': 225,
        'rounding_bonus': 0.03
    }
    
    best_error = float('inf')
    best_params = base_params
    
    # Test different parameter combinations
    for per_diem in [95, 100, 105]:
        for bonus in [40, 50, 60]:
            current_params = copy.deepcopy(base_params)
            current_params['per_diem'] = per_diem
            current_params['bonus_5day'] = bonus
            
            total_error = 0
            for case in cases[:100]:  # Test on subset for speed
                error = evaluate_case(
                    case["input"]["trip_duration_days"],
                    case["input"]["miles_traveled"],
                    case["input"]["total_receipts_amount"],
                    case["expected_output"]
                )
                total_error += error
            
            if total_error < best_error:
                best_error = total_error
                best_params = current_params
                print(f"New best error: {best_error:.2f}")
                print(f"Params: per_diem={per_diem}, bonus={bonus}")

    print("\n🏆 Best params found:")
    print(best_params)
    print(f"Total error: {best_error:.2f}")

if __name__ == "__main__":
    main()