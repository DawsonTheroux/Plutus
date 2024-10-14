import os
import json
import numpy as np
from plutus import Plutus

INPUT_FILE = "data/long.csv"

def get_user_config():
    print("\n---SELECT CONFIG (or create new)---")
    print(f" {[filename.split('.')[0] for filename in os.listdir('conf/') if filename != 'default.json']} - Or some new name")
    return f"{input('Which config would you like to use? ')}.json"

def prompt_user_for_new_categories(categories):
    categories_string = "Current Categories: "
    for category in enumerate(categories):
        category_string += "{categories}, "
    print(categories_string)
    while input("1: Create category, 2: save categories: ") == "1":
        categories.append(input("Please input the new category name: "))

    return categories


def prompt_user_fix_categories(missing_store_names, config):
    categories_string = ""
    for i, category in enumerate(config["categories"]):
        categories_string += f"({i} - {category}), "

    for store_name in missing_store_names:
        print(f"\n\nPossible categories: {categories_string}")
        category_index = input(f"Select a category for {store_name}: ")
        config["mappings"][store_name] = config["categories"][int(category_index)]

    return config 

# for some reason the deposit and withdraw lists are the same. 
I am here



def main():
    csv_filepath = INPUT_FILE
    user_config = None
    # Prompt the user for the budget config they want to use.
    # this includes categories and the mapping between stores and categories.
    config_file = get_user_config()
    # Read the config_file if it exists in the directory. 
    # If not then read the default one.
    with open(f"conf/{config_file if config_file in os.listdir('conf/') else 'default.json'}", 'r') as file:
        user_config = json.load(file)

    print("\n--WITHDRAW CONFIG--")
    user_config["withdraws"]["categories"] = prompt_user_for_new_categories(user_config["withdraws"]["categories"])

    print("\n--DEPOSIT CONFIG--")
    user_config["deposits"]["categories"] = prompt_user_for_new_categories(user_config["deposits"]["categories"])

    print(f"{user_config=}")
    # Create the plutus object that handles budget flow and session.
    print(f"{user_config=}")
    plutus = Plutus(csv_filepath, user_config)

    # Prompt the user to fix the categorization of the missing data.
    print("\n--WITHDRAW CONFIG--")
    missing_store_names = plutus.get_missing_store_names("withdraws")
    user_config["withdraws"] = prompt_user_fix_categories(missing_store_names, user_config["withdraws"])
    print("\n--DEPOSIT CONFIG--")
    missing_store_names = plutus.get_missing_store_names("deposits")
    user_config["deposits"] = prompt_user_fix_categories(missing_store_names, user_config["deposits"])

    # Update user config.
    plutus.set_user_config(user_config)
    plutus.categorize()

    # Get the new config and save it.
    user_config = plutus.dump_config()
    print(f"dumped config {user_config}")
    # with open(f"conf/{config_file}", 'w') as file:
    #     json.dump(user_config, file)

    # Create the summary.
    plutus.create_summary()

if __name__ == "__main__":
    main()
