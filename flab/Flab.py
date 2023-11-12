# Flab 3
# Distributed under GNU GPL v3
# Author: Nicholas Jose

"""
The Flab module contains the Flab and FlabNamespace classes, which are used for sharing of attributes,
methods, variables and other objects
"""

from flab import TaskManager, UiManager, DeviceManager, DataManager, EnvironmentManager, ModelManager
from multiprocessing.managers import NamespaceProxy, SyncManager, BaseProxy
import importlib
import time
import os
import sys
import inspect
import glob
import threading

class FlabObjectManager(SyncManager):
    """A manager class for sharing generic flab objects and across threads and processes.
    Extends the multiprocessing class SyncManager
    """
    pass

class Flab(DeviceManager.DeviceManager,
           TaskManager.TaskManager,
           UiManager.UiManager,
           DataManager.DataManager,
           EnvironmentManager.EnvironmentManager,
           ModelManager.ModelManager):
    """Flab inherits DeviceManager, TaskManager, UiManager, DataManager, EnvironmentManager and ModelManager, and contains dictionaries for
     devices, tasks, vars, uis, data and models.
    """
    version = '3.0.0' # version
    modules = {}  # module dictionary
    flab_object_manager = FlabObjectManager() # the object manager synchronizes objects like ui's, tasks, devices, etc.

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

        self.ui_queue = ui_queue # message queue to ui processes
        self.flab_queue = flab_queue # message queue to machine processes
        self.devices = {}  # device dictionary
        self.tasks = {}  # task dictionary
        self.vars = {}  # variable dictionary
        self.uis = {}  # UI dictionary
        self.bots = {}  # bot dictionary
        self.data = {} # data dictionary
        self.models = {} # model dictionary
        self.print_status = print_status  # True if outputs are to be displayed through the python console
        self.is_running = True  # True if flab has been initiated within a running program
        self.restart = False # True if running program is to be restarted
        self.project_path = 'NA' # path to project directory

    def set_project_path(self, project_path) -> None:
        """
        sets the current project path

        :param project_path: project path
        :type project_path: str

        :return: None
        """
        self.project_path = project_path

    def register_proxy(self) -> None:
        """
        Registers a proxy class within a project with the FlabObjectManager

        :returns: None
        """
        try:
            self.flab_object_manager.register('proxy', Proxy)
            self.display('Proxy successfully registered')

        except Exception as e:
            self.display('Error in register_proxy')
            self.display(e)

        finally:
            pass

    def start_object_manager(self) -> None:
        """
        Starts the FlabObjectManager

        :returns: None
        """
        try:
            self.flab_object_manager.start()

        except Exception as e:
            self.display('Error in start_object_manager')
            self.display(e)

        finally:
            pass

    def load_object(self, object_name, object_path, object_type, object_type_dict, object_class_name) -> None:
        """
        Generic method for loading objects

        :param object_name: Name of the object.
        :type object_name: str

        :param object_path: Relative project directory path to object
        :type object_path: str

        :param object_type: Object type (device, task, ui, data)
        :type object_type: str

        :param object_type_dict: Object dictionary name (devices, tasks, uis, data)
        :type object_type_dict: str

        :param object_class_name: Object class name (Device, Task, Ui, Data)
        :type object_class_name: str
        """
        load_error = ''
        try:
            #update module
            module_name = 'Projects.' + os.path.split(os.getcwd())[1] + object_path + object_name
            object_module = importlib.import_module(module_name)
            self.modules.update({object_name: object_module})

            #create object
            create_method = getattr(self.flab_object_manager, 'proxy')
            new_object = eval('create_method(object_module.'+object_class_name+'(),"'+object_class_name+'")')
            new_object.set_flab(self)

            #dictionary entry
            eval('self.' + object_type_dict + '.update({object_name: new_object})')
            self.display("Successfully loaded : " + object_name)

        except Exception as e:
            self.display('Error loading ' + object_type + ' ' + object_name)
            self.display(e)
        finally:
            pass

    def load_objects(self, object_names, object_path, object_type, object_type_dict, object_class_name) -> str:
        """
        load a list of objects into flab from a directory, defined by their names in a list (object_names)

        :param object_names: list of the object names
        :type object_names: [str]

        :param object_path: Relative project directory path to object
        :type object_path: str

        :param object_type: Object type (device, task, ui, data)
        :type object_type: str

        :param object_type_dict: Object dictionary name (devices, tasks, uis, data)
        :type object_type_dict: str

        :param object_class_name: Object class name (Device, Task, Ui, Data)
        :type object_class_name: str

        :returns: None
        """
        load_error = ''
        try:
            for object_name in object_names:
                self.load_object(object_name, object_path, object_type, object_type_dict, object_class_name)
            if load_error == '':
                self.display('All ' + object_type_dict + ' loaded successfully.')
        except Exception as e:
            self.display('Error in loading all ' + object_type_dict)
            self.display(e)
        finally:
            return load_error

    def load_all_objects(self, object_path, object_type, object_type_dict, object_class_name) -> None:
        """
        load every object present in the current project's object folder

        :param object_path: Relative project directory path to object
        :type object_path: str

        :param object_type: Object type (device, task, ui, data)
        :type object_type: str

        :param object_type_dict: Object dictionary name (devices, tasks, uis, data)
        :type object_type_dict: str

        :param object_class_name: Object class name (Device, Task, Ui, Data)
        :type object_class_name: str

        :returns: None
        """
        try:
            cwd = os.getcwd()
            objects = glob.glob(cwd + object_path + '*.py')
            object_names = []
            for o in objects:
                object_names.append(o[len(cwd + object_path):].replace('.py', ''))
            self.load_objects(sorted(object_names),object_path.replace('/','.'), object_type, object_type_dict, object_class_name)
        except Exception as e:
            self.display('Error in loading all ' + object_type_dict)
            self.display(e)
        finally:
            pass

    def reload_object(self, object_name, object_type_dict, object_type, object_class_name) -> None:
        """
        reload a single object into a flab object

        :param object_name: name of the object
        :type object_name: str

        :param object_type_dict: Object dictionary name (devices, tasks, uis, data)
        :type object_type_dict: str

        :param object_class_name: Object class name (Device, Task, Ui, Data)
        :type object_class_name: str

        :returns: None
        """
        try:
            # module update
            object_module = importlib.reload(self.modules[object_name])
            self.modules.update({object_name: object_module})

            # create new object
            create_method = getattr(self.flab_object_manager, 'proxy')
            new_object = eval('create_method(object_module.'+object_class_name+'(),"'+object_class_name+'")')
            new_object.set_flab(self)

            # dictionary entry
            object_entry = {object_name: new_object}
            self.__getattribute__(object_type_dict).update(object_entry)
            self.display(object_name + ' reloaded successfully')

        except Exception as e:
            self.display('Error reloading ' + object_name)
            self.display(e)

        finally:
            pass

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
            self.display('Successfully added variable ' + variable_name)
        except Exception as e:
            self.flab.display('Error when adding to variable dictionary')
            self.flab.display(e)
        finally:
            pass

    def display(self, object) -> None:
        """
        Displays an object by printing it out via the terminal/command prompt and/or passing to ui_queue

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

    def close_project(self) -> None:
        """
        Ends all running processes, tasks and deletes objects within a Flab object

        :return: None
        """

        #lock = threading.Lock()
        #lock.acquire()

        # stop all running tasks
        self.display('killing running tasks')
        self.kill_all_tasks()

        time.sleep(1)
        self.stop_asyncio_loop()

        #self.stop_all_tasks()
        while self.get_running_task_names():
            time.sleep(0.1)

        self.display('Clearing flab')

        self.devices = {}
        self.tasks = {}
        self.uis = {}
        self.variables = {}
        self.data = {}
        self.models = {}
        self.ui_queue.put('list_objects()')

        #lock.release()

    def close_flab(self) -> None:
        """
        Ends all running processes and tasks within a Flab object

        :return: None
        """
        try:
            lock = threading.Lock()
            lock.acquire()
            # stop all running tasks
            self.kill_all_tasks()
            self.display('stopping running tasks')
            self.stop_asyncio_loop()
            #self.stop_all_tasks()
            while self.get_running_task_names():
                time.sleep(1)
            lock.release()
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

         ├ UIs/

         ├ Data/

         └ Models/

        :param parent_path: full path of the parent directory (typically Projects)
        :type parent_path: str

        :param project_name: Name of the project
        :type project_name: str

        :return: None
        """

        try:
            project_dir = parent_path + '/' + project_name
            os.mkdir(project_dir)

            def add_directory(path, name):
                os.mkdir(path + '/' + name)

            add_directory(project_dir, 'Boot')
            add_directory(project_dir, 'Devices')
            add_directory(project_dir, 'Tasks')
            add_directory(project_dir, 'UIs')
            add_directory(project_dir, 'Data')
            add_directory(project_dir, 'Models')

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
            namespace.vars = self.vars.copy()
            namespace.data = self.data.keys()
            namespace.modules = self.modules.keys()
            namespace.uis = self.uis.keys()
            namespace.models = self.models.keys()
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

            #getting data attributes
            namespace.data_attributes = {}
            if len(namespace.data) > 0:
                for i in namespace.data:
                    attribute_list = self.data[i].list_attributes()
                    namespace.data_attributes[i] = attribute_list

        except Exception as e:
            if self.print_status:
                print('Error in Flab.get_namespace')
                print(e)
            namespace = None

        finally:
            return namespace

class Proxy(NamespaceProxy):

    def __new__(cls, alternate_obj, class_name):
        new_module = importlib.reload(inspect.getmodule(alternate_obj))
        obj = object.__new__(new_module.__dict__[class_name])
        obj.__dict__ = alternate_obj.__dict__
        return obj

    def __init__(self):
        pass

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
        self.vars = []
        self.modules = []
        self.uis = []
        self.data = []
        self.models = []
        self.data_attributes = []
        self.print_status = []
        self.is_running = []
        self.running_tasks = []
        self.device_attributes = {}
        self.device_methods = {}
        self.device_method_args = {}
        self.device_method_arg_descriptions = {}
