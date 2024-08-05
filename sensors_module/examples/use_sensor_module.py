import logging

from sensors_module.sensors_module import SensorsModule
from sensors_module.examples.ui import SensorModuleUI

from config_reader import config

logging.basicConfig(level=logging.INFO, filename=config.SENSOR_LOG_FILENAME, encoding='utf8')
m = SensorsModule()
app = SensorModuleUI(lambda: m.start(app.update_interface), m.stop)

app.mainloop()

