from service import Characteristic, Descriptor
import dbus
import struct
import random

GATT_CHRC_IFACE = "org.bluez.GattCharacteristic1"
NOTIFY_TIMEOUT = 5000

class PerformanceCharacteristic(Characteristic):
    YIELD_CHARACTERISTIC_UUID = "aef11e23-00c2-4a5c-8aa9-c2e8d7d8034b"
    temp = 100.0
    
    def __init__(self, service):
        self.notifying = False
        Characteristic.__init__(
            self, self.YIELD_CHARACTERISTIC_UUID,
            ["notify", "read", "write"], service
        )
        self.add_descriptor(PerformanceDescriptor(self))

    def get_performance(self):
        st = struct.pack('<f', self.temp + random.uniform(0.01, 0.09))

        # Create a list of dbus.Byte objects from the packed temp value
        value = [dbus.Byte(byte) for byte in st]
        return value
    
    def set_performance_callback(self):
        if self.notifying:
            value = self.get_performance()
            self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])
        return self.notifying

    def StartNotify(self):
        if self.notifying:
            return
        self.notifying = True
        value = self.get_performance()
        self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])
        self.add_timeout(NOTIFY_TIMEOUT, self.set_performance_callback)

    def StopNotify(self):
        self.notifying = False

    def ReadValue(self, options):
        value = self.get_performance()
        return value

    def WriteValue(self, value, options):
        utf8_string = bytearray(value).decode('utf-8')
        self.temp = float(utf8_string)

class PerformanceDescriptor(Descriptor):
    TEMP_DESCRIPTOR_UUID = "2901"
    TEMP_DESCRIPTOR_VALUE = "Performance Descriptor"

    def __init__(self, characteristic):
        Descriptor.__init__(
                self, self.TEMP_DESCRIPTOR_UUID,
                ["read"],
                characteristic)

    def ReadValue(self, options):
        value = []
        desc = self.TEMP_DESCRIPTOR_VALUE

        for c in desc:
            value.append(dbus.Byte(c.encode()))

        return value