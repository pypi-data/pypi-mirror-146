from typing import Optional

from rich.prompt import Prompt

from audit_tools.core.functions import Logger, clear


class Scanner:
    def __init__(self, session):
        self.keep_scanning = True
        self.session = session

    def count_item(self) -> Optional[list]:
        count = 0
        sku = Prompt.ask("> Enter product [bold green]SKU")

        if sku:
            is_count = False

            while not is_count:
                try:
                    count = int(Prompt.ask("> [bold]Enter product count"))

                    if count:
                        is_count = True

                except ValueError:
                    print("[bold red]Please enter a valid integer.")

            is_extra = False

            while not is_extra:
                try:
                    extra_items = int(Prompt.ask("> [bold red]Enter any missed items"))

                    if extra_items or extra_items == 0:
                        count = count + extra_items
                        is_extra = True

                except ValueError:
                    print("[bold red]Please enter a valid integer.")

            return [sku, count]

        return

    def count(self):
        clear()
        self.keep_scanning = True
        while self.keep_scanning:

            item = self.count_item()
            if item:
                self.session.count_product(item[0], item[1])
            else:
                self.keep_scanning = False
        self.session.is_counting = False
        clear()
        # print(self.items)
        # create_count_file(self.session.get_products())

    def mold(self):
        clear()
        while self.keep_scanning:
            pass

def product_from_scan(sku: str, count: int):
    """
    Creates a Pydantic model from the sku and count.

    :param sku: A string representing the SKU of a product.
    :param count: A Integer indicating the number of items in a scan.
    :return: Product object
    """

    Logger.info("Creating new product object from scan")
    #product = Product(sku=sku, count=count)

    return #product
