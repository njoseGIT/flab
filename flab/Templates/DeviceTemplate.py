# DeviceTemplate.py
# A template class for devices
# Version 2.0.3
# Distributed under GNU GPL v3
# Author: Nicholas Jose

"""
DeviceTemplate contains default methods for accessing device properties

Version 2.0.3
"""

from flab.Templates import DriverTemplate
from flab.Templates import ProtocolTemplate
import inspect

class Device(DriverTemplate.Driver, ProtocolTemplate.Protocol):

    version = '2.0.3'

    def __init__(self):
        """
        constructor
        """

        self.device_name = 'DeviceTemplate'
        self.protocol_name = 'ProtocolTemplate'
        self.driver_name = 'DriverTemplate'

    def get(self, attribute_name):
        """Returns the value of an attribute by its name

        :param attribute_name: name of the attribute
        :type attribute_name: string

        :returns: object
        """
        return self.__getattribute__(attribute_name)

    def set(self, attribute_name, value):
        """
        Sets the value of a Device attribute

        :param attribute_name: name of the attribute
        :type attribute_name: string

        :param value: new value of the attribute

        :returns: None
        """
        self.__setattr__(attribute_name, value)

    def get_device_name(self):
        """
        Returns the name of a Device

        :returns: name of the device (string)
        """
        return self.device_name

    def set_device_name(self, device_name):
        """
        Sets the name of a device

        :param device_name: the device name
        :type device_name: string

        :returns: None
        """
        self.device_name = device_name

    def get_flab(self):
        """
        returns the flab object of a Device

        :returns: flab object (Flab)
        """
        return self.flab

    def set_flab(self, flab):
        """
        sets the flab object of a Device

        :param flab: a flab object
        :type flab: Flab

        :returns: None
        """
        self.flab = flab

    def list_attributes(self):
        """
        Returns the attributes of a Device in a list

        :returns: None
        """
        variables = []
        for i in inspect.getmembers(self):
            if not inspect.ismethod(i[1]) and not inspect.ismethoddescriptor(i[1]) and not inspect.isbuiltin(i[1]) and not '__' in i[0]:
                variables.append(i[0])
        return variables

    def list_methods(self):
        """
        returns the methods of a Device in a list

        :returns: list of strings
        """
        variables = []
        for i in inspect.getmembers(self):
            if inspect.ismethod(i[1]) and not inspect.ismethoddescriptor(i[1]) and not inspect.isbuiltin(i[1]) and not '__' in i[0]:
                variables.append(i[0])
        return variables

    def list_method_args(self,method_name):
        """
        returns the arguments of a method of a Device in a list

        :param method_name: name of a method
        :type method_name: string

        :returns: list of strings
        """
        fullargspec = inspect.getfullargspec(self.get(method_name))
        return fullargspec