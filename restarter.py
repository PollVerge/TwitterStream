#!/usr/bin/python3

"""
Check to see if an process is running. If not, restart.
Run this in a cron job
"""
import subprocess


def main(process_name):

    tmp = subprocess.getoutput('ps -Af')

    if process_name not in tmp[:]:
        print('The process is not running. Let\'s restart.')
        subprocess.Popen(['python3', process_name, '&'], shell=False)
    else:
        print('The process is running.')


if __name__ == '__main__':
    process_name = '/code/TwitterStream/scraper.py'
    main(process_name=process_name)
