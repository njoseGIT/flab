#Flab
#Version 1.1.1
#Published 11-April-2022
#Distributed under GNU GPL v3
#Author: Nicholas A. Jose

from flab import TaskManager, UiManager, DeviceManager
import time
import os
import sys

class Flab(DeviceManager.DeviceManager, TaskManager.TaskManager, UiManager.UiManager):

    #Flab inherits methods from DeviceManager, TaskManager and UiManager libraries
    description = 'The Flab space for shared devices, tasks and user interfaces (UIs)'
    version = '1.1.1'
    devices = {} #device dictionary
    tasks = {}  #task dictionary
    vars = {} #variable dictionary
    modules = {} #module dictionary
    uis = {} #UI dictionary
    print_status = False #True if outputs are to be displayed through the python console
    is_running = False #True if flab has been initiated within a running program

    #Flab objects are initialized with two queues for exchanging information between processes.
    #ui_queue passes objects to UI processes
    #flab_queue passes objects to Flab processes
    #flab_proxy is a proxy object for sharing flab across multiple processes by the boot manager
    def __init__(self, ui_queue, flab_queue):
        self.ui_queue = ui_queue
        self.flab_queue = flab_queue
        self.is_running = True

    #Add a variable (object v) with name (string variable_name) into flab
    def add_var(self,v , variable_name):
        self.vars[variable_name]= v

    #Pass an object to the ui and print within the python console
    def display(self, s):
        try:
            if self.print_status:
                print(s)
            self.ui_queue.put(s)
        except Exception as e:
            if self.print_status:
                print('Error displaying object')
                print(e)
            self.ui_queue.put('Error displaying object')
            self.ui_queue.put(e)
        finally:
            pass

    #Pass a message (string message) to the ui and print within the python console
    def message(self, message):
        try:
            s = 'message: ' + message
            self.display(s)
        except Exception as e:
            self.display('Error passing message')
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
            print('closing flab process')
            self.flab_queue.put('close')
            print('closing ui process')
            self.ui_queue.put('close')
        except Exception as e:
            self.display('error in closing')
            self.display(e)
        finally:
            return 0

    #Closing of queues
    def close_queues(self):
        self.ui_queue.close()
        self.flab_queue.close()

    #creates a project directory with a given name at a given parent path
    def create_project_directory(self, parent_path, project_name):

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

    def set_working_directory(self,project_path):
        try:
            os.chdir(project_path)
            cwd = os.getcwd()
            par1 = os.path.abspath(os.path.join(cwd, '..'))
            par2 = os.path.abspath(os.path.join(par1, '..'))
            sys.path.append(par2)
        except Exception as e:
            print('Error in setting up project directory')
            print(e)
        finally:
            pass


