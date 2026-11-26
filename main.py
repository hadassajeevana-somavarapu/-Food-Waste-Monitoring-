# Food Waste Monitoring System
# Compares prepared meals, meals served, and leftovers across multiple days,
# calculates daily and overall wastage percentages, and identifies days exceeding
# the acceptable wastage limit.


def analyze_food_waste(daily_records, max_acceptable_waste_pct=10.0):
    """
    daily_records: list of dicts, each with:
        - 'day': str (e.g., 'Day 1' or 'Monday')
        - 'prepared': int
        - 'served': int
        - 'leftovers': int (unserved/wasted meals)
    max_acceptable_waste_pct: float percentage threshold (e.g., 10.0 for 10%)
    """
    if max_acceptable_waste_pct < 0 or max_acceptable_waste_pct > 100:
        raise ValueError("Acceptable wastage threshold must be between 0 and 100 percent.")

    processed_days = []
    exceeding_days = []

    total_prepared = 0
    total_served = 0
    total_leftovers = 0
    total_unaccounted = 0

    for idx, rec in enumerate(daily_records, start=1):
        day_label = rec["day"].strip().title() if rec.get("day") else f"Day {idx}"
        prepared = int(rec["prepared"])
        served = int(rec["served"])
        leftovers = int(rec["leftovers"])

        if prepared < 0 or served < 0 or leftovers < 0:
            raise ValueError(f"{day_label}: Meal counts cannot be negative.")
        if served > prepared:
            raise ValueError(f"{day_label}: Meals served ({served}) cannot exceed prepared meals ({prepared}).")
        if served + leftovers > prepared:
            raise ValueError(
                f"{day_label}: Served ({served}) + leftovers ({leftovers}) "
                f"cannot exceed prepared meals ({prepared})."
            )

        unaccounted = prepared - (served + leftovers)
        total_wasted_meals = leftovers + unaccounted
        waste_pct = (total_wasted_meals / prepared * 100.0) if prepared > 0 else 0.0
        exceeds_limit = waste_pct > max_acceptable_waste_pct

        if exceeds_limit:
            exceeding_days.append({
                "day": day_label,
                "waste_pct": waste_pct,
                "wasted_meals": total_wasted_meals,
            })

        total_prepared += prepared
        total_served += served
        total_leftovers += leftovers
        total_unaccounted += unaccounted

        processed_days.append({
            "day": day_label,
            "prepared": prepared,
            "served": served,
            "leftovers": leftovers,
            "unaccounted": unaccounted,
            "total_wasted": total_wasted_meals,
            "waste_pct": waste_pct,
            "exceeds_limit": exceeds_limit,
        })

    overall_wasted = total_leftovers + total_unaccounted
    overall_waste_pct = (overall_wasted / total_prepared * 100.0) if total_prepared > 0 else 0.0

    return {
        "max_acceptable_waste_pct": max_acceptable_waste_pct,
        "days": processed_days,
        "exceeding_days": exceeding_days,
        "total_prepared": total_prepared,
        "total_served": total_served,
        "total_leftovers": total_leftovers,
        "total_unaccounted": total_unaccounted,
        "overall_wasted": overall_wasted,
        "overall_waste_pct": overall_waste_pct,
    }


def print_waste_report(summary):
    limit = summary["max_acceptable_waste_pct"]
    print("\n" + "=" * 86)
    print(f"FOOD WASTE MONITORING REPORT (Acceptable Wastage Limit: {limit:.1f}%)")
    print("=" * 86)
    print(
        f"{'Day':<12} | {'Prepared':>8} | {'Served':>6} | {'Leftover':>8} | "
        f"{'Waste %':>8} | {'Status'}"
    )
    print("-" * 86)

    for d in summary["days"]:
        status = "EXCEEDS LIMIT" if d["exceeds_limit"] else "Acceptable"
        print(
            f"{d['day']:<12} | {d['prepared']:>8} | {d['served']:>6} | "
            f"{d['leftovers']:>8} | {d['waste_pct']:>7.2f}% | {status}"
        )

    print("-" * 86)
    print(f"Total Meals Prepared : {summary['total_prepared']}")
    print(f"Total Meals Served   : {summary['total_served']}")
    print(f"Total Leftovers      : {summary['total_leftovers']}")
    if summary["total_unaccounted"] > 0:
        print(f"Unaccounted Meals    : {summary['total_unaccounted']}")
    print(f"Overall Wastage      : {summary['overall_wasted']} meals ({summary['overall_waste_pct']:.2f}%)")

    print("\nDays Exceeding Acceptable Wastage Limit:")
    if summary["exceeding_days"]:
        for item in summary["exceeding_days"]:
            print(
                f"  * {item['day']}: {item['waste_pct']:.2f}% wastage "
                f"({item['wasted_meals']} meals vs. {limit:.1f}% limit)"
            )
    else:
        print("  None — all days stayed within the acceptable limit.")
    print("=" * 86)


def main():
    print("Food Waste Monitoring System")
    max_waste_pct = float(input("Enter maximum acceptable wastage percentage (e.g., 10): ") or 10.0)
    num_days = int(input("Enter number of days to monitor: "))

    daily_records = []
    for i in range(1, num_days + 1):
        print(f"\n--- Entry #{i} ---")
        day = input(f"Day label (default 'Day {i}'): ").strip() or f"Day {i}"
        prepared = int(input("  Meals prepared: "))
        served = int(input("  Meals served: "))
        leftovers = int(input("  Leftover meals: "))
        daily_records.append({
            "day": day,
            "prepared": prepared,
            "served": served,
            "leftovers": leftovers,
        })

    try:
        summary = analyze_food_waste(daily_records=daily_records, max_acceptable_waste_pct=max_waste_pct)
        print_waste_report(summary)
    except ValueError as err:
        print(f"\nInput Error: {err}")


if __name__ == "__main__":
    main()
