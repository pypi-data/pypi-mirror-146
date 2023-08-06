from rich.prompt import Prompt
from rich import print

from audit_tools.core import Logger, SessionManager, clear, SessionException


class Scanner:
    def __init__(self, session: SessionManager):
        self.session = session

    # Create run event
    def start_count(self):
        clear()

        scanning = True
        while scanning:
            Logger.info("Scanner: Scanning...")

            sku = Prompt.ask("> Enter [bold green]SKU")

            if sku == "" or sku == " " or not sku:
                Logger.info("Scanner: Stopped")
                break

            try:
                _ = self.session.get_product(sku)
            except SessionException as e:
                print(f"> [bold red]{e}")
                continue

            else:
                while True:
                    try:
                        count = int(Prompt.ask("\t> Enter product count [yellow]check all boxes"))

                        if count >= 0:

                            # Extra check incase user somehow enters a sku that passed a false positive
                            try:
                                self.session.count_product(sku, count)
                            except SessionException as e:
                                Logger.error(e)
                                print(f"\t> [bold red]{e}")
                            break

                    except ValueError:
                        Logger.error("Scanner: Invalid count")
                        continue

