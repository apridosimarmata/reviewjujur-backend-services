from datetime import datetime
from pytz import timezone    

def now():
    jakarta = timezone('Asia/Jakarta')
    now = datetime.now(jakarta).now().timestamp()
    return int(now)