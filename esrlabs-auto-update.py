#!/usr/bin/env python3

import schedule
import time
import os
import logging
import json
import argparse
import sys
import subprocess

from updaters.flashmate import *
from startup import *

from appdirs import *

# Defaults
APP_NAME = 'esrlabs-auto-update'
APP_AUTHOR = 'esrlabs'
USER_DATA_DIR = user_data_dir(APP_NAME, APP_AUTHOR)
download_dir = os.path.join(USER_DATA_DIR, 'downloads')
config_file = os.path.join(USER_DATA_DIR, 'config.json')

LOG_FILENAME = os.path.join(USER_DATA_DIR, 'esrlabs-auto-update.log')
LOG_LEVEL = logging.INFO

# Define and parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('init', nargs='?')
args = parser.parse_args()
if args.init and not os.path.exists(args.init):
    sys.exit("Path does not exists {}".format(args.init))

if os.path.exists(config_file):
    with open(config_file) as json_file:
        config = json.load(json_file)
else:
    config = {
        'installPath': os.path.join(USER_DATA_DIR, 'esrlabs-tools')
    }

if args.init:
    config['installPath'] = args.init

with open(config_file, 'w') as outfile:
    json.dump(config, outfile, indent=4)

install_dir = config["installPath"]

os.makedirs(USER_DATA_DIR, exist_ok=True)
os.makedirs(install_dir, exist_ok=True)
os.makedirs(download_dir, exist_ok=True)

logging.basicConfig(filename=LOG_FILENAME,
                    level=LOG_LEVEL,
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')


def self_update_if_needed():
    check_output = subprocess.check_output(
        "python3 -m pip list --outdated", shell=True, text=True)
    if 'esrlabs-auto-update' in check_output:
        logging.info('Running self update...')
        subprocess.check_call(
            "python3 -m pip install --upgrade esrlabs-auto-update",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)
        #os.execv(__file__, sys.argv)
        sys.exit(0)


def check_updates_job():
    # Check self updates
    self_update_if_needed()

    logging.info('Checking for updates...')
    updaters = [Flashmate(download_dir, install_dir)]
    for updater in updaters:
        logging.info('Checking: {}'.format(updater.name))
        updates_available = updater.check_updates()
        if updates_available:
            logging.info('Downloading: {}'.format(updater.name))
            downloaded = updater.download()
            if downloaded:
                logging.info('Installing: {}'.format(updater.name))
                updater.install()
                logging.info('Successfully installed {}'.format(updater.name))
            else:
                logging.warning('Downloading {} failed'.format(updater.name))
        else:
            logging.info('No updates')


set_startup_rules(__file__)

# Loop forever, doing scheduled jobs
schedule.every().day.at("01:00").do(check_updates_job)
#schedule.every(10).seconds.do(check_updates_job)
while True:
    schedule.run_pending()
    time.sleep(60)
