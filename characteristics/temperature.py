from service import Characteristic, Descriptor
import dbus
import struct
import random

GATT_CHRC_IFACE = "org.bluez.GattCharacteristic1"
NOTIFY_TIMEOUT = 5000

class TemperatureCharacteristic(Characteristic):
    TEMP_CHARACTERISTIC_UUID = "2A6E"

    def __init__(self, service):
        self.notifying = False

        Characteristic.__init__(
                self, self.TEMP_CHARACTERISTIC_UUID,
                ["notify", "read"], service)

    def get_temperature(self):
        # temp = random.randint(0, 100)
        temp = 50

        st = struct.pack('<h', temp)#signed16int

        # Create a list of dbus.Byte objects from the packed temp value
        value = [dbus.Byte(byte) for byte in st]

        return value

    
    def set_temperature_callback(self):
        if self.notifying:
            value = self.get_temperature()
            self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])

        self.add_timeout(NOTIFY_TIMEOUT, self.set_temperature_callback)

        return self.notifying

    def StartNotify(self):
        if self.notifying:
            return

        self.notifying = True

        value = self.get_temperature()
        self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])
        self.add_timeout(NOTIFY_TIMEOUT, self.set_temperature_callback)

    def StopNotify(self):
        self.notifying = False

    def ReadValue(self, options):
        value = self.get_temperature()
        return value