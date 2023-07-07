from service import Characteristic, Descriptor
import dbus
import struct

GATT_CHRC_IFACE = "org.bluez.GattCharacteristic1"
NOTIFY_TIMEOUT = 5000

class FaultCharacteristic(Characteristic):
    FAULT_CHARACTERISTIC_UUID = "aef11e22-00c2-4a5c-8aa9-c2e8d7d8034b"

    def __init__(self, service):
        self.notifying = False
        Characteristic.__init__(
            self, self.FAULT_CHARACTERISTIC_UUID,
            ["notify", "read", "write"], service
        )
        self.add_descriptor(FaultDescriptor(self))

    def get_fault(self):
        temp = 1
        st = struct.pack('<H', temp) #unsigned16int

        # Create a list of dbus.Byte objects from the packed temp value
        value = [dbus.Byte(byte) for byte in st]

        return value

    def set_fault_callback(self):
        if self.notifying:
            value = self.get_fault()
            self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])
        return self.notifying

    def StartNotify(self):
        if self.notifying:
            return
        self.notifying = True
        value = self.get_fault()
        self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])
        self.add_timeout(NOTIFY_TIMEOUT, self.set_fault_callback)

    def StopNotify(self):
        self.notifying = False

    def ReadValue(self, options):
        value = self.get_fault()
        return value

    def WriteValue(self, value, options):
        utf8_string = bytearray(value).decode('utf-8')
        self.temp = int(utf8_string)

class FaultDescriptor(Descriptor):
    TEMP_DESCRIPTOR_UUID = "2901"
    TEMP_DESCRIPTOR_VALUE = "Fault Descriptor"

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
