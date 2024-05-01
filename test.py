import holidays

# Define Los Angeles holidays
la_holidays = holidays.US(state='CA', years=2019)

print("afsds")
# Create a list of Los Angeles holidays
la_holidays_list = [holiday for holiday in la_holidays]

print(la_holidays_list)