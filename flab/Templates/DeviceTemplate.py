# Flab 3
# DeviceTemplate.py
# Distributed under GNU GPL v3
# Author: Nicholas Jose

"""
DeviceTemplate contains a template Device class,
which should be inherited by user Device classes to function properly
"""

import inspect

class Device():
    """
    Device description needed
    """

    device_name = 'DeviceTemplate' #Mandatory attribute. This must match the name of the .py file

    def __init__(self):
        pass

    def get(self, attribute_name):
        """
        Returns the value of a Device attribute

        :param attribute_name: str

        :returns: device attribute
        """
        return self.__getattribute__(attribute_name)

    def set(self, attribute_name, value):
        """
        Sets the value of a Device attribute

        :param attribute_name: str

        :returns: None
        """
        self.__setattr__(attribute_name, value)

    def get_device_name(self):
        """
        Returns the name of a Device

        :returns: device name
        :rtype: str
        """
        return self.device_name

    def set_device_name(self, device_name):
        """
        Sets the name of a Device

        :param device_name: str
        :returns: None
        """
        self.device_name = device_name

    def get_flab(self):
        """
        Returns the flab object of a device

        :returns: flab
        :rtype: Flab
        """
        return self.flab

    def set_flab(self, flab):
        """
        Sets the flab object of a Device

        :param flab: Flab
        :returns: None
        """
        self.flab = flab

    def list_attributes(self) -> list:
        """
        Returns the attributes of a Device in a list.

        :returns: the list of device attributes
        :rtype: list
        """
        attributes = []
        try:
            for i in inspect.getmembers(self):
                if not inspect.ismethod(i[1]) and not inspect.ismethoddescriptor(i[1]) and not inspect.isbuiltin(i[1]) and not '__' in i[0]:
                    attributes.append(i[0])

        except Exception as e:
            self.flab.display('Error in listing ' + self.device_name + ' attributes')
            self.flab.display(e)

        finally:
            return attributes

    def list_methods(self):
        """
        Returns the methods of a Device in a list.

        :returns: the list of device methods
        :rtype: list
        """

        variables = []
        for i in inspect.getmembers(self):
            if inspect.ismethod(i[1]) and not inspect.ismethoddescriptor(i[1]) and not inspect.isbuiltin(i[1]) and not '__' in i[0]:
                variables.append(i[0])
        return variables

    def list_method_args(self,method_name):
        """
        Returns the arguments of a method of a Device in a list

        :param method_name: str

        :returns: method arguments
        :rtype: list
        """
        fullargspec = inspect.getfullargspec(self.get(method_name))
        return fullargspec