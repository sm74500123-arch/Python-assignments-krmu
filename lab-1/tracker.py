from datetime import datetime

print("=============================================")
print("   Welcome to the Daily Calorie Tracker CLI  ")
print("=============================================")
print("This tool helps you log your meals and track")
print("total calories intake for the day.")
print("You can compare your calories with your daily limit")
print("and save the session for future reference.")
print("---------------------------------------------")

while True:
    try:
        num_meals = int(input("\nHow many meals do you want to enter today? ").strip())
        if num_meals <= 0:
            print("Please enter a positive number (e.g., 3 or 4).")
            continue
        break
    except ValueError:
        print("That's not a valid number. Please enter an integer (e.g., 4).")

meal_names = []
meal_calories = []

print(f"\nNow, you will enter details for {num_meals} meals today.")
for i in range(num_meals):
    print(f"\nMeal {i+1}:")
    while True:
        meal = input("\tEnter meal name: ").strip()
        if meal == "":
            print("\tPlease enter a non-empty meal name.")
            continue
        break
    while True:
        try:
            calories_input = input(f"\tEnter calories for {meal}: ").strip()
            calories = float(calories_input)
            if calories < 0:
                print("\tCalories cannot be negative. Enter a positive number.")
                continue
            break
        except ValueError:
            print("\tInvalid number. Please enter calories as a number (e.g., 350 or 350.5).")
    meal_names.append(meal)
    meal_calories.append(calories)

print("\n---------------------------------------------")
print("Meals Entered:", meal_names)
print("Calories:", meal_calories)
print("---------------------------------------------")

if len(meal_calories) == 0:
    print("\nNo meals entered — cannot calculate totals.")
else:
    total_calories = sum(meal_calories)
    average_calories = total_calories / len(meal_calories)
    while True:
        try:
            daily_limit = float(input("\nEnter your daily calorie limit: ").strip())
            if daily_limit <= 0:
                print("Please enter a positive number for the daily limit.")
                continue
            break
        except ValueError:
            print("Invalid input. Enter the daily limit as a number (e.g., 2000).")

    print("\n---------------------------------------------")
    print(f"Total Calories Consumed: {total_calories:.2f}")
    print(f"Average Calories per Meal: {average_calories:.2f}")

    if total_calories > daily_limit:
        excess = total_calories - daily_limit
        print(f"⚠️  You have exceeded your daily calorie limit by {excess:.2f} calories!")
        status = f"Exceeded by {excess:.2f} calories"
    elif total_calories == daily_limit:
        print("ℹ️  You have exactly met your daily calorie limit.")
        status = "Exactly met"
    else:
        remaining = daily_limit - total_calories
        print(f"✅ You are within your daily calorie limit. {remaining:.2f} calories remaining.")
        status = f"Within limit ({remaining:.2f} remaining)"
    print("---------------------------------------------")

    print("\nMeal Name\t\tCalories")
    print("---------------------------------------------")
    for name, cal in zip(meal_names, meal_calories):
        print(f"{name:<20}{cal:>8.2f}")
    print("---------------------------------------------")
    print(f"Total:\t\t\t{total_calories:.2f}")
    print(f"Average:\t\t{average_calories:.2f}")

    save = input("\nDo you want to save this session to a file? (yes/no): ").strip().lower()
    if save in ("y", "yes"):
        filename = f"calorie_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"  # ✅ changed line
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(filename, "a", encoding="utf-8") as f:
            f.write("Calorie Tracker Log\n")
            f.write(f"Timestamp: {now}\n")
            f.write("---------------------------------------------\n")
            for name, cal in zip(meal_names, meal_calories):
                f.write(f"{name:<20}{cal:>8.2f}\n")
            f.write("---------------------------------------------\n")
            f.write(f"Total Calories: {total_calories:.2f}\n")
            f.write(f"Average Calories: {average_calories:.2f}\n")
            f.write(f"Daily Limit: {daily_limit:.2f}\n")
            f.write(f"Status: {status}\n")
            f.write("\n")
        print(f"\n✅ Report saved successfully to '{filename}'")
    else:
        print("\nReport not saved. Session ended.")

