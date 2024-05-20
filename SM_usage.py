"""
Модуль опроса датчиков, зарегистрированных в БД.

Требуется предварительный запуск модуля сбора данных!
"""

from sensors_module.sensors_module import SensorsModule
from sensors_module.examples.ui import SensorModuleUI

m = SensorsModule()
app = SensorModuleUI(lambda: m.start(app.update_interface), m.stop)

app.mainloop()
