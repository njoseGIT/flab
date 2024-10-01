from Projects.AMLearn.Devices.Protocols import BronkhorstProtocol
from flab.Templates import DeviceTemplate
from flab.Templates import DriverTemplate

#A class for Bronkhorst Devices
class Device(BronkhorstProtocol.Protocol, DeviceTemplate.Device, DriverTemplate.Driver):

    device_name = 'BronkhorstDevice'

    def __init__(self):
        pass