from datetime import datetime, timedelta
from pytz import timezone


jakarta = timezone('Asia/Jakarta')

def now():
    now = datetime.now(jakarta).now().timestamp()
    return int(now)

def one_week_ago():
    one_week_ago = datetime.now(jakarta) - timedelta(days = 7)
    return int(one_week_ago.timestamp())