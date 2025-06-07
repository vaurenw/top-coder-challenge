import json
from run import calculate_reimbursement

def load_cases(filename="public_cases.json"):
    with open(filename) as f:
        return json.load(f)

def main():
    print("🧾 Black Box Challenge - Reimbursement System Evaluation")
    print("=======================================================\n")

    try:
        cases = load_cases()
    except FileNotFoundError:
        print("❌ Error: public_cases.json not found!")
        return

    num_cases = len(cases)
    print(f"📊 Running evaluation against {num_cases} test cases...\n")

    results = []
    errors = []
    successful_runs = 0
    exact_matches = 0
    close_matches = 0
    total_error = 0
    max_error = 0
    worst_case = None

    for i, case in enumerate(cases):
        if i % 100 == 0:
            print(f"Progress: {i}/{num_cases} cases processed...")

        d = case["input"]["trip_duration_days"]
        m = case["input"]["miles_traveled"]
        r = case["input"]["total_receipts_amount"]
        expected = case["expected_output"]

        try:
            output = calculate_reimbursement(d, m, r)
            if not isinstance(output, (float, int)):
                raise ValueError("Invalid output format")

            error = abs(output - expected)
            successful_runs += 1
            total_error += error

            results.append({
                "case_num": i + 1,
                "expected": expected,
                "actual": output,
                "error": error,
                "trip_days": d,
                "miles": m,
                "receipts": r
            })

            if error < 0.01:
                exact_matches += 1
            if error < 1.0:
                close_matches += 1
            if error > max_error:
                max_error = error
                worst_case = results[-1]

        except Exception as e:
            errors.append(f"Case {i+1}: Error - {str(e)}")

    if successful_runs == 0:
        print("❌ No successful test cases!")
        print("Your script may have failed, produced invalid output, or timed out.")
        return

    avg_error = total_error / successful_runs
    exact_pct = round((exact_matches / successful_runs) * 100, 1)
    close_pct = round((close_matches / successful_runs) * 100, 1)
    score = round(avg_error * 100 + (num_cases - exact_matches) * 0.1, 2)

    print("\n✅ Evaluation Complete!\n")
    print("📈 Results Summary:")
    print(f"  Total test cases: {num_cases}")
    print(f"  Successful runs: {successful_runs}")
    print(f"  Exact matches (±$0.01): {exact_matches} ({exact_pct}%)")
    print(f"  Close matches (±$1.00): {close_matches} ({close_pct}%)")
    print(f"  Average error: ${avg_error:.2f}")
    print(f"  Maximum error: ${max_error:.2f}")
    print(f"\n🎯 Your Score: {score} (lower is better)\n")

    if exact_matches == num_cases:
        print("🏆 PERFECT SCORE! You have reverse-engineered the system completely!")
    elif exact_matches > 950:
        print("🥇 Excellent! You are very close to the perfect solution.")
    elif exact_matches > 800:
        print("🥈 Great work! You have captured most of the system behavior.")
    elif exact_matches > 500:
        print("🥉 Good progress! You understand some key patterns.")
    else:
        print("📚 Keep analyzing the patterns in the interviews and test cases.")

    # Top 5 highest-error cases
    if exact_matches < num_cases:
        print("\n💡 Tips for improvement:")
        print("  Check these high-error cases:")
        top_errors = sorted(results, key=lambda x: -x["error"])[:5]
        for res in top_errors:
            print(f"    Case {res['case_num']}: {res['trip_days']} days, {res['miles']} miles, ${res['receipts']} receipts")
            print(f"      Expected: ${res['expected']:.2f}, Got: ${res['actual']:.2f}, Error: ${res['error']:.2f}")

    # Show errors if any
    if errors:
        print("\n⚠️  Errors encountered:")
        for msg in errors[:10]:
            print(f"  {msg}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more errors")

    print("\n📝 Next steps:")
    print("  1. Fix any script errors shown above")
    print("  2. Ensure your run.py outputs only a number")
    print("  3. Analyze the patterns in the interviews and public cases")
    print("  4. Test edge cases around trip length and receipt amounts")
    print("  5. Submit your solution via the Google Form when ready!")

if __name__ == "__main__":
    main()
