import datetime

def generate_perpetual_calendar_dates(start_date, end_date):
    """
    Generates dates for the proposed perpetual calendar and maps them to standard dates.
    """

    latin_days = ["Solis", "Lunae", "Stellae", "Terrae", "Aquae", "Aeris", "Ignis"]
    seasons = ["Florea", "Calida", "Fructus", "Frigida"] # Spring, Summer, Autumn, Winter

    perpetual_calendar_data = []

    current_date = start_date

    # Initial state for the perpetual calendar
    # We need to find a consistent starting point.
    # Let's align the start date of Florea (Spring) with the day after the Year Day.
    # The Year Day is the Winter Solstice (Dec 21/22).
    # So, Dec 22nd is the first day of Florea, Week 1, Solis.

    # Find the first Dec 22nd on or after the start_date
    perpetual_year_start = datetime.date(current_date.year, 12, 22)
    if current_date > perpetual_year_start:
        perpetual_year_start = datetime.date(current_date.year + 1, 12, 22)

    # Let's make Dec 22, 2025 the first day of Florea, Week 1, Solis.
    # This means Dec 21, 2025 (or 2024 for the prev year) is the Year Day.
    # We will track the perpetual calendar state: year, season, week, day_of_week_name
    perpetual_year = perpetual_year_start.year
    perpetual_season_idx = 0 # Florea
    perpetual_week = 1
    perpetual_day_idx = 0 # Solis

    # We need to calculate how many days have passed from the *first* perpetual year start
    # to the current_date, so we can set the initial perpetual_day_idx, perpetual_week, season etc.
    # This ensures a consistent mapping, even if start_date is mid-year.

    # Calculate offset from the perpetual start point (Dec 22nd of some year)
    # This is a bit tricky: let's re-align the perpetual year to start AFTER the Year Day.
    # So, Dec 22nd is Florea, Week 1, Solis for most years.
    # We will simulate the calendar day by day.

    # We'll use a `perpetual_day_counter` to keep track of the 364-day cycle.
    # A day_counter of 0 corresponds to Solis, 1 to Lunae, etc.

    # Let's establish a fixed starting point for the perpetual calendar to calculate all others.
    # E.g., Jan 1, 2000 was a Solis, Day 1 of Florea, Week 1. This is arbitrary but consistent.
    # Our Year Day (Dec 21) would then reset the cycle.
    # To simplify, let's assume Dec 22, 2024 (the day after the 2024 Winter Solstice) was Florea, Week 1, Solis.
    # This makes the 2024 Winter Solstice (Dec 21) the "Year Day".
    # This works well for 2025.

    perpetual_start_anchor = datetime.date(2024, 12, 22) # Florea, Week 1, Solis
    # This means the 2024 Winter Solstice (Dec 21, 2024) was the "Year Day".

    while current_date <= end_date:
        is_leap_year = (current_date.year % 4 == 0 and current_date.year % 100 != 0) or (current_date.year % 400 == 0)

        perpetual_day_name = None
        perpetual_season = None
        perpetual_week_num = None
        perpetual_week_in_season = None
        perpetual_day_in_week = None
        perpetual_extra_day = False
        perpetual_extra_day_type = None

        # --- Perpetual Calendar Logic ---

        # Calculate days from our anchor point to the current date
        days_since_anchor = (current_date - perpetual_start_anchor).days

        # Determine if it's a "Year Day" or "Leap Day"
        if current_date.month == 12 and current_date.day == 21: # Winter Solstice (Year Day)
            # This is the Year Day. It doesn't have a day of the week, season, or week number.
            perpetual_extra_day = True
            perpetual_extra_day_type = "Year Day (Winter Solstice)"
            # The next day (Dec 22) will reset the perpetual cycle to Florea, Week 1, Solis
            # So, for the purpose of calculating the next cycle, we adjust the anchor.
            perpetual_start_anchor = current_date + datetime.timedelta(days=1)

        elif is_leap_year and current_date.month == 6 and current_date.day == 21: # Summer Solstice (Leap Day)
            # This is the Leap Day. Only in leap years, no day of the week, season, or week number.
            perpetual_extra_day = True
            perpetual_extra_day_type = "Leap Day (Summer Solstice)"
            # This also affects the `days_since_anchor` for subsequent calculations.
            # We treat this day as "outside" the 364-day cycle.
            # The next day continues the regular cycle as if this day never happened for counting.
            # No anchor adjustment needed as it's just an extra day in the *current* 364-day cycle
            # but outside the weekly count.
            pass # The logic below will handle regular days, we just mark this as special.

        # If it's not an extra day, calculate its position in the perpetual calendar
        if not perpetual_extra_day:
            days_into_cycle = (current_date - perpetual_start_anchor).days % 364 # 364 regular days

            perpetual_day_idx = days_into_cycle % 7
            perpetual_day_name = latin_days[perpetual_day_idx]

            perpetual_week_num = (days_into_cycle // 7) + 1 # Weeks 1-52

            perpetual_season_idx = (perpetual_week_num - 1) // 13
            perpetual_season = seasons[perpetual_season_idx]

            # Adjust week number relative to the season (Week 1-13 of Season)
            perpetual_week_in_season = (perpetual_week_num - 1) % 13 + 1


        # --- Store Data ---
        perpetual_calendar_data.append({
            "current_date": current_date,
            "std_weekday": current_date.strftime("%A"),
            "std_date": current_date.strftime("%B %d, %Y"),
            "perpetual_day_name": perpetual_day_name,
            "perpetual_season": perpetual_season,
            "perpetual_week_in_season": perpetual_week_in_season,
            "perpetual_extra_day": perpetual_extra_day,
            "perpetual_extra_day_type": perpetual_extra_day_type
        })

        current_date += datetime.timedelta(days=1)

    return perpetual_calendar_data

# Define the start and end dates
start_date = datetime.date(2025, 12, 21)
end_date = datetime.date(2029, 12, 21)

# Generate the calendar data
calendar_output = generate_perpetual_calendar_dates(start_date, end_date)

# Print the results
print("--- Perpetual Calendar vs. Standard Calendar ---")
print("Proposed Days: Solis, Lunae, Stellae, Terrae, Aquae, Aeris, Ignis")
print("Proposed Seasons: Florea (Spring), Calida (Summer), Fructus (Autumn), Frigida (Winter)\n")

for entry in calendar_output:
    std_date_str = f"{entry['std_weekday']:<9} {entry['std_date']}"
    if entry['perpetual_extra_day']:
        perpetual_date_str = f"--- {entry['perpetual_extra_day_type']} ---"
    else:
        perpetual_date_str = (
            f"{entry['perpetual_day_name']:<9} "
            f"{entry['perpetual_season']:<9} "
            f"Week {entry['perpetual_week_in_season']:<2}"
        )
    print(f"Standard: {std_date_str}   |   Perpetual: {perpetual_date_str}")
