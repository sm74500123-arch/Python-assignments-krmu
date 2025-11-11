from datetime import datetime
import csv
import statistics

def welcome():
    print("==========================================")
    print("         GradeBook Analyzer CLI")
    print("==========================================")
    print("Choose input method: manual entry or CSV import.\n")

def manual_entry():
    data = {}
    print("Manual entry mode. Enter students (blank name to stop).")
    while True:
        name = input("Student name: ").strip()
        if name == "":
            break
        while True:
            v = input(f"Marks for {name}: ").strip()
            try:
                marks = float(v)
                if marks < 0:
                    print("Marks cannot be negative. Enter again.")
                    continue
                break
            except ValueError:
                print("Invalid number. Enter numeric marks (e.g., 78 or 78.5).")
        data[name] = marks
    return data

def load_csv(path):
    data = {}
    try:
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if not row:
                    continue
                name = row[0].strip()
                if name == "":
                    continue
                try:
                    marks = float(row[1].strip())
                except (IndexError, ValueError):
                    print(f"Skipping invalid row: {row}")
                    continue
                data[name] = marks
        if not data:
            print("No valid records found in CSV.")
    except FileNotFoundError:
        print("CSV file not found.")
    return data

def calculate_average(marks_dict):
    return sum(marks_dict.values()) / len(marks_dict) if marks_dict else 0.0

def calculate_median(marks_dict):
    if not marks_dict:
        return 0.0
    vals = sorted(marks_dict.values())
    return statistics.median(vals)

def find_max_score(marks_dict):
    if not marks_dict:
        return 0.0, []
    max_score = max(marks_dict.values())
    students = [n for n, s in marks_dict.items() if s == max_score]
    return max_score, students

def find_min_score(marks_dict):
    if not marks_dict:
        return 0.0, []
    min_score = min(marks_dict.values())
    students = [n for n, s in marks_dict.items() if s == min_score]
    return min_score, students

def assign_grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"

def build_grades(marks_dict):
    return {name: assign_grade(score) for name, score in marks_dict.items()}

def grade_distribution(grades):
    dist = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
    for g in grades.values():
        if g in dist:
            dist[g] += 1
    return dist

def passed_failed_lists(marks_dict, pass_threshold=40.0):
    passed = [n for n, s in marks_dict.items() if s >= pass_threshold]
    failed = [n for n, s in marks_dict.items() if s < pass_threshold]
    return passed, failed

def print_summary(marks_dict, grades):
    total = len(marks_dict)
    avg = calculate_average(marks_dict)
    med = calculate_median(marks_dict)
    max_score, max_students = find_max_score(marks_dict)
    min_score, min_students = find_min_score(marks_dict)
    dist = grade_distribution(grades)

    print("\n------ Analysis Summary ------")
    print(f"Students: {total}")
    print(f"Average: {avg:.2f}")
    print(f"Median: {med:.2f}")
    print(f"Max: {max_score:.2f} ( {', '.join(max_students)} )")
    print(f"Min: {min_score:.2f} ( {', '.join(min_students)} )")
    print("Grade distribution:", dist)
    print("-------------------------------\n")

def print_table(marks_dict, grades):
    print(f"{'Name':<20}{'Marks':>8}{'  '}{'Grade':>6}")
    print("-" * 40)
    for name, marks in marks_dict.items():
        print(f"{name:<20}{marks:8.2f}   {grades[name]:>6}")
    print("-" * 40)

def save_to_csv(filename, marks_dict, grades):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Marks", "Grade"])
        for n, m in marks_dict.items():
            writer.writerow([n, f"{m:.2f}", grades[n]])
    print(f"Saved final table to {filename}")

def run_once():
    while True:
        choice = input("Choose (1) Manual entry  (2) Load CSV  (q) Quit : ").strip().lower()
        if choice == "1":
            marks = manual_entry()
            break
        elif choice == "2":
            path = input("Enter CSV file path (name,marks lines): ").strip()
            marks = load_csv(path)
            if marks:
                break
            else:
                continue
        elif choice == "q":
            return
        else:
            print("Invalid choice. Enter 1, 2 or q.")

    if not marks:
        print("No student data to analyze. Returning to main menu.")
        return

    grades = build_grades(marks)
    print_summary(marks, grades)
    print_table(marks, grades)

    passed, failed = passed_failed_lists(marks, pass_threshold=40.0)
    print(f"\nPassed ({len(passed)}): {', '.join(passed) if passed else 'None'}")
    print(f"Failed ({len(failed)}): {', '.join(failed) if failed else 'None'}\n")

    save = input("Export final grade table to CSV? (yes/no): ").strip().lower()
    if save in ("y", "yes"):
        fname = input("Enter output filename (e.g., result.csv): ").strip()
        if fname == "":
            fname = "gradebook_output.csv"
        save_to_csv(fname, marks, grades)

def main():
    welcome()
    while True:
        run_once()
        again = input("\nDo you want to run another analysis? (y/n): ").strip().lower()
        if again not in ("y", "yes"):
            print("Exiting GradeBook Analyzer. Goodbye.")
            break

if __name__ == "__main__":
    main()
