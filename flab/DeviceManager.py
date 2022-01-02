#DeviceManager
#Version 1.0.0
#Published 27-December-2021
#Distributed under XX license
#Author: Nicholas Jose

import importlib
import os

#A class for dynamically creating device objects
class DeviceManager():

    description = 'Methods for loading and reloading device libraries into flab'
    version = '1.0.0'
    devices = {}

    def __init__(self):
        pass

    #Dynamically load a predefined set of devices into flab as objects. The device is defined in the Devices folder
    def load_device(self, device_name):
        if device_name in self.devices:
            self.reload_device(device_name)
        else:
            try:
                cwf = 'Projects.'+ os.path.split(os.getcwd())[1]
                device_module = importlib.import_module(cwf+'.Devices.' + device_name)
                new_device = device_module.Device()
                new_device.flab = self
                self.devices.update({device_name: new_device})
                self.modules.update({device_name: device_module})
                self.display("loaded : " + device_name)
            except Exception as e:
                self.display('Error loading device ' + device_name)
                self.display(e)
            finally:
                pass

    #Dynaically reload a single device into flab - this only reloads the main device class, not the assoicated drivers and protocols
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


