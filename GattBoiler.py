#!/usr/bin/python3

from advertisement import Advertisement
from service import Application, Service

from characteristics.carbon import CarbonCharacteristic
from characteristics.fault import FaultCharacteristic
from characteristics.performance import PerformanceCharacteristic
from characteristics.temperature import TemperatureCharacteristic
from characteristics.pressure import PressureCharacteristic


GATT_CHRC_IFACE = "org.bluez.GattCharacteristic1"
NOTIFY_TIMEOUT = 5000

class BoilerAdvertisement(Advertisement):
    def __init__(self, index):
        Advertisement.__init__(self, index, "peripheral")
        self.add_local_name("Boiler")
        self.include_tx_power = True

class UserdataService(Service):
    USERDATA_SVC_UUID = "181C"

    def __init__(self, index):
        Service.__init__(self, index, self.USERDATA_SVC_UUID, True)
        self.add_characteristic(TemperatureCharacteristic(self))
        self.add_characteristic(PressureCharacteristic(self))
        self.add_characteristic(CarbonCharacteristic(self))
        self.add_characteristic(FaultCharacteristic(self))
        self.add_characteristic(PerformanceCharacteristic(self))

app = Application()
app.add_service(UserdataService(0))
app.register()

adv = BoilerAdvertisement(0)
adv.register()

try:
    app.run()
except KeyboardInterrupt:
    app.quit()
