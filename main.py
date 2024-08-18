from datetime import datetime
import csv
import matplotlib.pyplot as plt
import pandas as pd
from data_entry import get_amount, get_category, get_date, get_description


class CSV:
    FILE_NAME = "finance_data.csv"
    COLUMS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initalize_csv(cls):
        try:
            pd.read_csv(cls.FILE_NAME)

        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMS)
            df.to_scv(cls.FILE_NAME, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }

        with open(cls.FILE_NAME, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, cls.COLUMS)
            writer.writerow(new_entry)
            print("Entry add succesfull!")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.FILE_NAME)
        df["date"] = pd.to_datetime(pd["date"], format=CSV.FORMAT)
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)
        mask = (df["date"] >= start_date & df["date"] <= end_date)
        filtered_df = df.loc(mask)

        if filtered_df.empty:
            print("No transactions found in the given date")
        else:
            print(
                f"Ttransiactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}")
            print(filtered_df.to_string(index=False, formatters={
                "date": lambda x: x.strftime(CSV.FORMAT)}))

            total_income = filtered_df[filtered_df["category"]
                                       == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"]
                                        == "Expense"]["amount"].sum()
            print("\nSummary:")
            print(f"Total Income ${total_income:.2f}")
            print(f"Total Expense ${total_expense:.2f}")
            print(F"Net savings ${(total_income - total_expense):.2f}")

        return filtered_df


def add():
    CSV.initalize_csv()
    date = get_date(
        "enter the date of transiction (dd=mm-yyy) or Enter today's date:",
        allow_default=True
    )
    amount = get_amount()
    description = get_description()
    category = get_category()

    CSV.add_entry(date, amount, category, description)


def plot_transaction(df):
    df.set_index("date", inplace=True)

    income_df = {
        df[df["category"] == "Income"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    }

    expense_df = {
        df[df["category"] == "Expense"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)

    }

    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index,
            expense_df["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expense over the time")
    plt.legend()
    plt.grid()
    plt.show()


def main():
    while True:
        print("\n1. add new transiaction")
        print("2. view transiaction and summary witin a date range")
        print("3. Exit")

        choice = input("Enter your choice (1-3)")
        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date, end_date)

            if input("Do you want to see a plot? (y/n) ").lower() == "Y":
                plot_transaction(df)

        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("invalid input enter 1, 2 or 3")


if __name__ == "__main__":
    main()
