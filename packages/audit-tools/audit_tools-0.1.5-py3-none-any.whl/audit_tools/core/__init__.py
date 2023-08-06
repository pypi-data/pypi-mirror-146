import json
import sys
from typing import Optional

import pandas as pd

from audit_tools.core.errors import SessionException
from audit_tools.core.functions import clear, get_logger, import_file, export_file

columns_main = ["Product Name", "Product Classification", "In Stock", "Counted", "Variance", "Notes", "SKU"]


# Session Manager
# Allows the application to store products to allow for updates to information
#
class SessionManager:
    def __init__(self, file_path: str):
        self.variance_counter = 0
        self.missed_counter = 0
        self.is_counting = False
        self.logger = get_logger()
        self.logger.setLevel("DEBUG")
        self.logger.info("Session Manager initialized")

        # Creates a DataFrame based on the Product model
        self.logger.info("------Creating DataFrame------")

        try:
            self.products, self.file_type = import_file(file_path)
        except SessionException as e:
            self.logger.error(e)

        self.variance_items = self.products[0:0]
        self.missed_items = self.products[0:0]
        self.logger.info("Creating alternative data structures")

        self.logger.info("------DataFrame Created------")

    # Update a products count via user input
    def count_product(self, sku: str, count: int = 0):

        exists = self.get_product(sku)

        if exists:
            self.logger.info(f"Updating product: {sku}")

            # Grab the product pertaining to the SKU
            try:
                prod = self.products.index[self.products.select_dtypes(object).eq(sku).any(1)]
            except pd.errors.InvalidIndexError as e:
                self.logger.error(f"Product: {sku} not found")
                self.logger.error(e)
                return False

            # Set the products count to the updated count
            self.products.loc[prod, "Counted"] = count

            return True
        else:
            self.logger.error(f"Product: {sku} not found")
            raise SessionException(f"Product: {sku} not found")

    def increase_product(self, sku: str, count: int = 0):
        exists = self.get_product(sku)

        if exists:
            self.logger.info(f"Updating product: {sku}")

            # Grab the product pertaining to the SKU
            try:
                prod = self.products.index[self.products.select_dtypes(object).eq(sku).any(1)]
            except pd.errors.InvalidIndexError as e:
                self.logger.error(f"Product: {sku} not found")
                self.logger.error(e)
                return False

            counted = self.products["Counted"].iloc[prod[0]]

            # Set the products count to the updated count
            self.products.loc[prod, "Counted"] = count + counted

            return True
        else:
            self.logger.error(f"Product: {sku} not found")
            raise SessionException(f"Product: {sku} not found")

    # Update the products count via receipt input
    def reduce_product(self, sku: str, count: int = 0):
        exists = self.get_product(sku)

        if exists:
            self.logger.info(f"Updating product: {sku}")
            # Grabs the product pertaining to the SKU
            try:
                prod = self.products.index[self.products.select_dtypes(object).eq(sku).any(1)]
            except pd.errors.InvalidIndexError as e:
                self.logger.error(f"Product: {sku} not found")
                self.logger.error(e)
                return

            counted = self.products["Counted"].iloc[prod[0]]

            # Sets the products count to the updated count
            self.products.loc[prod, "Counted"] = count - counted

            return True
        else:
            self.logger.error(f"Product: {sku} not found")
            raise SessionException(f"Product: {sku} not found")

    def remove_product(self, sku: str):
        """
        SHOULD NOT BE USED! Removes a product from the session

        """
        self.products = self.products[~self.products.select_dtypes(str).eq(sku).any(1)]

    def get_product(self, sku: str):
        self.logger.info(f"Getting product: {sku}")

        prod = self.products[self.products['SKU'] == sku]

        if prod.empty:
            self.logger.error(f"Product: {sku} not found")
            raise SessionException(f"Product: {sku} not found")

        return prod.all

    def parse_session_data(self):
        for index, row in self.products.iterrows():
            variance = row["Counted"] - row["In Stock"]
            self.products.loc[index, "Variance"] = variance
            self.products.loc[index, "Notes"] = f"{row['Notes']} Variance caught by A.T." if row["Notes"] else "Variance caught by A.T."
            if variance > 0:
                self.variance_counter += 1
                self.variance_items = pd.concat([
                    self.variance_items,
                    self.products[self.products['SKU'] == row["SKU"]]
                ],
                    ignore_index=True,
                    verify_integrity=True
                )

            if row["Counted"] == 0:
                self.missed_counter += 1
                self.missed_items = pd.concat([
                    self.missed_items,
                    self.products[self.products['SKU'] == row["SKU"]]
                ],
                    ignore_index=True,
                    verify_integrity=True
                )

    def shutdown(self, file_folder: Optional[str] = None):
        """
        Shuts down the session and saves the data to a file

        :param file_folder: When provided the file will be saved to the given folder
        """
        self.logger.info("Shutting down session manager")

        if self.variance_counter > 0:
            print(f"{self.variance_counter} products have a variance!")
            print(self.variance_items)
            self.logger.info(f"{self.variance_counter} items have a variance")
            prods_to_exp = self.variance_items
        else:
            prods_to_exp = self.products

        try:
            file_name = export_file(self.file_type, file_folder, prods_to_exp)
            print(f"Exported to: {file_name}")
            sys.exit()
        except SessionException as e:
            self.logger.error(e)
