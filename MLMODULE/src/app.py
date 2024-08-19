from handler import Handler

import logging
import os

from yaml import load
from yaml.loader import SafeLoader

import requests
from pprint import pprint

from handler import Handler

from pathlib import Path
import hashlib

from yaml import load
from yaml.loader import SafeLoader

with open("../config.yaml", "r") as config_file:
    config = load(config_file, Loader=SafeLoader)

block_data = requests.get(
    f"http://{config['SDIP']}:{config['SDPORT']}/blocks?need_active=true"
)

handler_obj = Handler(config=config)

while True:
    handler_obj.action()
