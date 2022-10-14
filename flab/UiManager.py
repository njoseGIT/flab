# Flab
# UiManager
# Version 2.0.2
# Published XX-XXX-XXXX
# Distributed under GNU GPL v3
# Author: Nicholas Jose

"""The UIManager module contains class and methods for creating, loading and converting UIs"""

import importlib
import time
import os
import glob


class UiManager:
    """
    A class containing methods for converting and loading UIs. Note: PyQT interfaces generally need to bed
    be started within a main method or separate process
    """

    version = '2.0.2'

    def __init__(self):
        self.uis = {}

    def convert_ui(self, ui_file_name):
        """
        Converts a UI from a ui file to python file with the same name within the "Designs" folder using the PyQt
        library. This method is now deprecated to reduce dependencies on PyQt.

        :param ui_file_name: name of the .ui file in the Designs folder
        :type ui_file_name: str

        :returns: None
        """

        try:
            cwd = os.getcwd()
            if 'Boot' in cwd:
                os.chdir('../..')
            cwd = os.getcwd()
            ui_file_path = cwd + '/UIs/Designs/' + ui_file_name + '.ui'
            py_file_path = cwd + '/UIs/Designs/' + ui_file_name + '.py'
            with open(py_file_path, 'w') as pyfile:
                pass
            # uic.compileUi(ui_file_path,pyfile)
            time.sleep(1)
        except Exception as e:
            self.display('Error in .ui to .py file conversion')
            self.display(e)
        finally:
            pass

    def create_ui(self, design_name, design_class_name, methods_name):
        """
        Dynamically creates a ui class that inherits the design and methods classes.

        :param design_name: name of the design file
        :type design_name: str

        :param design_class_name: name of the design class
        :type design_class_name: str

        :param methods_name: NAme of the methods class
        :type methods_name: str

        :return: ui object or None
        """
        try:
            cwf = 'Projects.' + os.path.split(os.getcwd())[1]
            ui_mod = importlib.import_module(cwf + '.UIs.Designs.' + design_name)
            methods_mod = importlib.import_module(cwf + '.UIs.Methods.' + methods_name)
            ui_class = ui_mod.__getattribute__(design_class_name)
            methods_class = methods_mod.Methods
            new_ui_class = type('NewUI', (ui_class, methods_class), {})
            new_ui = new_ui_class(self)
            return new_ui
        except Exception as e:
            self.display('Error in ui creation')
            self.display(e)
            return None
        finally:
            pass

    def load_ui(self, ui_name):
        """
        Loads a predefined UI from the UI folder into a flab object

        :param ui_name: name of the ui

        :type ui_name: str
        :return: None
        """
        cwf = 'Projects.' + os.path.split(os.getcwd())[1]
        try:
            mo = importlib.import_module(cwf + '.UIs.' + ui_name)
            nt = mo.UI(self)
            # dictionary entry
            mod = {ui_name: mo}
            ntd = {ui_name: nt}
            self.uis[ui_name] = nt
            self.modules.update(mod)
            self.display(ui_name + ' loaded successfully.')
        except Exception as e:
            self.display('Error loading UI ' + ui_name + '.')
            self.display(e)
        finally:
            pass

    def load_uis(self, ui_names):
        """
        Load a list of UIs into flab

        :param ui_names: list of UI names
        :type ui_names: [str]

        :returns: None
        """
        try:
            for g in ui_names:
                self.load_ui(g)
            self.display('All uis loaded successfully.')
        except Exception as e:
            self.display('Error in loading UIs: ' + ui_names)
            self.display(e)
        finally:
            pass

    def load_all_uis(self):
        """
        Load every UI in the UI folder

        :returns: None
        """
        try:
            uis = glob.glob('UIs/*.py')
            ui_names = []
            self.display(uis)
            for g in uis:
                ui_names.append(g[4:].replace('.py', ''))
            self.load_uis(ui_names)
        except Exception as e:
            self.display('Error loading all UIs')
            self.display(e)
        finally:
            pass

    def reload_ui(self, ui_name):
        """
        Dynamically reload a UI

        :param ui_name: name of UI
        :type ui_name: str

        :returns: None
        """
        try:
            mo = importlib.reload(self.modules[ui_name])
            nt = self.modules[ui_name].UI(self)
            # dictionary entry
            mod = {ui_name: mo}
            ntd = {ui_name: nt}
            self.uis.update(ntd)
            self.modules.update(mod)
        except Exception as e:
            self.display(' Error reloading UIs ' + ui_name)
            self.display(e)
        finally:
            pass

    def reload_all_uis(self, ui_names):
        """
        Dynamically reload all UIs

        :param ui_names: list of ui names
        :type ui_names: [str]

        :returns: None
        """
        try:
            for g in ui_names:
                self.reload_ui(g)
            self.display('All UIs reloaded successfully')
        except Exception as e:
            self.display('Error reloading all UIs')
            self.display(e)
        finally:
            pass
