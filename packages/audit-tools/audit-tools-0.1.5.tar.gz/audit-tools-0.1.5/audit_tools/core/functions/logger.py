import logging
from datetime import datetime
import pytz
import os

date_time = datetime.now(pytz.timezone('US/Eastern'))
date = date_time.strftime("%m-%d-%Y-%H-%M")

logs_folder = os.path.isdir('logs')
if not logs_folder:
    os.mkdir('logs')

logging.basicConfig(
    filename=f"./logs/audit-tool-{date}.log",
    format="%(asctime)s %(message)s",
    filemode='w'
)


def get_logger():
    return logging.getLogger(__name__)