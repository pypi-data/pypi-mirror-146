from typing import Optional

import pandas as pd
from audit_tools.core.functions.logger import Logger
from rich import print


def import_from_csv(file_path: str) -> Optional[pd.DataFrame]:
    if file_path:
        imported_data = pd.read_csv(file_path)

        # print(imported_data)

        return imported_data

    return


def create_count_file(products):
    # Creates a pandas DataFrame out of our products
    Logger.info("Creating CSV file for product counts")
    print(products)
    #data = pd.DataFrame(jsonable_encoder(products))

    #data.to_csv("products.csv")

    #print(data)
