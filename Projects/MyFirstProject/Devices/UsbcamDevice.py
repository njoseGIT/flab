from Projects.AMLearn.Devices.Protocols import UsbcamProtocol
from flab.Templates import DeviceTemplate
from flab.Templates import DriverTemplate

#A class for Bronkhorst Devices
class Device(UsbcamProtocol.Protocol, DeviceTemplate.Device, DriverTemplate.Driver):

    device_name = 'UsbcamDevice'

    def __init__(self):
        pass