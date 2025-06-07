import json
from run import calculate_reimbursement

def analyze_patterns():
    """Analyze patterns in the public test cases to understand the system better."""
    
    with open("public_cases.json") as f:
        cases = json.load(f)
    
    print("🔍 Analyzing Legacy System Patterns")
    print("=" * 50)
    
    # Analyze per diem patterns
    print("\n📊 Per Diem Analysis:")
    per_diem_cases = []
    for case in cases[:20]:  # Sample first 20 cases
        d = case["input"]["trip_duration_days"]
        expected = case["expected_output"]
        per_diem_cases.append((d, expected))
        print(f"  {d} days → ${expected:.2f}")
    
    # Analyze 5-day trip bonus
    print("\n🎯 5-Day Trip Bonus Analysis:")
    five_day_cases = [c for c in cases if c["input"]["trip_duration_days"] == 5]
    four_day_cases = [c for c in cases if c["input"]["trip_duration_days"] == 4]
    six_day_cases = [c for c in cases if c["input"]["trip_duration_days"] == 6]
    
    print(f"  5-day trips: {len(five_day_cases)} cases")
    print(f"  4-day trips: {len(four_day_cases)} cases")  
    print(f"  6-day trips: {len(six_day_cases)} cases")
    
    # Sample comparisons
    if five_day_cases and four_day_cases:
        print(f"  Sample 5-day: ${five_day_cases[0]['expected_output']:.2f}")
        print(f"  Sample 4-day: ${four_day_cases[0]['expected_output']:.2f}")
    
    # Analyze mileage patterns
    print("\n🚗 Mileage Analysis:")
    low_mile_cases = [c for c in cases if c["input"]["miles_traveled"] <= 150]
    high_mile_cases = [c for c in cases if c["input"]["miles_traveled"] > 150]
    
    print(f"  Low mileage (≤150): {len(low_mile_cases)} cases")
    print(f"  High mileage (>150): {len(high_mile_cases)} cases")
    
    # Analyze receipt patterns
    print("\n🧾 Receipt Analysis:")
    receipt_ranges = [
        ("Very low (<50)", [c for c in cases if c["input"]["total_receipts_amount"] < 50]),
        ("Low (50-600)", [c for c in cases if 50 <= c["input"]["total_receipts_amount"] < 600]),
        ("Sweet spot (600-800)", [c for c in cases if 600 <= c["input"]["total_receipts_amount"] <= 800]),
        ("High (>800)", [c for c in cases if c["input"]["total_receipts_amount"] > 800])
    ]
    
    for range_name, range_cases in receipt_ranges:
        print(f"  {range_name}: {len(range_cases)} cases")
        if range_cases:
            avg_reimbursement = sum(c["expected_output"] for c in range_cases) / len(range_cases)
            print(f"    Average reimbursement: ${avg_reimbursement:.2f}")
    
    # Analyze efficiency patterns
    print("\n⚡ Efficiency Analysis:")
    efficiency_cases = []
    for case in cases:
        d = case["input"]["trip_duration_days"]
        m = case["input"]["miles_traveled"]
        mpd = m / d if d > 0 else 0
        efficiency_cases.append((mpd, case["expected_output"]))
    
    # Find cases in the "sweet spot"
    sweet_spot_cases = [c for c in cases 
                       if 180 <= (c["input"]["miles_traveled"] / c["input"]["trip_duration_days"]) <= 220]
    print(f"  Cases in efficiency sweet spot (180-220 mpd): {len(sweet_spot_cases)}")

def test_specific_cases():
    """Test specific cases that might reveal patterns."""
    
    print("\n🧪 Testing Specific Patterns")
    print("=" * 30)
    
    # Test the examples from the interviews
    test_cases = [
        # Marcus's examples
        (3, 180, 847, "Marcus Cleveland-Detroit trip 1"),
        (3, 180, 623, "Marcus Cleveland-Detroit trip 2"),
        (8, 300, 1200, "Marcus 8-day Ohio/Indiana swing"),
        
        # Kevin's "sweet spot"
        (5, 900, 500, "Kevin's 5-day optimal trip"),
        (5, 1000, 400, "Another 5-day test"),
        
        # Efficiency tests
        (1, 200, 100, "High efficiency single day"),
        (10, 500, 800, "Low efficiency long trip"),
    ]
    
    for days, miles, receipts, description in test_cases:
        result = calculate_reimbursement(days, miles, receipts)
        mpd = miles / days
        print(f"  {description}:")
        print(f"    Input: {days}d, {miles}mi, ${receipts}")
        print(f"    Miles/day: {mpd:.1f}")
        print(f"    Result: ${result:.2f}")
        print()

def find_worst_errors():
    """Find the cases with the highest errors to debug."""
    
    with open("public_cases.json") as f:
        cases = json.load(f)
    
    print("\n❌ Worst Error Cases")
    print("=" * 20)
    
    errors = []
    for i, case in enumerate(cases):
        d = case["input"]["trip_duration_days"]
        m = case["input"]["miles_traveled"]
        r = case["input"]["total_receipts_amount"]
        expected = case["expected_output"]
        actual = calculate_reimbursement(d, m, r)
        error = abs(actual - expected)
        
        errors.append((error, i, d, m, r, expected, actual))
    
    # Sort by error and show top 10
    errors.sort(reverse=True)
    
    for error, case_num, days, miles, receipts, expected, actual in errors[:10]:
        mpd = miles / days if days > 0 else 0
        print(f"  Case {case_num + 1}: Error ${error:.2f}")
        print(f"    Input: {days}d, {miles}mi, ${receipts:.2f}")
        print(f"    Miles/day: {mpd:.1f}")
        print(f"    Expected: ${expected:.2f}, Got: ${actual:.2f}")
        print()

if __name__ == "__main__":
    analyze_patterns()
    test_specific_cases()
    find_worst_errors()