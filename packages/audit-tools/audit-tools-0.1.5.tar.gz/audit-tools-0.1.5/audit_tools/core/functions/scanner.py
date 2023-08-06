from rich.prompt import Prompt, Confirm
from rich import print

from audit_tools.core import SessionManager, clear, SessionException, export_file


class Scanner:
    def __init__(self, session: SessionManager):
        self.session = session

    # Create run event
    def start_count(self):
        clear()

        scanning = True
        while scanning:
            self.session.logger.info("Scanner: Scanning...")

            sku = Prompt.ask("> Enter [bold green]SKU")

            if sku == "" or sku == " " or not sku:
                self.session.logger.info("Scanner: Stopped")
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
                                self.session.logger.error(e)
                                print(f"\t> [bold red]{e}")
                            break

                    except ValueError:
                        self.session.logger.error("Scanner: Invalid count")
                        continue

    def count_missed(self):
        self.session.logger.info("Scanner: Counting missed products...")
        print(f"> [bold orange]You may have missed items!")
        print(self.session.missed_items)
        self.start_count()

    def shutdown(self):
        self.session.logger.info("Scanner: Shutting down...")

        self.session.parse_session_data()

        while self.session.missed_counter > 0:
            user_input = Confirm.ask("> [bold orange]Would you like to count missed items?", default=True)
            if user_input:
                self.count_missed()
            else:
                break

        try:
            file_name = export_file(self.session.file_type, None, self.session.variance_items)
            print(f"> [bold]Exported to [green]{file_name}")
        except SessionException as e:
            self.session.logger.error(e)
            print(f"> [bold red]{e}")
