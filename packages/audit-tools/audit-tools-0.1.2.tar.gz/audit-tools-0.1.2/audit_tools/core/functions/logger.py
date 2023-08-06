import logging
from datetime import datetime
import pytz

date_time = datetime.now(pytz.timezone('US/Eastern'))
date = date_time.strftime("%m-%d-%Y-%H-%M")


logging.basicConfig(
    filename=f"./logs/audit-tool-{date}.log",
    format="%(asctime)s %(message)s",
    filemode='w'
)

Logger = logging.getLogger(__name__)

Logger.setLevel(logging.DEBUG)
