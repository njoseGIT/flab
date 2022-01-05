#BootManager
#Version 0.0.4
#Published 1-January-2021
#Distributed under GNU GPL v3
#Author: Nicholas Jose

from flab import Flab
from multiprocessing import Process
from multiprocessing.managers import NamespaceProxy, SyncManager
import types
import os

#A class for managing the booting of flab, specifically using the multiprocessing library
class BootManager():

    version = '0.0.4'
    processes = {}
    managers = {}

    #create the basic flab manager, queue manager and shared flab and queue
    def __init__(self):
        FlabManager.register('Flab', Flab.Flab, FlabProxy)
        self.flab_manager = FlabManager()
        self.queue_manager = SyncManager()
        self.flab_manager.start()
        self.queue_manager.start()

    def create_queue(self):
        return self.queue_manager.Queue()

    def create_flab_proxy(self, out_queue, in_queue):
        flab_proxy = self.flab_manager.Flab(out_queue, in_queue) # flab namespace
        flab_proxy.tasks = self.flab_manager.dict() # tasks dictionary
        flab_proxy.devices = self.flab_manager.dict()  # device dictionary
        flab_proxy.vars = self.flab_manager.dict()  # variable dictionary
        flab_proxy.uis = self.flab_manager.dict()  # GUI dictionary
        return flab_proxy

    def start_process(self, flab, task_name, *args, blocking=False):
        process_class = flab.tasks[task_name]
        process = Process(target=process_class.run, args=args)
        process.start()
        if blocking:
            process.join()
        return process

    # args is a multidimensional tuple, where each element consists of the process arguments
    def start_processes(self, flab, task_names, *args, blocking=False):
        procs = {}
        index = 0
        for t in task_names:
            process_class = flab.tasks[t]
            process = Process(target=process_class.run, args=args[index])
            process.start()
            procs.update({t: process})
            index = index + 1
        if blocking:
            for p in procs:
                procs[p].join()
        return procs

    #shuts down sync managers
    def shutdown(self):
        self.queue_manager.shutdown()
        self.flab_manager.shutdown()

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


#A proxy class for sharing flab

class FlabProxy(NamespaceProxy):
    _exposed_ = tuple(dir(Flab.Flab))

    def __getattr__(self, name):
        result = super().__getattr__(name)
        if isinstance(result, types.MethodType):
            def wrapper(*args, **kwargs):
                return self._callmethod(name, args)  # Note the return here
            return wrapper
        return result


class FlabManager(SyncManager):
    pass

