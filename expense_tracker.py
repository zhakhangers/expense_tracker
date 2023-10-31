
import csv
import datetime
from expense import Expense
import calendar

def main():

    print(f"running expense tracker")
    filepath = 'expenses.csv'
    budget = 10000
    
    new_expense = get_expense_data()

    #save that data inside csv
    save_expense_data(new_expense, filepath)


    #show the data inside csv (summary)
    summary_expense_data(filepath, budget)


def get_expense_data():
    #ask for input data (category) OR keep track of the current date automatically
    expense_date = current_date()


    #ask for input data (amount of expense)
    expense_amount = get_expense_amount()


    # #ask for input data (name)
    expense_name = get_expense_name()


    expense_category =  get_expense_category()

    return Expense(name = expense_name, category=expense_category, amount= expense_amount, date=expense_date)

def current_date():
    current_date = datetime.date.today()
    print(f"The current date: {current_date}")
    return current_date

def get_expense_amount():
    exp_amount = float(input("Type amount of expense: "))
    return exp_amount


def get_expense_name():
    exp_name = input("Type name of expense: ")
    return exp_name


def get_expense_category():
    #show categories and corresponding number to them 
    expense_categories = [
        'Food',
        'House',
        'Entertainment',
        'Transportation',
        'Unexpected', 
        'Finance',
        'Clothes',
        'Travel',
        'Other'
    ]
    print("Choose category:\n")
    for i, category in enumerate(expense_categories):
        print(f"{i+1}. {category}\n")
    #ask for input data (category)
    exp_category = int(input("Choose category and type corressponding number: "))
    if exp_category not in range(1,len(expense_categories)+1):
        print("Invalid input for category, type number for corresponding category!")
        get_expense_category()
    return exp_category


def save_expense_data(expense: Expense, filepath):
    print(f"Saving the data")

    with open(filepath, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([expense.date, expense.name, expense.amount, expense.category])
    print("Expense data saved successfully!")


def summary_expense_data(filepath, budget):

    print(f"Showing summary of expenses")
    expenses: list[Expense] = []
    with open(filepath, "r") as f:
        lines = f.readlines()
        for line in lines:
            expense_name, expense_category, expense_amount, expense_date = line.strip().split(",")
            line_expense = Expense(
                name=expense_name,
                amount=float(expense_amount),
                category=expense_category,
                date=expense_date
            )
            expenses.append(line_expense)

    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount

    print("Expenses By Category 📈:")
    for key, amount in amount_by_category.items():
        print(f"  {key}: ${amount:.2f}")

    amount_by_date = {}
    for expense in expenses:
        key = expense.date
        if key in amount_by_date:
            amount_by_date[key] += expense.amount
        else:
            amount_by_date[key] = expense.amount

    print("Expenses By Date 📈:")
    for key, amount in amount_by_date.items():
        print(f"  {key}: ${amount:.2f}")

    total_spent = sum([x.amount for x in expenses])
    print(f"💵 Total Spent: ${total_spent:.2f}")

    remaining_budget = budget - total_spent
    if remaining_budget < 0:
        print("You are out of budget for this month!")
    else:
        print(f"✅ Budget Remaining: ${remaining_budget:.2f}")

    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day
    if remaining_days != 0:
        daily_budget = remaining_budget / remaining_days
    else:
        daily_budget = remaining_budget / 1
    
    print(green(f"👉 Budget Per Day: ${daily_budget:.2f}"))


def green(text):
    return f"\033[92m{text}\033[0m"




if __name__ == "__main__":
    main()