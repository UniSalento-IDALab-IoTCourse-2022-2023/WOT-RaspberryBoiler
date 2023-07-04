#!/usr/bin/python3

import random
import struct
import dbus

from advertisement import Advertisement
from service import Application, Service, Characteristic, Descriptor

GATT_CHRC_IFACE = "org.bluez.GattCharacteristic1"
NOTIFY_TIMEOUT = 5000

class ThermometerAdvertisement(Advertisement):
    def __init__(self, index):
        Advertisement.__init__(self, index, "peripheral")
        self.add_local_name("Boiler")
        self.include_tx_power = True

class ThermometerService(Service):
    THERMOMETER_SVC_UUID = "181A"

    def __init__(self, index):
        Service.__init__(self, index, self.THERMOMETER_SVC_UUID, True)
        self.add_characteristic(TempCharacteristic(self))
        self.add_characteristic(PressureCharacteristic(self))
        self.add_characteristic(HumidityCharacteristic(self))

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
    
class PressureCharacteristic(Characteristic):
    PRESSURE_CHARACTERISTIC_UUID = "2A6D"

    def __init__(self, service):
        self.notifying = False
        Characteristic.__init__(
            self, self.PRESSURE_CHARACTERISTIC_UUID,
            ["notify", "read"], service
        )

    def get_pressure(self):
        temp = random.randint(500000, 10000000)
        st = struct.pack('<I', temp) #unsigned32int

        # Create a list of dbus.Byte objects from the packed temp value
        value = [dbus.Byte(byte) for byte in st]

        return value

    def set_pressure_callback(self):
        if self.notifying:
            value = self.get_pressure()
            self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])
        return self.notifying

    def StartNotify(self):
        if self.notifying:
            return
        self.notifying = True
        value = self.get_pressure()
        self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])
        self.add_timeout(NOTIFY_TIMEOUT, self.set_pressure_callback)

    def StopNotify(self):
        self.notifying = False

    def ReadValue(self, options):
        value = self.get_pressure()
        return value

class TempCharacteristic(Characteristic):
    TEMP_CHARACTERISTIC_UUID = "2A6E"

    def __init__(self, service):
        self.notifying = False

        Characteristic.__init__(
                self, self.TEMP_CHARACTERISTIC_UUID,
                ["notify", "read"], service)

    def get_temperature(self):
        temp = random.randint(0, 100)
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
    
class TempDescriptor(Descriptor):
    TEMP_DESCRIPTOR_UUID = "2901"
    TEMP_DESCRIPTOR_VALUE = "CPU Temperature"

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

app = Application()
app.add_service(ThermometerService(0))
app.register()

adv = ThermometerAdvertisement(0)
adv.register()

try:
    app.run()
except KeyboardInterrupt:
    app.quit()
