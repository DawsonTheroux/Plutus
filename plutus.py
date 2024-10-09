import pandas as pd
import numpy as np
import re

INPUT_FILE = "data/long.csv"

# I want to take in the data and then calculate if I am plus or minux
def filter_and_calculate(df, month):
    # Convert the date column to a datetime format (assuming the date column is named 'Date Posted')
    df['Date Posted'] = pd.to_datetime(df['Date Posted'], format='%Y%m%d')
    # Filter for the specific and month
    filtered_df = df[(df['Date Posted'].dt.month == month)]
    # Calculate the sum of the ' Transaction Amount' column for the filtered rows
    total_amount = filtered_df[' Transaction Amount'].sum()
    return total_amount

def calculate_account_balance(df):
    # Take only the transactions, then just sum them?
    print(f"{df.columns=}")
    transactions = df[" Transaction Amount"].to_numpy().T
    for value in transactions:
        print(value)
    print(f"{transactions.shape=}")
    print(f"{transactions.sum()=}")

def get_categories(df):
    categories = df["Description"].to_numpy().T
    values = [value.split("#")[0].split("  ")[0][4:] for value in categories]

    print(values)
    

def main():
    df = pd.read_csv(INPUT_FILE, skiprows=1)
    get_categories(df)
    print(f"{df.head()}")

    
if __name__ == "__main__":
    main()
