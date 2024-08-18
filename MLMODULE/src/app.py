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

block_data = requests.get(f"http://sd-module:3000/blocks?need_active=true")

config = {"POLLINT": 8, "SDIP": "sd-module", "SDPORT": 3000, "LOGNAME": "MLMODULE"}

handler_obj = Handler(config=config)

while True:
    handler_obj.action()
