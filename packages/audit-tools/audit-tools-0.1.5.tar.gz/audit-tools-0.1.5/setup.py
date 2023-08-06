# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['audit_tools', 'audit_tools.core', 'audit_tools.core.functions']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.3,<2.0.0',
 'openpyxl>=3.0.9,<4.0.0',
 'pandas>=1.4.2,<2.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'rich>=12.2.0,<13.0.0']

setup_kwargs = {
    'name': 'audit-tools',
    'version': '0.1.5',
    'description': 'Auditing tools for Cova POS files',
    'long_description': "# Cova Dispensary POS Audit Tools\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/audit-tools?style=for-the-badge)\n![PyPI](https://img.shields.io/pypi/v/audit-tools?style=for-the-badge)\n\nAn inventory audit tool for speeding up inventory and avoiding errors that occur during processing. This tool will allow\nusers to complete inventory counts with a simple workflow that remedies user error.\n\n\nInstallation and Usage\n-----\n```bash\n$ pypi install audit-tools\n```\n\n```python\nfrom audit_tools import SessionManager, Scanner\n\nsession = SessionManager('/path/to/products.csv') # Path to products.csv\n\n...\n\nsession.count_product('F7X6A7', 20) # Counts 20 F7X6A7's to the inventory\nsession.increase_product('F7X6A7', 10) # Increases F7X6A7 to 30 in the inventory\nsession.reduce_product('F7X6A7', 3) # Reduces F7X6A7 to 27 in the inventory\n\nprint(session.get_product('F7X6A7')) # Returns the row of product with SKU 'F7X6A7'\n\n...\n\nsession.parse_session_data() # Updates session dataframes with accurate content\n\nsession.shutdown() # Saves session data to disk\n\n...\n\n# Usage of the scanner is discouraged as it is not thread safe or efficient\n# Scanner is mostly for testing purposes\n\nscanner = Scanner(session) # Creates a scanner object\n\nscanner.start_count() # Starts the count process\n\nscanner.shutdown() # processes and saves session data to disk\n```\n\n\nProblems\n--------\nAll the problems that we encounter while processing inventory data during an audit.\n\n* Extremely slow\n* Miscounts often occur\n* Redundant item checks\n* Manual data entry\n* User error\n\nSolutions\n---------\nOur ideas for solution implementations for fixing these problems so that an Audit can be completed successfully with\naccuracy and speed.\n\n- #### Session Manager\n    - Allows users to start a new session with a products csv or xlsx file. The session manager will process all incoming\n    products and append them to the sessions DataFrame, when you shut down the session manager will parse all the data in the session, complete variance calculations, raise any alerts, and save the session to the updated csv\n    or xlsx file.\n\n\n- #### Scan & Count\n    - Allows users to scan a SKU and count the number of products to update the session file.\n\n\n- #### Scan & Edit\n    - Allows user to scan a SKU adn manage the data entry for a specified product in the session.\n\n\n- #### Receipt Parser\n    - Allows user to upload scan a receipt and the system will parse the receipt and update the session file.\n\nFeature List\n------------\nThis list will include all the features, current and future.\n\n|    Features     | Working Status |\n|:---------------:|:--------------:|\n| Session Manager | In Development |\n|  Scan & Count   |    Planned     |\n|   Scan & Edit   |    Planned     |\n| Receipt Parser  |    Planned     |\n\n\n\nDev notes:\nIf you come across this project, I am a newish developer, and I am not familiar with the \npython ecosystem especially poetry. If you are confused on the namings in this project, keep in mind\nthis package was created for a sole reason to help the creator at work, and will be used in tandem with\na handheld scanner.\n",
    'author': 'JakePIXL',
    'author_email': 'jakewjevans@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/JakePIXL/audit-tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
