#Flab
#Version 2.0.1
#Published 17-Jul-2022
#Distributed under GNU GPL v3
#Author: Nicholas Jose

from flab import TaskManager, UiManager, DeviceManager
import time
import os
import sys
import inspect

class Flab(DeviceManager.DeviceManager, TaskManager.TaskManager, UiManager.UiManager):

    #Flab inherits methods from DeviceManager, TaskManager, UiManager and BotManager libraries
    #Flab objects can be initialized with two queues for exchanging information between processes.
    #ui_queue passes objects to UI processes
    #flab_queue passes objects to Flab processes
    #FlabNamespace is a namespace class for sharing the names of flab attributes, methods and variables

    description = 'The Flab object for shared devices, tasks and user interfaces (UIs)'
    version = '2.0.1'
    modules = {}  # module dictionary

    def __init__(self, ui_queue = None, flab_queue = None, print_status = True):
        self.ui_queue = ui_queue
        self.flab_queue = flab_queue
        self.devices = {}  # device dictionary
        self.tasks = {}  # task dictionary
        self.vars = {}  # variable dictionary
        self.uis = {}  # UI dictionary
        self.bots = {}  # bot dictionary
        self.print_status = print_status  # True if outputs are to be displayed through the python console
        self.is_running = True # True if flab has been initiated within a running program

    #Add a variable (object v) with name (string variable_name) into flab
    def add_var(self,v, variable_name):
        try:
            self.vars[variable_name]= v
        except Exception as e:
            if self.print_status:
                print('Error in Flab.add_var')
                print(e)
        finally:
            pass

    #Pass an object to the ui and print within the python console
    def display(self, s):
        try:
            if self.print_status:
                print(s)
            if self.ui_queue != None:
                self.ui_queue.put(s)
        except Exception as e:
            if self.print_status:
                print('Error in Flab.display')
                print(e)
            if self.ui_queue != None:
                self.ui_queue.put('Error in Flab.display')
                self.ui_queue.put(e)
        finally:
            pass

    #Pass a message (string message) to the ui and print within the python console
    def message(self, message):
        try:
            s = 'message: ' + message
            self.display(s)
        except Exception as e:
            self.display('Error in Flab.message')
            self.display(e)
        finally:
            pass

    #Actions to take when closing flab
    def close_flab(self):
        try:
            #stop all running tasks
            print('stopping running tasks')
            self.stop_all_tasks()
            while self.get_running_task_names() != []:
                time.sleep(1)
            self.is_running = False
            if self.flab_queue != None:
                print('closing flab process')
                self.flab_queue.put('close')
            if self.ui_queue != None:
                print('closing ui process')
                self.ui_queue.put('close')
        except Exception as e:
            self.display('Error in Flab.close_flab')
            self.display(e)
        finally:
            return 0

    #Closing of queues
    def close_queues(self):
        try:
            if self.ui_queue != None:
                self.ui_queue.close()
            if self.flab_queue != None:
                self.flab_queue.close()
        except Exception as e:
            if self.print_status:
                print('Error in Flab.close_queues')
                print(e)
        finally:
            pass

    #creates a project directory with a given name at a given parent path
    def create_project_directory(self, parent_path, project_name):
        try:
            project_dir = parent_path + '/' + project_name
            device_dir = project_dir + '/' + 'Devices'
            ui_dir = project_dir + '/' + 'UIs'
            os.mkdir(project_dir)
            def add_directory(parent_path, name):
                os.mkdir(parent_path + '/' + name)
            add_directory(project_dir, 'Boot')
            add_directory(project_dir, 'Devices')
            add_directory(device_dir, 'Drivers')
            add_directory(device_dir, 'Protocols')
            add_directory(project_dir, 'Tasks')
            add_directory(project_dir, 'UIs')
            add_directory(ui_dir, 'Actions')
            add_directory(ui_dir, 'Designs')
        except Exception as e:
            if self.print_status:
                print('Error in Flab.create_project_directory')
                print(e)
        finally:
            pass

    #sets the current working directory
    def set_working_directory(self,project_path):
        try:
            os.chdir(project_path)
            cwd = os.getcwd()
            par1 = os.path.abspath(os.path.join(cwd, '..'))
            par2 = os.path.abspath(os.path.join(par1, '..'))
            sys.path.append(par2)
        except Exception as e:
            print('Error in Flab.set_working_directory')
            print(e)
        finally:
            pass

    #return the namespace representation of a Flab object
    def get_namespace(self):
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

            #getting task arguments and descriptions
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

            #getting device attributes, methods, arguments, descriptions
            namespace.device_attributes = {}
            namespace.device_methods = {}
            namespace.device_method_args = {}
            namespace.device_method_arg_descriptions = {}

            if len(namespace.devices)>0:
                for i in namespace.devices:
                    attribute_list = self.devices[i].list_attributes()
                    method_list = self.devices[i].list_methods()
                    namespace.device_attributes[i] = attribute_list
                    namespace.device_methods[i] = method_list

            #getting the arguments and argument descriptions for each device method
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
                                namespace.device_method_arg_descriptions[device_name][method_name][arg] = self.devices[device_name].argument_descriptions[arg]
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

#A custom namespace for flab - this contains basic information on flab items, useful for remote communication
class FlabNamespace():
    def __init__(self):
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
