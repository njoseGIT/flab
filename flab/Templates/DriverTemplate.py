# DriverTemplate
# A template class for device drivers
# Version 2.0.3
# Distributed under GNU GPL v3
# Author: Nicholas Jose

"""
DriverTemplate contains default methods for accessing Driver properties

Version 2.0.3
"""

class Driver():

    version = '2.0.3'

    def __init__(self):
        """
        constructor

        """
        self.driver_name = 'DriverTemplate'

    def get(self, attribute_name):
        """
        Returns the value of an attribute by its name

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

    def get_driver_name(self):
        """
        Returns the name of a Driver

        :returns: name of the driver (string)
        """
        return self.driver_name

    def set_driver_name(self, driver_name):
        """
        Sets the name of a device

        :param driver_name: the driver name
        :type driver_name: string

        :returns: None
        """
        self.driver_name = driver_name
