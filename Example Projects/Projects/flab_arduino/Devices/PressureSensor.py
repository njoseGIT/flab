from Projects.flab_arduino.Devices.Drivers import ArduinoMegaDriver
from Projects.flab_arduino.Devices.Protocols import PressureSensorProtocol
from flab.Templates import DeviceTemplate

class Device(ArduinoMegaDriver.Driver, PressureSensorProtocol.Protocol, DeviceTemplate.Device):
    """
    A class for devices measuring pressure with Arduino. This is modifiable and can contain default parameters.
    """

    device_name = 'PressureSensor'

    def __init__(self):
        pass

    def set_flab(self, flab):
        """
        Sets the flab object used by the device

        :param flab: a flab object
        :type flab: Flab
        """
        self.flab = flab