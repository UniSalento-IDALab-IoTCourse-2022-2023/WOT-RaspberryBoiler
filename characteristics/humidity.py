from service import Characteristic, Descriptor
import dbus
import struct
import random

GATT_CHRC_IFACE = "org.bluez.GattCharacteristic1"
NOTIFY_TIMEOUT = 5000

class HumidityCharacteristic(Characteristic):
    HUMIDITY_CHARACTERISTIC_UUID = "2A6F"

    def __init__(self, service):
        self.notifying = False
        Characteristic.__init__(
            self, self.HUMIDITY_CHARACTERISTIC_UUID,
            ["notify", "read"], service
        )

    def get_humidity(self):
        temp = random.randint(0, 100)
        st = struct.pack('<H', temp) #unsigned16int

        # Create a list of dbus.Byte objects from the packed temp value
        value = [dbus.Byte(byte) for byte in st]

        return value

    def set_humidity_callback(self):
        if self.notifying:
            value = self.get_humidity()
            self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])
        return self.notifying

    def StartNotify(self):
        if self.notifying:
            return
        self.notifying = True
        value = self.get_humidity()
        self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])
        self.add_timeout(NOTIFY_TIMEOUT, self.set_humidity_callback)

    def StopNotify(self):
        self.notifying = False

    def ReadValue(self, options):
        value = self.get_humidity()
        return value