# Flab 3
# DeviceManager
# Distributed under GNU GPL v3
# Author: Nicholas Jose

"""
The DeviceManager module contains classes and methods for creating and manipulating devices
"""

import os
import glob

class DeviceManager:
    """
    The DeviceManager class contains methods for loading and manipulating device objects.
    Devices do not necessarily have publicly accessible attributes, and a "get_attr" method may be needed to access these attributes.
    """

    devices = {} # A dictionary that contains device objects
    load_all_devices_completed = False # A boolean that indicates if all devices have been loaded

    def __init__(self):
        pass

    def load_device(self, device_name):
        """
        Loads a device into the Flab object

        :param device_name: the name of the device
        :type device_name: str

        :returns: None
        """
        self.load_object(device_name,'.Devices.', 'device', 'devices', 'Device')

    def load_devices(self, device_names):
        """
        Loads a list of devices into a flab object

        :param device_names: list of device names
        :type device_names: [str]

        :returns: None
        """
        try:
            for d in device_names:
                self.load_device(d)
        except Exception as e:
            self.flab.display('Error in loading devices')
            self.flab.display(e)
        finally:
            pass

    def load_all_devices(self):
        """
        Loads every device present in the current project's Devices folder

        :returns: None
        """
        try:
            cwd = os.getcwd()
            device = glob.glob(cwd + '/Devices/*.py')
            device_names = []
            for d in device:
                if not '__init__.py' in d:
                    device_names.append(d[len(cwd + '/Devices/'):].replace('.py', ''))
            self.load_devices(sorted(device_names))
        except Exception as e:
            self.display(e)
            self.display('Error in loading all devices')
        finally:
            self.display('All devices loaded successfully')
            self.load_all_devices_completed = True

    def reload_device(self, device_name):
        """
        Reloads a single device into flab.

        :param device_name: str

        :returns: None
        """
        self.reload_object(device_name,'devices','device','Device')

    def get_devices(self):
        """
        Returns devices in a flab object.

        :returns: a dictionary of devices
        """
        devices = {}
        keys = self.devices.keys()
        try:
            if len(keys) > 0:
                for i in keys:
                    devices[i] = self.devices[i].get_obj()
        except Exception as e:
            self.display('error in retrieving devices from flab')
            self.display(e)
        return devices
