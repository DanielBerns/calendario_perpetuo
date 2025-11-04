import datetime

def generate_perpetual_calendar_dates(start_date, end_date):
    """
    Generates dates for the proposed perpetual calendar with constellation-inspired season names.
    """

    latin_days = ["Solis", "Lunae", "Stellae", "Terrae", "Aquae", "Aeris", "Ignis"]
    # Updated season names based on Option 3 (Revised)
    seasons = ["Hunter", "Lion", "Eagle", "Water Bearer"]

    perpetual_calendar_data = []

    current_date = start_date

    # Establish a fixed starting point for the perpetual calendar:
    # We will anchor the start of "Hunter" (Week 1, Solis) to the day after
    # the December Solstice (Year Day).
    # Let's assume Dec 22, 2024 was the start of Hunter, Week 1, Solis.
    # This means Dec 21, 2024 was the Year Day (December Solstice).
    perpetual_start_anchor = datetime.date(2024, 12, 22) # Hunter, Week 1, Solis

    while current_date <= end_date:
        is_leap_year_gregorian = (current_date.year % 4 == 0 and current_date.year % 100 != 0) or (current_date.year % 400 == 0)

        perpetual_day_name = None
        perpetual_season = None
        perpetual_week_in_season = None
        perpetual_extra_day = False
        perpetual_extra_day_type = None

        # --- Perpetual Calendar Logic ---

        # Check for special Solstice/Equinox days that are 'extra-calendar'
        if current_date.month == 12 and current_date.day == 21: # December Solstice (Year Day)
            perpetual_extra_day = True
            perpetual_extra_day_type = "Year Day (December Solstice)"
            # The next day (Dec 22) will reset the perpetual cycle to Hunter, Week 1, Solis
            # So, for the purpose of calculating the next cycle, we adjust the anchor.
            perpetual_start_anchor = current_date + datetime.timedelta(days=1)

        elif is_leap_year_gregorian and current_date.month == 6 and current_date.day == 21: # June Solstice (Leap Day)
            perpetual_extra_day = True
            perpetual_extra_day_type = "Leap Day (June Solstice)"
            # This day is also outside the regular 364-day cycle and doesn't affect the anchor.
            pass # No specific anchor change for leap day, it's just a pause in the 364 cycle.


        # If it's not an extra day, calculate its position in the perpetual calendar
        if not perpetual_extra_day:
            total_days_from_anchor = (current_date - perpetual_start_anchor).days

            leap_days_to_subtract = 0
            temp_date_for_leap_check = perpetual_start_anchor
            while temp_date_for_leap_check < current_date:
                if (temp_date_for_leap_check.month == 6 and temp_date_for_leap_check.day == 21 and
                    (temp_date_for_leap_check.year % 4 == 0 and temp_date_for_leap_check.year % 100 != 0) or (temp_date_for_leap_check.year % 400 == 0)):
                    leap_days_to_subtract += 1
                temp_date_for_leap_check += datetime.timedelta(days=1)

            days_into_cycle = (total_days_from_anchor - leap_days_to_subtract) % 364

            perpetual_day_idx = days_into_cycle % 7
            perpetual_day_name = latin_days[perpetual_day_idx]

            perpetual_week_num_overall = (days_into_cycle // 7) + 1 # Weeks 1-52

            # Now map to the 4 seasons (Hunter, Lion, Eagle, Water Bearer)
            perpetual_season_idx = (perpetual_week_num_overall - 1) // 13
            perpetual_season = seasons[perpetual_season_idx]

            perpetual_week_in_season = (perpetual_week_num_overall - 1) % 13 + 1


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
print("--- Perpetual Calendar vs. Standard Calendar (Constellation-Inspired Seasons) ---")
print("Proposed Days: Solis, Lunae, Stellae, Terrae, Aquae, Aeris, Ignis")
print("Proposed Seasons: Hunter, Lion, Eagle, Water Bearer (13 weeks each)")
print("\nInterpretive Overlay for Seasonal Experience:")
print("  - Hunter: Northern Winter / Southern Summer (Starts after Dec Solstice)")
print("  - Lion:      Northern Spring / Southern Autumn (Starts after March Equinox)")
print("  - Eagle:     Northern Summer / Southern Winter (Starts after June Solstice)")
print("  - Water Bearer:     Northern Autumn / Southern Spring (Starts after Sept Equinox)\n")

for entry in calendar_output:
    std_date_str = f"{entry['std_weekday']:<9} {entry['std_date']}"
    if entry['perpetual_extra_day']:
        perpetual_date_str = f"--- {entry['perpetual_extra_day_type']:<30} ---"
    else:
        # Add Equinox markers for clarity, similar to before
        start_of_season_marker = ""
        # March Equinox starts Lion
        if (entry['current_date'].month == 3 and entry['current_date'].day == 22 and
            entry['perpetual_season'] == "Lion" and entry['perpetual_week_in_season'] == 1 and entry['perpetual_day_name'] == "Solis") :
            start_of_season_marker = "(Equinox)"
        # September Equinox starts Water Bearer
        elif (entry['current_date'].month == 9 and entry['current_date'].day == 22 and
            entry['perpetual_season'] == "Water Bearer" and entry['perpetual_week_in_season'] == 1 and entry['perpetual_day_name'] == "Solis"):
            start_of_season_marker = "(Equinox)"

        perpetual_date_str = (
            f"{entry['perpetual_day_name']:<9} "
            f"{entry['perpetual_season']:<11} " # Adjust width for longer name
            f"Week {entry['perpetual_week_in_season']:<2} {start_of_season_marker}"
        )
    print(f"Standard: {std_date_str:<30} |   Perpetual: {perpetual_date_str}")
