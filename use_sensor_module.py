from sensors_module.sensors_module import SensorsModule
from sensors_module.ui import SensorModuleUI

m = SensorsModule()
app = SensorModuleUI(lambda: m.start(app.update_interface), m.stop)

app.mainloop()
