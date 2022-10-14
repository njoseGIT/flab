# Flab
# Version 2.0.2
# Published 17-Jul-2022
# Distributed under GNU GPL v3
# Author: Nicholas Jose

"""
The Flab module contains the Flab and FlabNamespace classes, which are used for sharing of attributes,
methods, variables and other objects
"""

from flab import TaskManager, UiManager, DeviceManager
import time
import os
import sys
import inspect


class Flab(DeviceManager.DeviceManager, TaskManager.TaskManager, UiManager.UiManager):
    """Flab inherits DeviceManager, TaskManager, UiManager and BotManager and contains dictionaries for
     devices, tasks, vars, uis and bots.
     Version 2.0.2
    """
    version = '2.0.2'

    def __init__(self, ui_queue=None, flab_queue=None, print_status=True):
        """
        Constructs the Flab object, containing empty dictionaries

        Flab objects can be constructed with two queues for exchanging information between processes.

        :param ui_queue: queue object that passes information to UI processes, defaults to None
        :type ui_queue: multiprocessing.Queue(,queue.Queue)

        :param flab_queue: queue object that passes information to flab processes, defaults to None
        :type flab_queue: multiprocessing.Queue(,queue.Queue)

        :param print_status: a boolean indicating if output should be sent to the command prompt, defaults to True

        :returns: None
        """

        super().__init__()
        self.ui_queue = ui_queue
        self.flab_queue = flab_queue
        self.devices = {}  # device dictionary
        self.tasks = {}  # task dictionary
        self.vars = {}  # variable dictionary
        self.uis = {}  # UI dictionary
        self.bots = {}  # bot dictionary
        self.print_status = print_status  # True if outputs are to be displayed through the python console
        self.is_running = True  # True if flab has been initiated within a running program
        self.modules = {}  # module dictionary

    def add_var(self, value, variable_name) -> None:
        """adds a variable with a given value to the variable dictionary

        :param value: value of the variable
        :type value: numbers, strings, lists, objects, etc.

        :param variable_name: the name of the variable
        :type variable_name: str

        :return: None

        Do not use devices, tasks, bots or uis in the variable dictionary.
        Avoid nested dictionaries and complex objects.

        """

        try:
            self.vars[variable_name] = value
        except Exception as e:
            self.flab.display('Error when adding to variable dictionary')
            self.flab.display(e)
            # raise Exception('Error in Flab.add_var')
        finally:
            pass

    def display(self, object) -> None:
        """
        Displays an object by printing to the command prompt and/or passing to ui_queue

        :param object: an object

        :returns: None
        """
        try:
            if self.print_status:
                print(object)
            if self.ui_queue is not None:
                self.ui_queue.put(object)
        except Exception as e:
            if self.print_status:
                print('Error in Flab.display')
                print(e)
            if self.ui_queue is not None:
                self.ui_queue.put('Error in Flab.display')
                self.ui_queue.put(e)
        finally:
            pass

    #
    def message(self, text) -> None:
        """
        Displays a message. For example, message('HelloWorld') leads to the
        display of "message: Hello World"

        :param text: whatever you want to send a message about
        :type text: str

        :returns: None
        """

        try:
            s = 'message: ' + text
            self.display(s)
        except Exception as e:
            self.display('Error in Flab.message')
            self.display(e)
        finally:
            pass

    # Actions to take when closing flab
    def close_flab(self) -> None:
        """
        Ends all running processes and tasks within a Flab object

        :return: None
        """
        try:
            # stop all running tasks
            self.display('stopping running tasks')
            self.stop_all_tasks()
            while self.get_running_task_names():
                time.sleep(1)
            self.is_running = False
            if self.flab_queue is not None:
                self.display('closing flab process')
                self.flab_queue.put('close')
            if self.ui_queue is not None:
                self.display('closing ui process')
                self.ui_queue.put('close')
        except Exception as e:
            self.display('Error in Flab.close_flab')
            self.display(e)
        finally:
            return 0

    def close_queues(self) -> None:
        """
        Closes any open queues

        :return: None
        """
        try:
            if self.ui_queue is not None:
                self.ui_queue.close()
            if self.flab_queue is not None:
                self.flab_queue.close()
        except Exception as e:
            self.display('Error in Flab.close_queues')
            self.display(e)
        finally:
            pass

    def create_project_directory(self, parent_path, project_name) -> None:
        """

        Creates a project directory with a given name at a given parent path

        For example, create_project_directory('C:/Projects','MyFirstProject') yields a directory
        with the following structure.

        C:/Projects/

        └ MyFirstProject/

         ├ Boot/

         ├ Tasks/

         ├ Devices/

         │ ├ Drivers/

         │ └ Protocols/

         ├ UIs/

         │ ├ Actions/

         │ ├ Designs/

         │ └ Windows/

         └ Bots/

            └ Algorithms/


        :param parent_path: full path of the parent directory (typically Projects)
        :type parent_path: str

        :param project_name: Name of the project
        :type project_name: str

        :return: None
        """

        try:
            project_dir = parent_path + '/' + project_name
            device_dir = project_dir + '/' + 'Devices'
            ui_dir = project_dir + '/' + 'UIs'
            bot_dir = project_dir + '/' + 'Bots'
            os.mkdir(project_dir)

            def add_directory(path, name):
                os.mkdir(path + '/' + name)

            add_directory(project_dir, 'Boot')
            add_directory(project_dir, 'Devices')
            add_directory(device_dir, 'Drivers')
            add_directory(device_dir, 'Protocols')
            add_directory(project_dir, 'Tasks')
            add_directory(project_dir, 'UIs')
            add_directory(ui_dir, 'Actions')
            add_directory(ui_dir, 'Designs')
            add_directory(bot_dir, 'Algorithms')

        except Exception as e:
            self.display('Error in Flab.create_project_directory')
            self.display(e)

        finally:
            pass

    def set_working_directory(self, project_path):
        """

        Sets the current working directory to a given path

        :param project_path: the full path
        :type project_path: str

        :return: None
        """
        try:
            os.chdir(project_path)
            cwd = os.getcwd()
            par1 = os.path.abspath(os.path.join(cwd, '..'))
            par2 = os.path.abspath(os.path.join(par1, '..'))
            sys.path.append(par2)
        except Exception as e:
            self.display('Error in Flab.set_working_directory')
            self.display(e)
        finally:
            pass

    def get_namespace(self):
        """
        returns a representation of the Flab object's attributes and contained devices, tasks, etc.

        :return: FlabNamespace
        """
        try:
            namespace = FlabNamespace()
            namespace.devices = self.devices.keys()
            namespace.tasks = self.tasks.keys()
            namespace.bots = self.bots.keys()
            namespace.vars = self.vars.copy()
            namespace.modules = self.modules.keys()
            namespace.uis = self.uis.keys()
            namespace.print_status = self.print_status
            namespace.is_running = self.is_running
            namespace.running_tasks = self.get_running_task_names()

            # getting task arguments and descriptions
            namespace.task_args = {}
            namespace.task_arg_descriptions = {}
            for task_name in namespace.tasks:
                namespace.task_args[task_name] = inspect.getfullargspec(self.tasks[task_name].run)
                full_args = namespace.task_args[task_name]
                if len(full_args) > 1:
                    args_list = full_args.args[1:]
                    arg_list = []
                    opt_arg_list = []
                    for a in args_list:
                        if 'argument_descriptions' in dir(self.tasks[task_name]):
                            namespace.task_arg_descriptions[task_name] = {}
                            namespace.task_arg_descriptions[task_name] = self.tasks[task_name].argument_descriptions

            # getting device attributes, methods, arguments, descriptions
            namespace.device_attributes = {}
            namespace.device_methods = {}
            namespace.device_method_args = {}
            namespace.device_method_arg_descriptions = {}

            if len(namespace.devices) > 0:
                for i in namespace.devices:
                    attribute_list = self.devices[i].list_attributes()
                    method_list = self.devices[i].list_methods()
                    namespace.device_attributes[i] = attribute_list
                    namespace.device_methods[i] = method_list

                # getting the arguments and argument descriptions for each device method
                for device_name in namespace.devices:
                    namespace.device_method_args[device_name] = {}
                    namespace.device_method_arg_descriptions[device_name] = {}
                    for method_name in namespace.device_methods[device_name]:
                        full_args = self.devices[device_name].list_method_args(method_name)
                        args_list = full_args.args[1:]
                        namespace.device_method_args[device_name][method_name] = args_list
                        namespace.device_method_arg_descriptions[device_name][method_name] = {}
                        if 'argument_descriptions' in dir(self.devices[device_name]):
                            for arg in args_list:
                                namespace.device_method_arg_descriptions[device_name][method_name][arg] \
                                    = self.devices[device_name].argument_descriptions[arg]
                        else:
                            for arg in args_list:
                                namespace.device_method_arg_descriptions[device_name][method_name][arg] = str(arg)
        except Exception as e:
            if self.print_status:
                print('Error in Flab.get_namespace')
                print(e)
            namespace = None
        finally:
            return namespace


class FlabNamespace:
    """
    A namespace for a Flab object which contains the information on the contained objects (e.g. Devices, Tasks,
    variables)
    """

    def __init__(self) -> None:
        """
        The constructor defines the namespace attributes with the following code:
        ::

            self.devices = []
            self.tasks = []
            self.bots = []
            self.vars = []
            self.modules = []
            self.uis = []
            self.print_status = []
            self.is_running = []
            self.running_tasks = []
            self.device_attributes = {}
            self.device_methods = {}
            self.device_method_args = {}
            self.device_method_arg_descriptions = {}

        """

        self.devices = []
        self.tasks = []
        self.bots = []
        self.vars = []
        self.modules = []
        self.uis = []
        self.print_status = []
        self.is_running = []
        self.running_tasks = []
        self.device_attributes = {}
        self.device_methods = {}
        self.device_method_args = {}
        self.device_method_arg_descriptions = {}
