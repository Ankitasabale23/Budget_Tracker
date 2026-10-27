
import csv
import os
from datetime import datetime
from collections import defaultdict

EXPENSE_FILE = "expenses.csv"
BUDGET_FILE = "budgets.csv"

CATEGORIES = [
    "Food",
    "Travel",
    "Shopping",
    "Education",
    "Bills",
    "Health",
    "Entertainment",
    "Other"
]

EXPENSE_FIELDS = ["ID", "Date", "Category", "Description", "Amount"]
BUDGET_FIELDS = ["Month", "Category", "Budget"]


def create_files():
    """Create CSV files with headers if they do not exist."""
    if not os.path.exists(EXPENSE_FILE):
        with open(EXPENSE_FILE, "w", newline="", encoding="utf-8") as file:
            csv.DictWriter(file, fieldnames=EXPENSE_FIELDS).writeheader()

    if not os.path.exists(BUDGET_FILE):
        with open(BUDGET_FILE, "w", newline="", encoding="utf-8") as file:
            csv.DictWriter(file, fieldnames=BUDGET_FIELDS).writeheader()


def load_expenses():
    """Load all expenses from CSV."""
    with open(EXPENSE_FILE, "r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def load_budgets():
    """Load all budgets from CSV."""
    with open(BUDGET_FILE, "r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def save_expenses(expenses):
    """Save expenses to CSV."""
    with open(EXPENSE_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=EXPENSE_FIELDS)
        writer.writeheader()
        writer.writerows(expenses)


def save_budgets(budgets):
    """Save budgets to CSV."""
    with open(BUDGET_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=BUDGET_FIELDS)
        writer.writeheader()
        writer.writerows(budgets)


def get_amount(prompt):
    """Accept only positive monetary amounts."""
    while True:
        try:
            amount = float(input(prompt))
            if amount <= 0:
                print("Amount must be greater than zero.")
                continue
            return round(amount, 2)
        except ValueError:
            print("Please enter a valid number.")


def get_date():
    """Get a valid date from the user."""
    while True:
        date_text = input(
            "Enter date (YYYY-MM-DD), or press Enter for today: "
        ).strip()

        if not date_text:
            return datetime.today().strftime("%Y-%m-%d")

        try:
            return datetime.strptime(date_text, "%Y-%m-%d").strftime(
                "%Y-%m-%d"
            )
        except ValueError:
            print("Invalid date. Use YYYY-MM-DD.")


def choose_category():
    """Display and select an expense category."""
    print("\nExpense Categories:")
    for number, category in enumerate(CATEGORIES, start=1):
        print(f"{number}. {category}")

    while True:
        try:
            choice = int(input("Choose category number: "))
            if 1 <= choice <= len(CATEGORIES):
                return CATEGORIES[choice - 1]
            print("Choose a number from the list.")
        except ValueError:
            print("Please enter a valid number.")


def add_expense():
    """Record a new expense."""
    expenses = load_expenses()

    if expenses:
        expense_id = max(int(e["ID"]) for e in expenses) + 1
    else:
        expense_id = 1

    date = get_date()
    category = choose_category()
    description = input("Enter expense description: ").strip()

    if not description:
        description = "General expense"

    amount = get_amount("Enter amount (₹): ")

    expense = {
        "ID": str(expense_id),
        "Date": date,
        "Category": category,
        "Description": description,
        "Amount": f"{amount:.2f}"
    }

    expenses.append(expense)
    save_expenses(expenses)

    print("\nExpense added successfully!")
    check_budget(date[:7], category)


def display_expenses(expenses):
    """Display a list of expenses."""
    if not expenses:
        print("No expenses found.")
        return

    print("\n" + "-" * 75)
    print(f"{'ID':<5}{'Date':<13}{'Category':<18}{'Amount (₹)':<15}Description")
    print("-" * 75)

    for expense in expenses:
        print(
            f"{expense['ID']:<5}"
            f"{expense['Date']:<13}"
            f"{expense['Category']:<18}"
            f"{float(expense['Amount']):<15.2f}"
            f"{expense['Description']}"
        )

    print("-" * 75)


def view_expenses():
    """View all recorded expenses."""
    display_expenses(load_expenses())


def set_budget():
    """Set or update a monthly budget for a category."""
    month = input("Enter budget month (YYYY-MM): ").strip()

    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Invalid month. Use YYYY-MM.")
        return

    category = choose_category()
    amount = get_amount("Enter monthly budget (₹): ")

    budgets = load_budgets()
    updated = False

    for budget in budgets:
        if budget["Month"] == month and budget["Category"] == category:
            budget["Budget"] = f"{amount:.2f}"
            updated = True
            break

    if not updated:
        budgets.append({
            "Month": month,
            "Category": category,
            "Budget": f"{amount:.2f}"
        })

    save_budgets(budgets)
    print(f"Budget saved for {category} in {month}.")

    check_budget(month, category)


def check_budget(month, category):
    """Compare category spending with its monthly budget."""
    budgets = load_budgets()
    expenses = load_expenses()

    budget = next(
        (
            float(b["Budget"]) for b in budgets
            if b["Month"] == month and b["Category"] == category
        ),
        None
    )

    if budget is None:
        return

    spent = sum(
        float(e["Amount"]) for e in expenses
        if e["Date"].startswith(month) and e["Category"] == category
    )

    print(f"Monthly budget: ₹{budget:.2f}")
    print(f"Amount spent:   ₹{spent:.2f}")
    print(f"Remaining:      ₹{budget - spent:.2f}")

    if spent > budget:
        print("WARNING: You have exceeded your budget!")
    elif spent == budget:
        print("You have reached your budget limit.")
    else:
        print("You are within your budget.")


def budget_summary():
    """Display budgets and spending for a selected month."""
    month = input("Enter month (YYYY-MM): ").strip()

    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Invalid month. Use YYYY-MM.")
        return

    budgets = [
        b for b in load_budgets()
        if b["Month"] == month
    ]
    expenses = [
        e for e in load_expenses()
        if e["Date"].startswith(month)
    ]

    if not budgets:
        print("No budgets set for this month.")

    print(f"\n===== BUDGET SUMMARY: {month} =====")

    for budget in budgets:
        category = budget["Category"]
        limit = float(budget["Budget"])

        spent = sum(
            float(e["Amount"]) for e in expenses
            if e["Category"] == category
        )

        print(f"\nCategory: {category}")
        print(f"Budget:   ₹{limit:.2f}")
        print(f"Spent:    ₹{spent:.2f}")
        print(f"Balance:  ₹{limit - spent:.2f}")

        if spent > limit:
            print("Status: Budget exceeded")
        else:
            print("Status: Within budget")


def spending_summary():
    """Show monthly spending totals by category."""
    month = input("Enter month (YYYY-MM): ").strip()

    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Invalid month. Use YYYY-MM.")
        return

    expenses = [
        e for e in load_expenses()
        if e["Date"].startswith(month)
    ]

    if not expenses:
        print("No expenses recorded for this month.")
        return

    totals = defaultdict(float)

    for expense in expenses:
        totals[expense["Category"]] += float(expense["Amount"])

    total = sum(totals.values())

    print(f"\n===== SPENDING SUMMARY: {month} =====")
    for category, amount in sorted(totals.items()):
        print(f"{category:<20} ₹{amount:.2f}")

    print("-" * 35)
    print(f"Total Spending: ₹{total:.2f}")


def search_expenses():
    """Search by description or category."""
    keyword = input("Enter search keyword: ").strip().lower()

    if not keyword:
        print("Please enter a keyword.")
        return

    results = [
        expense for expense in load_expenses()
        if keyword in expense["Description"].lower()
        or keyword in expense["Category"].lower()
        or keyword in expense["Date"].lower()
        or keyword == expense["ID"].lower()
    ]

    display_expenses(results)


def filter_expenses():
    """Filter expenses by category or month."""
    print("\n1. Filter by Category")
    print("2. Filter by Month")
    choice = input("Choose option: ").strip()

    expenses = load_expenses()

    if choice == "1":
        category = choose_category()
        results = [
            e for e in expenses if e["Category"] == category
        ]
        display_expenses(results)

    elif choice == "2":
        month = input("Enter month (YYYY-MM): ").strip()

        try:
            datetime.strptime(month, "%Y-%m")
        except ValueError:
            print("Invalid month. Use YYYY-MM.")
            return

        results = [
            e for e in expenses if e["Date"].startswith(month)
        ]
        display_expenses(results)

    else:
        print("Invalid option.")


def main():
    create_files()

    while True:
        print("\n===================================")
        print(" PERSONAL EXPENSE & BUDGET TRACKER")
        print("===================================")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Set Monthly Budget")
        print("4. View Budget Summary")
        print("5. View Spending Summary")
        print("6. Search Expenses")
        print("7. Filter Expenses")
        print("8. Exit")

        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            set_budget()
        elif choice == "4":
            budget_summary()
        elif choice == "5":
            spending_summary()
        elif choice == "6":
            search_expenses()
        elif choice == "7":
            filter_expenses()
        elif choice == "8":
            print("Thank you for using Expense Tracker!")
            break
        else:
            print("Invalid choice. Please select 1-8.")


if __name__ == "__main__":
    main()
