#UiManager
#Version 1.0.0
#Published 1-January-2021
#Distributed under GNU GPL v3
#Author: Nicholas Jose

from PyQt5 import uic
import importlib
import time
import os
import glob

#A class for managing UIs. This is inherited by typically inherited by Flab
class UiManager():

    description = 'Methods for converting and loading user interfaces. Note: PyQT interfaces generally need to be ' \
                  'be started within a main method or separate process'
    version = '1.0.0'
    uis = {}

    def __init__(self):
        pass

    #Convert UI from ui file to python file with the same name within the "Designs" folder
    def convert_ui(self, ui_file_name):
        try:
            cwd = os.getcwd()
            if 'Boot' in cwd:
                os.chdir('..')
            cwd = os.getcwd()
            ui_file_path = cwd +'/UIs/Designs/'+ui_file_name+'.ui'
            py_file_path = cwd +'/UIs/Designs/'+ui_file_name+'.py'
            with open(py_file_path,'w') as pyfile:
                uic.compileUi(ui_file_path,pyfile)
            time.sleep(1)
        except Exception as e:
            self.display('Error in .ui to .py file conversion')
            self.display(e)
        finally:
            pass

    #Dynamically create a ui class return its instance from a design and methods class
    def create_ui(self, design_name, design_class_name, methods_name):
        try:
            cwf = 'Projects.'+os.path.split(os.getcwd())[1]
            ui_mod = importlib.import_module(cwf+'.UIs.Designs.'+ design_name)
            methods_mod = importlib.import_module(cwf+'.UIs.Methods.'+methods_name)
            ui_class = ui_mod.__getattribute__(design_class_name)
            methods_class = methods_mod.Methods
            new_ui_class = type('NewUI',(ui_class, methods_class),{})
            new_ui = new_ui_class(self)
            return new_ui
        except Exception as e:
            self.display('Error in ui creation')
            self.display(e)
        finally:
            pass

    #load a predefined UI from the UI folder into flab
    def load_ui(self, ui_name):
        cwf = 'Projects.'+os.path.split(os.getcwd())[1]
        try:
            mo = importlib.import_module(cwf+'.UIs.' + ui_name)
            nt = mo.UI(self)
            #dictionary entry
            mod = {ui_name:mo}
            ntd = {ui_name:nt}
            self.uis[ui_name] = nt
            self.modules.update(mod)
            self.display(ui_name + ' loaded successfully.')
        except Exception as e:
            self.display('Error loading UI ' + ui_name + '.')
            self.display(e)
        finally:
            pass

    #Load a list of UIs into flab.
    def load_uis(self, ui_names):
        try:
            load_err = ''
            for g in ui_names:
                g_err = self.load_ui(g)
                load_err = load_err + g_err
            if load_err == '':
                self.display('All uis loaded successfully.')
            return load_err
        except Exception as e:
            self.display('Error in loading UIs: ' + ui_names)
        finally:
            pass

    #load every UI in the UI folder
    def load_all_uis(self):
        try:
            uis = glob.glob('UIs/*.py')
            ui_names = []
            self.display(uis)
            for g in uis:
                ui_names.append(g[4:].replace('.py', ''))
            self.load_uis(ui_names)
        except Exception as e:
            self.display('Error loading all UIs')
        finally:
            pass

    #dynamically reload a ui
    def reload_ui(self,ui_name):
        try:
            mo = importlib.reload(self.modules[ui_name])
            nt = self.modules[ui_name].UI(self)
            #dictionary entry
            mod = {ui_name:mo}
            ntd = {ui_name:nt}
            self.uis.update(ntd)
            self.modules.update(mod)
        except Exception as e:
            self.display(' Error reloading UIs ' + ui_name)
            self.display(e)
        finally:
            pass

    #dynamically reload all uis
    def reload_all_uis(self,ui_names):
        try:
            reload_err = ''
            for g in ui_names:
                err = self.reload_ui(g)
                reload_err = reload_err + err
            if reload_err == '':
                self.display('All UIs reloaded successfully')
        except Exception as e:
            self.display('Error reloading all UIs')
            self.display(e)
        finally:
            pass