import sys

def calculate_reimbursement(
    trip_days, miles, receipts,
    per_diem_rate=75,
    bonus_5day=50,
    rate_under_150=0.4,
    rate_above_150=0.1,
    receipt_low_mult=0.25,
    receipt_mid_mult=0.8,
    receipt_mid_bonus=20,
    receipt_high_mult=0.1,
    receipt_default_mult=0.6,
    receipt_cap=650,
    eff_bonus=40,
    eff_low=180,
    eff_high=220,
    per_diem_cap=700
):
    # Per diem logic
    per_diem = min(trip_days * per_diem_rate, per_diem_cap)

    # 5-day trip bonus
    bonus = bonus_5day if trip_days == 5 else 0

    # Mileage calculation
    if miles <= 150:
        mileage = miles * rate_under_150
    else:
        mileage = 150 * rate_under_150 + (miles - 150) * rate_above_150

    # Receipt logic
    if receipts < 50:
        receipt_value = receipts * receipt_low_mult
    elif 600 <= receipts <= 800:
        receipt_value = receipts * receipt_mid_mult + receipt_mid_bonus
    elif receipts > 800:
        receipt_value = 800 * receipt_mid_mult + (receipts - 800) * receipt_high_mult
    else:
        receipt_value = receipts * receipt_default_mult

    receipt_value = min(receipt_value, receipt_cap)

    # Efficiency bonus
    mpd = miles / trip_days
    efficiency = eff_bonus if eff_low <= mpd <= eff_high else 0

    total = per_diem + bonus + mileage + receipt_value + efficiency
    return round(total, 2)




if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python run.py <trip_days> <miles> <receipts>")
        sys.exit(1)

    try:
        days = int(sys.argv[1])
        miles = float(sys.argv[2])
        receipts = float(sys.argv[3])
    except ValueError:
        print("Invalid input.")
        sys.exit(1)

    print(calculate_reimbursement(days, miles, receipts))
