# Personal Expense & Budget Tracker

## 1. Project Description
The Personal Expense & Budget Tracker is a Python-based application that helps users record daily expenses, organize spending into categories, set monthly budgets, and generate spending summaries.

## 2. Objectives
- Record and manage daily expenses.
- Organize expenses by category.
- Set and monitor monthly budgets.
- Calculate total monthly spending.
- Search and filter expense records.
- Store data using CSV file handling.

## 3. Technologies Used
- Python
- CSV
- `datetime` module
- `collections` module
- Visual Studio Code

## 4. Key Features
- Add and view daily expenses.
- Categorize expenses such as Food, Travel, Shopping, Education, and Bills.
- Set or update monthly budgets for each category.
- Check spending against budget limits.
- Generate category-wise spending summaries.
- Search expenses by ID, description, category, or date.
- Filter expenses by category or month.
- Store expense and budget records permanently in CSV files.
- Validate dates and amounts to reduce invalid inputs.

## 5. Project Files
- `expense_tracker.py` — Main Python application.
- `expenses.csv` — Stores expense records.
- `budgets.csv` — Stores monthly budget details.
- `README.md` — Project documentation.

The CSV files are created automatically when the program runs.

## 6. How to Run

1. Install Python on your computer.
2. Open the project folder in Visual Studio Code.
3. Open the terminal.
4. Run the following command:

```powershell
& "C:\Users\Admin\.local\bin\python3.14.exe" expense_tracker.py
```

No external Python libraries are required.

## 7. How to Use
1. Run the program.
2. Select **Add Expense** to record a daily expense.
3. Select a category and enter the date, description, and amount.
4. Use **Set Monthly Budget** to define category-wise spending limits.
5. View the budget summary to check spending and remaining balances.
6. Generate monthly spending summaries.
7. Search or filter records when required.
8. Select Exit to close the application.

## 8. Data Storage
The application uses two CSV files:

- `expenses.csv` stores expense IDs, dates, categories, descriptions, and amounts.
- `budgets.csv` stores the month, category, and budget amount.

The application loads saved data whenever it runs, so records remain available between sessions.

## 9. Learning Outcomes
- Improved understanding of Python functions and collections.
- Practised CSV file handling.
- Learned date validation using the `datetime` module.
- Implemented searching and filtering.
- Applied exception handling for invalid inputs.
- Developed basic budget monitoring and data analysis.

## 10. Future Scope
- Add charts to visualize monthly spending.
- Export reports to PDF or Excel.
- Develop a graphical user interface.
- Add income tracking and savings calculations.
- Integrate database storage.
- Add expense editing and deletion features.

## 11. Conclusion
The Personal Expense & Budget Tracker demonstrates how Python can be used to manage daily expenses and monitor monthly budgets. It provides practical experience in file handling, data processing, date operations, and basic financial management.

