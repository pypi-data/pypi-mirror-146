import sys

import pandas as pd

from audit_tools.core.errors import SessionException
from audit_tools.core.functions import clear, Logger


# Session Manager
# Allows the application to store products to allow for updates to information
#
class SessionManager:
    def __init__(self, file_path: str):
        self.variance_counter = 0
        self.is_counting = False
        Logger.info("Session Manager initialized")

        # Creates a DataFrame based on the Product model
        if '.xlsx' in file_path:
            self.file_type = ".xlsx"
            self.products = pd.read_excel(file_path)
        elif '.csv' in file_path:
            self.file_type = ".csv"
            self.products = pd.read_csv(file_path)
        elif '.json' in file_path:
            self.file_type = ".json"
            self.products = pd.read_json(file_path)
        else:
            print("Invalid file type!")
            Logger.error("Invalid file type!")
            sys.exit()

        Logger.info("Created DataFrame")

    # Update a products count via user input
    def count_product(self, sku: str, count: int = 0):

        exists = self.get_product(sku)

        if exists:
            Logger.info(f"Updating product: {sku}")

            # Grab the product pertaining to the SKU
            try:
                prod = self.products.index[self.products.select_dtypes(object).eq(sku).any(1)]
            except pd.errors.InvalidIndexError as e:
                Logger.error(f"Product: {sku} not found")
                Logger.error(e)
                return False

            counted = self.products["Counted"].iloc[prod[0]]

            # Set the products count to the updated count
            self.products.loc[prod, "Counted"] = count + counted

            return True
        else:
            Logger.error(f"Product: {sku} not found")
            raise SessionException(f"Product: {sku} not found")

    # Update the products count via receipt input
    def reduce_product(self, sku: str, count: int = 0):
        exists = self.get_product(sku)

        if exists:
            Logger.info(f"Updating product: {sku}")
            # Grabs the product pertaining to the SKU
            try:
                prod = self.products.index[self.products.select_dtypes(object).eq(sku).any(1)]
            except pd.errors.InvalidIndexError as e:
                Logger.error(f"Product: {sku} not found")
                Logger.error(e)
                return

            counted = self.products["Counted"].iloc[prod[0]]

            # Sets the products count to the updated count
            self.products.loc[prod, "Counted"] = count - counted

            return True
        else:
            Logger.error(f"Product: {sku} not found")
            raise SessionException(f"Product: {sku} not found")

    def remove_product(self, sku: str):
        """
        SHOULD NOT BE USED! Removes a product from the session

        """
        self.products = self.products[~self.products.select_dtypes(str).eq(sku).any(1)]

    def get_product(self, sku: str):
        Logger.info(f"Getting product: {sku}")

        prod = self.products[self.products['SKU'] == sku]

        if prod.empty:
            Logger.error(f"Product: {sku} not found")
            raise SessionException(f"Product: {sku} not found")

        return prod.all

    def parse_session_data(self):
        for index, row in self.products.iterrows():
            variance = row["Counted"] - row["In Stock"]
            self.products.loc[index, "Variance"] = variance
            if variance > 0:
                self.variance_counter += 1

    def dump_session(self):
        if self.file_type == ".xlsx":
            self.products.to_excel(f"output_file{self.file_type}", index=False)
        elif self.file_type == ".json":
            self.products.to_json(f"output_file{self.file_type}", orient="records")
        else:
            self.products.to_csv(f"output_file{self.file_type}", index=False)

    def shutdown(self):
        Logger.info("Shutting down session manager")
        self.parse_session_data()

        if self.variance_counter > 0:
            print(f"{self.variance_counter} products have a variance!")
            Logger.info(f"{self.variance_counter} items have a variance")

        self.dump_session()

