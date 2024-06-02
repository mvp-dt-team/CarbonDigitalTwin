import logging

from sensors_module.sensors_module import SensorsModule
from sensors_module.examples.ui import SensorModuleUI

LOG_FILENAME = 'sensors_module.log'
logging.basicConfig(level=logging.INFO, filename=LOG_FILENAME)
m = SensorsModule()
app = SensorModuleUI(lambda: m.start(app.update_interface), m.stop)

app.mainloop()
