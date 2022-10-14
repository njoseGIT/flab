# Flab
# DeviceManager
# Version 2.0.2
# Published XX-XXX-XXXX
# Distributed under GNU GPL v3
# Author: Nicholas Jose

"""
The DeviceManager module contains classes and methods for creating and manipulating devices
"""

import importlib
import os
import glob
import types
from multiprocessing.managers import NamespaceProxy, SyncManager


class FlabDeviceManager(SyncManager):
    """A manager class for sharing devices in a flab object and across threads and processes.
    Extends the multiprocessing class SyncManager
    """
    pass


class DeviceManager:
    """
    A class for dynamically creating and sharing device objects. Devices do not necessarily have publicly accessible
    attributes, and a "get_attr" method may be needed to access these attributes.
    Version 2.0.2
    """

    version = '2.0.2'

    def __init__(self):
        self.devices = {}
        self.flab_device_manager = FlabDeviceManager()
        self.load_all_devices_completed = False

    def register_device(self, device_name):
        """
        Registers a device within a project with the FlabDeviceManager

        :param device_name: name of the device
        :type device_name: str
        :returns: None
        """
        try:
            cwf = 'Projects.' + os.path.split(os.getcwd())[1]
            device_module = importlib.import_module(cwf + '.Devices.' + device_name)
            self.flab_device_manager.register(device_name, device_module.Device)
            self.display(device_name + ' successfully registered')
            self.modules.update({device_name: device_module})

        except Exception as e:
            self.display('error in registering: ' + device_name)
            self.display(e)
        finally:
            pass

    # register a list of devices within a project with the FlabDeviceManager
    def register_devices(self, device_names):
        """registers a list of devices within a project with the FlabDeviceManager. This is required
        before the devices are loaded into a flab object.

        :param device_names: array of device names
        :type device_names: [str]

        :return: None
        """
        for device_name in device_names:
            self.register_device(device_name)

    def register_all_devices(self):
        """
        Registers all devices within a project with the FlabDeviceManager

        :returns: None
        """
        cwd = os.getcwd()
        devices = glob.glob(cwd + '/Devices/*.py')
        device_names = []
        for d in devices:
            device_names.append(d[len(cwd + '/Devices/'):].replace('.py', ''))
        self.register_devices(sorted(device_names))

    def start_device_manager(self):
        """
        starts the device manager

        :returns: None
        """
        try:
            self.flab_device_manager.start()
        except Exception as e:
            self.display(e)
        finally:
            pass

    def load_device(self, device_name):
        """
        Loads a predefined set of devices into a flab object as objects. The device is defined in the Devices folder.

        :param device_name: name of the device
        :type device_name: str

        :returns: None
        """
        if device_name not in self.modules:
            self.display(device_name + ' is not registered')
        else:
            try:
                create_method = getattr(self.flab_device_manager, device_name)
                new_device = create_method()
                new_device.set_flab(self)
                self.devices.update({device_name: new_device})
                self.display("loaded : " + device_name)
            except Exception as e:
                self.display('Error loading device ' + device_name)
                self.display(e)
            finally:
                pass

    def load_devices(self, device_names):
        """
        Loads a list of devices into a flab object

        :param device_names: [str]

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
        Loads all devices in a project folder into a flab object

        :returns: None
        """
        try:
            cwd = os.getcwd()
            devices = glob.glob(cwd + '/Devices/*.py')
            device_names = []
            for d in devices:
                device_names.append(d[len(cwd + '/Devices/'):].replace('.py', ''))
            self.load_devices(sorted(device_names))
        except Exception as e:
            self.display('Error in loading all devices')
            self.display(e)
        finally:
            self.load_all_devices_completed = True

    def reload_device(self, device_name):
        """
        Reloads a single device into flab. This only reloads the main device class, not the associated drivers and
        protocols. This is now deprecated after v1.0.0
        """
        try:
            device_module = importlib.reload(self.modules[device_name])
            new_device = self.modules[device_name].Device()
            new_device.flab = self
            self.devices.update({device_name: new_device})
            self.modules.update({device_name: device_module})
            self.display("reloaded : " + device_name)
        except Exception as e:
            self.display('Error reloading device ' + device_name)
            self.display(e)
        finally:
            pass

    def get_devices(self):
        """
        returns devices in a flab object

        :returns: a list of device names
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


def Proxy(target):
    """
    A method for creating proxy classes for devices.

    :param target: the target device object

    :returns: DeviceProxy
    """

    class DeviceProxy(NamespaceProxy):
        _exposed_ = tuple(dir(target))

        def __getattr__(self, name):
            result = super().__getattr__(name)
            if isinstance(result, types.MethodType):
                def wrapper(*args, **kwargs):
                    return self._callmethod(name, args)  # Note the return here

                return wrapper
            return result

    return DeviceProxy
