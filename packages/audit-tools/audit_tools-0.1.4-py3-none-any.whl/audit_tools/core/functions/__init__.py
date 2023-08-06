import os

from audit_tools.core.functions.file_manager import *
from audit_tools.core.functions.logger import *


def clear():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')
