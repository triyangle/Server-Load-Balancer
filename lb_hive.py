import json
import re
import subprocess
from urllib.request import urlopen

LOGIN = "" # Replace with your 3-letter login (xxx)

# fetches JSON
hive_page = 'https://hivemind-data.firebaseapp.com/latest.json'
page = urlopen(hive_page)
data = json.loads(page.read().decode())["data"]

lowest_load = 1000
use_env = 'hive1.cs'

# Go through each server, finds the hive with the lowest load
for env in data:
    match = re.match(r'(hive.*)',env)
    if(match != None):
        if(data[env] and data[env]["load_avgs"][0] < lowest_load):
            use_env = env
            lowest_load = data[env]["load_avgs"][0]

host = 'cs61c-%s@%s.berkeley.edu' % (LOGIN, use_env)

subprocess.call(["ssh %s" % host], shell=True)

