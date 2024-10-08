import logging

from sensors_module import SensorsModule

from yaml import load
from yaml.loader import SafeLoader

with open("../config.yaml", "r") as config_file:
    config = load(config_file, Loader=SafeLoader)


logging.basicConfig(level=logging.INFO, filename=config["LOGNAME"], encoding="utf8")
app = SensorsModule()
while True:
    app.action()
