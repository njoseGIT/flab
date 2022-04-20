#DeviceManager
#Version 1.1.1
#Published 11-April-2022
#Distributed under GNU GPL v3
#Author: Nicholas A. Jose

import importlib
import os
import glob
import types
from multiprocessing.managers import NamespaceProxy, SyncManager

#A class for sharing device objects across flab/multiprocessing
class FlabDeviceManager(SyncManager):
    pass

#A class for dynamically creating device objects
#Device objects in 1.0.0 have publicly accessible attributes
class DeviceManager():

    description = 'Actions for loading and reloading device libraries into flab'
    version = '1.1.0'
    devices = {}
    flab_device_manager = FlabDeviceManager()
    load_all_devices_completed = False

    def __init__(self):
        pass

    # register a device within a project with the FlabDeviceManager
    def register_device(self, device_name):
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
        for device_name in device_names:
            self.register_device(device_name)

    # register all devices within a project with the FlabDeviceManager
    def register_all_devices(self):
        cwd = os.getcwd()
        devices = glob.glob(cwd+'/Devices/*.py')
        device_names = []
        for d in devices:
            device_names.append(d[len(cwd+'/Devices/'):].replace('.py',''))
        self.register_devices(sorted(device_names))

    #star the flab device manager
    def start_device_manager(self):
        try:
            self.flab_device_manager.start()
        except Exception as e:
            self.display(e)
        finally:
            pass

    #Dynamically load a predefined set of devices into flab as objects. The device is defined in the Devices folder
    def load_device(self, device_name):
        if device_name not in self.modules:
            self.display(device_name + ' is not registered')
        else:
            try:
                create_method = getattr(self.flab_device_manager,device_name)
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
        try:
            for d in device_names:
                self.load_device(d)
        except Exception as e:
            self.flab.display('Error in loading devices')
            self.flab.display(e)
        finally:
            pass

    def load_all_devices(self):
        try:
            cwd = os.getcwd()
            devices = glob.glob(cwd+'/Devices/*.py')
            device_names = []
            for d in devices:
                device_names.append(d[len(cwd+'/Devices/'):].replace('.py',''))
            self.load_devices(sorted(device_names))
        except Exception as e:
            self.display('Error in loading all devices')
            self.display(e)
        finally:
            self.load_all_devices_completed = True

    #Dynaically reload a single device into flab - this only reloads the main device class, not the assoicated drivers and protocols
    #This is now deprecated as of v1.0.0
    def reload_device(self, device_name):
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

#A proxy class for sharing devices
def Proxy(target):

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



