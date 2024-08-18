from datetime import datetime

DATE_FORMAT = "%d-%m-%Y"
CATEGORIES = {"I": "Income", "E": "Expense"}


def get_date(prompt, allow_default=False):
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime(DATE_FORMAT)

    try:
        valid_date = datetime.strptime(date_str, DATE_FORMAT)
        return valid_date.strftime(DATE_FORMAT)
    except ValueError:
        print("invalid date fromat. please entry the date in dd-mm-yyyy format")
        return get_date(prompt, allow_default)


def get_amount():
    try:
        amount = float(input("Entry amount: "))
        if amount <= 0:
            raise ValueError("amount must be non-negative non-zero valu.")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()


def get_category():
    category = input(
        "entry the category (I for Income or 'E' for Expense)").upper()
    if category in CATEGORIES:
        return CATEGORIES[category]

    print("invalid category pleasd entry 'I' for income 'Expense' ")
    return get_category()


def get_description():
    return input("enter a description (optional): ")
