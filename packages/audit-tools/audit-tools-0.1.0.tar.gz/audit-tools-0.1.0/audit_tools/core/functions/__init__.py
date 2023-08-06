import os

from audit_tools.core.functions.logger import Logger
from audit_tools.core.functions.file_manager import create_count_file


def clear():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')