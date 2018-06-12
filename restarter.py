#!/usr/bin/env python3
"""
Check to see if an process is running. If not, restart.
Run this in a cron job
"""
import subprocess
# change this to the name of your process
process_name = "/code/TwitterStream/scraper.py"

tmp = subprocess.getoutput('ps -Af')

if process_name not in tmp[:]:
    print("The process is not running. Let's restart.")
    # newprocess = "python3 %s &" % (process_name)
    subprocess.Popen(
        ['/usr/bin/env/python3', process_name, '&'])
else:
    print("The process is running.")
