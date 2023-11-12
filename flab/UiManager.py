# Flab 3
# UiManager.py
# Distributed under GNU GPL v3
# Author: Nicholas Jose

"""The UiManager module contains class and methods for creating, loading and converting UIs"""

import importlib
import glob
from flab.Templates import TaskTemplate

class UiManager:
    """
    A class containing methods for converting and loading UIs. Note: PyQT interfaces generally need to bed
    be started within a main method or separate process
    """

    uis = {}
    load_all_uis_completed = False

    def __init__(self):
        pass

    def load_ui(self, ui_name):
        """
        Loads a predefined UI from the UI folder into a flab object

        :param ui_name: name of the ui

        :type ui_name: str
        :return: None
        """
        try:
            self.load_object(ui_name,'.UIs.', 'ui', 'uis', 'Ui')

        except Exception as e:
            self.display('Error in loading Ui: ' + ui_name)
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
            for g in uis:
                ui_names.append(g[4:].replace('.py', ''))
            self.load_uis(ui_names)

        except Exception as e:
            self.display('Error loading all UIs')
            self.display(e)

        finally:
            self.load_all_uis_completed = True

    def reload_ui(self, ui_name):
        """
        Dynamically reload a UI

        :param ui_name: name of UI
        :type ui_name: str

        :returns: None
        """

        try:
            ui_module = importlib.reload(self.modules[ui_name])
            self.modules.update({ui_name: ui_module})
            self.uis.pop(ui_name)
            self.load_ui(ui_name)

        except Exception as e:
            self.display(' Error reloading UI ' + ui_name)
            self.display(e)

        finally:
            pass

    def reload_all_uis(self, ui_names):
        """
        Reload all UIs

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

    def start_ui(self, ui_name):
        """
        Starts a UI

        :param ui_name: the name of the ui
        :type ui_name: str
        """

        try:
            if 'UiTask_' + ui_name not in self.tasks:
                ui_task = UiTask(ui_name)
                ui_task.set_flab(self)
                self.tasks.update({'UiTask_' + ui_name: ui_task})
            self.start_task('UiTask_' + ui_name)

        except Exception as e:
            self.display('Error in starting UI: ' + ui_name)
            self.display(e)

        finally:
            pass

    def stop_ui(self, ui_name):
        """
        Stops a UI

        :param ui_name: the name of the ui
        :type ui_name: str
        """

        try:
            if 'UiTask_' + ui_name not in self.tasks:
                ui_task = UiTask(ui_name)
                ui_task.set_flab(self)
                self.tasks.update({'UiTask_' + ui_name: ui_task})
            self.stop_task('UiTask_' + ui_name)
            self.uis[ui_name].stop()

        except Exception as e:
            self.display('Error in starting UI: ' + ui_name)
            self.display(e)

        finally:
            pass

    def get_running_ui_names(self):
        """
        gets the names of the UIs that are currently running

        :return: list of strings
        """
        running_uis = []
        try:
            running_tasks = self.get_running_task_names()
            for t in running_tasks:
                if 'UiTask' in t:
                    ui_name = t.replace('RUN_UiTask_','')
                    running_uis.append(ui_name)

        except Exception as e:
            self.display('Error in getting running uis')
            self.display(e)

        finally:
            return sorted(running_uis)


class UiTask(TaskTemplate.Task):
    """
    A dedicated Task class for Uis
    """

    task_name = 'UiTask'
    task_type = 'process'
    task_stopped = False

    def __init__(self, ui_name):
        self.task_name = self.task_name + '_' + ui_name
        self.ui_name = ui_name

    def run(self):
        """
        starts the ui
        """
        try:
            run_method = self.flab.uis[self.ui_name].get('run')
            run_method()

        except Exception as e:
            self.flab.display('Error in running ui - ' + self.ui_name)
            self.flab.display(str(e))

        finally:
            pass

    def stop(self):
        """
        stops the UI

        :return: None
        """
        try:
            stop_method = self.flab.uis[self.ui_name].get('stop')
            stop_method()

        except Exception as e:
            self.flab.display('Error in stopping ui - ' + self.ui_name)
            self.flab.display(str(e))

        finally:
            pass


