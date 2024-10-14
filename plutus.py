import re
import json
import os

import pandas as pd
import numpy as np

CONIFG_DIR = "config/"

    # def filter_and_calculate(df, month):
    #     # Convert the date column to a datetime format (assuming the date column is named 'Date Posted')
    #     df['Date Posted'] = pd.to_datetime(df['Date Posted'], format='%Y%m%d')
    #     # Filter for the specific and month
    #     filtered_df = df[(df['Date Posted'].dt.month == month)]
    #     # Calculate the sum of the ' Transaction Amount' column for the filtered rows
    #     total_amount = filtered_df[' Transaction Amount'].sum()
    #     return total_amount
    #
    # # I want to take in the data and then calculate if I am plus or minux
    # def filter_and_calculate(df, month):
    #     # Convert the date column to a datetime format (assuming the date column is named 'Date Posted')
    #     df['Date Posted'] = pd.to_datetime(df['Date Posted'], format='%Y%m%d')
    #     # Filter for the specific and month
    #     filtered_df = df[(df['Date Posted'].dt.month == month)]
    #     # Calculate the sum of the ' Transaction Amount' column for the filtered rows
    #     total_amount = filtered_df[' Transaction Amount'].sum()
    #     return total_amount
    # def calculate_account_balance(df):
    #     # Take only the transactions, then just sum them?
    #     print(f"{df.columns=}")
    #     transactions = df[" Transaction Amount"].to_numpy().T
    #     for value in transactions:
    #         print(value)
    #     print(f"{transactions.shape=}")
    #     print(f"{transactions.sum()=}")


class Plutus:
    #
    # __init__ - The initial control flow of the program.
    #
    def __init__(self, input_filepath, user_config):
        self.input_filepath = input_filepath
        self.user_config = user_config
        # read the CSV
        self.df = pd.read_csv(input_filepath, skiprows=1)
        # Assign the store names for both dfs.
        self.assign_store_names()
        # Split input df inot deposit and withdraw
        self.df_deposits, self.df_withdraws = self.split_deposit_withdraw()
        # Attempt to assign categories to all the transactions.
        self.categorize()

    #
    # split_deposit_withdraw - converts input df to deposit and withdraw df.
    #
    def split_deposit_withdraw(self):
        return self.df[self.df[" Transaction Amount"] > 0], self.df[self.df[" Transaction Amount"] < 0]

    #
    # assign_store_names - Add a column with the filtered store names.
    #
    def assign_store_names(self):
        store_names = [value.split("  ")[0][4:].split('#')[0].rstrip('1234567890#') for value in self.df["Description"].to_numpy().T]
        self.df = self.df.assign(StoreNames=store_names)

    #
    # Categorize - Attempt to categorize stores based on the user config.
    #
    def categorize(self):
        print(self.user_config)
        mappings = self.user_config["withdraws"]["mappings"]
        self.df_withdraws = self.df_deposits.assign(Category=self.df_withdraws["StoreNames"].map(mappings))
        mappings = self.user_config["deposits"]["mappings"]
        self.df_deposits = self.df_deposits.assign(Category=self.df_deposits["StoreNames"].map(mappings))

    #
    # get_missing_store_names 
    #
    def get_missing_store_names(self, transaction_type):
        target_df = None
        match transaction_type:
            case "deposits":
                target_df = self.df_deposits
            case "withdraws":
                target_df = self.df_withdraws
            case _:
                assert False, f"Failed to get missing categories for {transaction_type=}"

        missing_store_names = []
        store_names = target_df["StoreNames"].to_numpy().T
        for i, category in enumerate(target_df["Category"].to_numpy().T):
            if np.isnan(category):
                missing_store_names.append(store_names[i])
        return missing_store_names

    # Update user_config
    def set_user_config(self, user_config):
        self.user_config = user_config

    def create_summary(self):
        print("NOT IMPLIMENTED -- create_summary()")

    def dump_config(self):
        return self.user_config
    


""" Task Devision:
    Plutus class will not handle files or anything. It will just be given the data and then thats it.
    I think maybe the overall flow should also not be worried by plutus? For example I think that 
    the server session should handle the flow of prompting the user for new categories. Plutus will just make
    it wasy to do so.

    I think this means that the server should not know about pandas, but plutus should not know about the server.

    This also means that plutus should not know about user interaction.
    """

