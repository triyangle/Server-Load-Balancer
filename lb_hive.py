"""
Finds optimal hive server to connect to
"""

import json
import re
import subprocess
from urllib.request import urlopen

LOGIN = "" # Replace with your 3-letter login (xxx)

# fetches JSON
HIVE_PAGE = 'https://hivemind-data.firebaseapp.com/latest.json'
PAGE = urlopen(HIVE_PAGE)
DATA = json.loads(PAGE.read().decode())["data"]

def ema(data, alpha=.15):
    """
    Returns the exponential moving average of the data list with smoothing factor alpha
    """
    result = 0

    for i, datum in enumerate(data):
        weight = alpha if i < len(data) - 1 else 1
        result += weight * (1 - alpha) ** i * datum

    return result

MIN_EMA, MIN_USERS = float('inf'), float('inf')
USE_ENV = 'hive1.cs'

# Go through each server, find active hive servers
for env in DATA:
    match = re.match(r'(hive.*)', env)

    if match and 'users' in DATA[env]:
        current_ema = ema(DATA[env]['load_avgs'])

        if current_ema <= MIN_EMA:
            current_users = len(DATA[env]['users'])

            if current_ema < MIN_EMA or current_users < MIN_USERS:
                USE_ENV = env
                MIN_USERS = current_users
                MIN_EMA = current_ema

HOST = 'cs61c-%s@%s.berkeley.edu' % (LOGIN, USE_ENV)

subprocess.call(["ssh %s" % HOST], shell=True)
