# Flab
# TaskManager
# Version 2.0.2
# Published XX-XXX-XXXX
# Distributed under GNU GPL v3
# Author: Nicholas Jose
# Update: No longer contains Qthread capabilities to remove dependency on PyQt

"""The TaskManager module includes classes and methods for creating and running synchronous/simultaneous routines"""

import glob
import threading
import sys
import os
import asyncio
import importlib
from multiprocessing import Process


class TaskManager:
    """
    The TaskManager class contains methods for loading, running and terminating tasks implementing python\'s threading
    library, asyncio, and multiprocessing
    Version 2.0.2
    """

    version = '2.0.2'

    def __init__(self):
        self.tasks = {}  # dictionary of loaded tasks
        self.running_tasks = {}  # dictionary of running tasks (i.e. instances of threads)
        self.load_all_tasks_completed = False

    def load_task(self, task_name):
        """
        load a single task into flab. The task name is given by the filename, without the '.py' at the end

        :param task_name: the task's name
        :type: str

        :returns: None
        """
        load_err = ''
        try:
            module_name = 'Projects.' + os.path.split(os.getcwd())[1] + '.Tasks.' + task_name
            mo = importlib.import_module(module_name)
            nt = mo.Task(self)

            # dictionary entry
            mod = {task_name: mo}
            ntd = {task_name: nt}
            self.tasks.update(ntd)
            self.modules.update(mod)
        except Exception as e:
            load_err = load_err + 'Error loading task ' + task_name + '.'
            self.display(load_err)
            self.display(e)
        if load_err == '':
            self.display(task_name + ' loaded successfully.')
        return load_err

    def load_tasks(self, task_names):
        """
        load a list of tasks into flab. task_names is an array of the task names (string)

        :param task_names: list of the task names
        :type task_names: [str]

        :returns: None
        """
        load_err = ''
        for ta in task_names:
            ta_err = self.load_task(ta)
            load_err = load_err + ta_err
        if load_err == '':
            self.display('All tasks loaded successfully.')
        return load_err

    def load_all_tasks(self):
        """
        load every task present in the current project's Tasks folder

        :returns: None
        """
        try:
            cwd = os.getcwd()
            tasks = glob.glob(cwd + '/Tasks/*.py')
            task_names = []
            for t in tasks:
                task_names.append(t[len(cwd + '/Tasks/'):].replace('.py', ''))
            self.load_tasks(sorted(task_names))
        except Exception as e:
            self.display(e)
            self.display('Error in loading tasks')
        finally:
            self.load_all_tasks_completed = True

    def reload_task(self, task_name):
        """
        reload a single task into a flab object

        :param task_name: name of the task
        :type task_name: str

        :returns: None
        """
        reload_err = ''
        try:
            mo = importlib.reload(self.modules[task_name])
            nt = self.modules[task_name].Task(self)
            # dictionary entry
            mod = {task_name: mo}
            ntd = {task_name: nt}
            self.tasks.update(ntd)
            self.modules.update(mod)
        except Exception as e:
            reload_err = reload_err + ' Error reloading task ' + task_name + '.'
            self.display(reload_err)
            self.display(e)
        finally:
            pass
        if reload_err == '':
            self.display(task_name + ' reloaded successfully')
        return reload_err

    def reload_tasks(self, task_names):
        """
        reload multiple tasks

        :param task_names: names of tasks in a list
        :type task_names: [str]

        :returns: None
        """
        reload_err = ''
        for ta in task_names:
            err = self.reload_task(ta)
            reload_err = reload_err + err
        if reload_err == '':
            self.display('All Tasks reloaded successfully')
        return reload_err

    def start_task(self, task_name, *args, **kwargs):
        """
        start a task using the "run" method. By default this runs each task as a thread, but if the task type is
        specified otherwise, it will start the task as an asyncio thread or a process

        :param task_name: name of the task
        :type task_name: str

        :param args: arguments for the task

        :param kwargs: keyword arguments for the task

        :returns: None
        """
        try:
            task = self.tasks[task_name]
            if hasattr(task, 'task_type'):
                if task.task_type == 'thread':
                    self.start_thread(task_name, *args, **kwargs)
                elif task.task_type == 'asyncio':
                    self.start_asyncio_task(task_name, *args, **kwargs)
                elif task.task_type == 'process':
                    self.start_process(task_name, *args, **kwargs)
                else:
                    self.display(task_name + ' task type ' + task.task_type + ' not recognized')
            else:
                self.start_thread(task_name, *args, **kwargs)
        except Exception as e:
            self.display('Error in starting task ' + task_name)
            self.display(e)
        finally:
            pass

    def load_start_task(self, task_name, *args, **kwargs):
        """
        Load and start a task in one method

        :param task_name: name of the task
        :type task_name: str

        :param args: task arguments

        :param kwargs: task keyword arguments

        :returns: None
        """
        try:
            self.load_task(task_name)
            self.start_task(task_name, *args, **kwargs)
        except Exception as e:
            self.display('Error in loading and starting task ' + task_name)
            self.display(e)
        finally:
            pass

    def reload_start_task(self, task_name, *args, **kwargs):
        """
        reload and start a task in one method

        :param task_name: name of the task
        :type task_name: str

        :param args: task arguments

        :param kwargs: task keyword arguments

        :returns: None
        """
        try:
            self.reload_task(task_name)
            self.start_task(task_name, *args, **kwargs)
        except Exception as e:
            self.display('Error in loading and starting task ' + task_name)
            self.display(e)
        finally:
            pass

    def stop_task(self, task_name, *args, **kwargs):
        """
        Stop a task using the task's "stop" method. By default this runs each task as a thread, but if the task type
        is specified otherwise, it will start the task as an asyncio thread or a process.

        :param task_name: name of the task
        :type task_name: str

        :param args: arguments for the task

        :param kwargs: keyword arguments for the task

        :returns: None
        """
        try:
            task = self.tasks[task_name]
            if hasattr(task, 'task_type'):
                if task.task_type == 'thread':
                    self.stop_thread(task_name, *args, **kwargs)
                elif task.task_type == 'asyncio':
                    self.stop_asyncio_task(task_name, *args, **kwargs)
                elif task.task_type == 'process':
                    self.stop_process(task_name, *args, **kwargs)
                else:
                    self.display(task_name + ' task type ' + task.task_type + ' not recognized')
            else:
                self.stop_thread(task_name, *args, **kwargs)
        except Exception as e:
            self.display('Error in stopping task ' + task_name)
            self.display(e)
        finally:
            pass

    def stop_all_tasks(self):
        """
        this method stops all running tasks

        :returns: None
        """
        try:
            current_tasks = self.running_tasks
            temp_tasks = []
            for t in current_tasks:
                if t.__contains__('RUN_'):
                    temp_tasks.append(t)
            for t in temp_tasks:
                tt = t.replace('RUN_', '')
                self.stop_task(tt)
        except Exception as e:
            print(e)
            self.display(e)
        finally:
            pass

    def start_thread(self, task_name, *args, **kwargs):
        """
        Start a thread with the run method, with input arguments args and kwargs

        :param task_name: name of the task
        :type task_name: str

        :param args: task arguments

        :param kwargs: task keyword arguments

        :returns: None
        """
        try:
            task = self.tasks[task_name]
            thr = ThreadTrace('run', task_name, self, target=task.run, args=args, kwargs=kwargs, daemon=True)
            thr.start()
            self.running_tasks.update({'RUN_' + task_name: thr})
        except Exception as e:
            self.display('Error in starting task ' + task_name)
            self.display(e)
        finally:
            pass

    def stop_thread(self, task_name, *args, **kwargs):
        """
        Stop a thread with the stop method, with input arguments args and kwargs.

        :param task_name: name of the task
        :type task_name: str

        :param args: task arguments

        :param kwargs: task keyword arguments

        :returns: None
        """
        try:
            task = self.tasks[task_name]
            thr = ThreadTrace('stop', task_name, self, target=task.stop, args=args, kwargs=kwargs, daemon=True)
            thr.start()
            self.running_tasks.update({'STOP_' + task_name: thr})
            self.kill_thread('RUN_' + task_name)
        except Exception as e:
            self.display('Error in stopping task ' + task_name)
            self.display(e)
        finally:
            pass

    def kill_thread(self, thread_name):
        """
        directly kills a thread

        :param thread_name: name of the thread
        :type thread_name: str

        :returns: None
        """
        thr = self.running_tasks[thread_name]
        thr.kill()
        thr.join()

    def display_running_tasks(self):
        """
        Displays task instances

        :returns: None
        """
        self.display(self.running_tasks.keys())

    def display_alive_threads(self):
        """
        displays all threads that are still alive

        :returns: None
        """
        for thr in self.running_tasks:
            try:
                if self.running_tasks[thr].is_alive() is True:
                    self.display(thr)
            finally:
                pass

    def get_running_task_names(self):
        """
        Returns names of running tasks

        :returns: list of str
        """
        running_task_names = []
        for i in self.running_tasks:
            if self.running_tasks[i].is_alive() is True:
                running_task_names.append(i)
        return running_task_names

    def start_process(self, task_name, *args, blocking=False):
        """
        Start a process with the run method,  with input arguments args and kwargs

        :param task_name: name of the task
        :type task_name: str

        :param args: args for the task

        :param blocking: if the task is blocking (False by default)
        :type blocking: boolean

        :returns: None
        """
        try:
            process_class = self.tasks[task_name]
            process = Process(target=process_class.run, args=args, daemon=True)
            process.start()
            self.running_tasks.update({'RUN_' + task_name: process})
            if blocking:
                process.join()
        except Exception as e:
            self.display('Error in starting process ' + task_name)
            self.display(e)
        finally:
            pass

    def start_processes(self, task_names, *args, blocking=False):
        """
        Start multiple processes at once.

        :param task_names: name of the task
        :type task_names: [str]

        :param args: args is a multidimensional tuple, where each element consists of the process arguments

        :param blocking: if the task is blocking (False by default)
        :type blocking: boolean

        :return: None
        """
        try:
            processes = {}
            index = 0
            for t in task_names:
                process_class = self.tasks[t]
                process = Process(target=process_class.run, args=args[index])
                process.start()
                processes.update({'RUN_' + t: process})
                self.running_tasks.update({'RUN_' + t: process})
                index = index + 1
            for p in processes:
                processes[p].join()
            if blocking:
                for p in processes:
                    processes[p].join()
        except Exception as e:
            self.display('Error in starting processes ' + task_names)
            self.display(e)
        finally:
            pass

    def stop_process(self, task_name, *args, blocking=True):
        """
        stop a process by terminating the running task, then calling the stop method of the process as another process.

        :param task_name: the task name
        :type task_name: str

        :param args: args is a multidimensional tuple, where each element consists of the process arguments

        :param blocking: if the task is blocking (True by default)
        :type blocking: boolean

        :returns: None
        """
        try:
            running_task_name = 'RUN_' + task_name
            if running_task_name in self.get_running_task_names():
                self.running_tasks[running_task_name].terminate()
            process_class = self.tasks[task_name]
            process = Process(target=process_class.stop, args=args, daemon=True)
            process.start()
            self.running_tasks.update({'STOP_' + task_name: process})
            if blocking:
                process.join()
        except Exception as e:
            self.display('Error in stopping process ' + task_name)
            self.display(e)
        finally:
            pass

    #
    def start_asyncio_task(self, task_name, *args, **kwargs):
        """
        Start an asyncio task by first creating an asyncio task to "main" from the run method, putting this into a
        separate thread.

        :param task_name: name of the task
        :type task_name: str

        :param args: task arguments
        :param kwargs: task keyword arguments

        :return: None
        """

        try:
            task = self.tasks[task_name]

            def asyn_task():
                async def main():
                    t = asyncio.create_task(task.run())
                    await t

                asyncio.run(main())

            thr = ThreadTrace('run', task_name, self, target=asyn_task, args=args, kwargs=kwargs, daemon=True)
            thr.start()
            self.running_tasks.update({'RUN_ATask_' + task_name: thr})
        except Exception as e:
            self.display('Error in starting task ' + task_name)
            self.display(e)
        finally:
            pass

    def start_asyncio_tasks(self, task_names, *args, **kwargs):
        """
        start multiple asyncio tasks within the same thread by creating one "main" method which is comprised of multiple
        asyncio tasks created from task run methods

        :param task_names: names of the tasks
        :type task_names: list of strings

        :param args: task arguments

        :param kwargs: task keyword arguments

        :return: None
        """
        try:
            tot_task_name = ''.join(task_names)
            asyncio_tasks = []

            def asyn_task():
                async def main():
                    for task_name in task_names:
                        task = self.tasks[task_name]
                        t = asyncio.create_task(task.run())
                        asyncio_tasks.append(t)
                    for t in asyncio_tasks:
                        await t

                asyncio.run(main())

            thr = ThreadTrace('run', task_names, self, target=asyn_task, args=args, kwargs=kwargs, daemon=True)
            thr.start()
            self.running_tasks.update({'RUN_ATask_' + tot_task_name: thr})
        except Exception as e:
            self.display('Error in starting tasks ' + tot_task_name)
            self.display(e)
        finally:
            pass

    def stop_asyncio_task(self, task_name, *args, **kwargs):
        """
        Stop an asyncio task similarly to starting, but creating the main asyncio task from the stop method

        :param task_name: name of the task
        :type task_name: str

        :param args: task arguments

        :param kwargs: task keyword arguments

        :return: None
        """
        try:
            task = self.tasks[task_name]

            def asyn_task():
                async def main():
                    t = asyncio.create_task(task.stop())
                    await t

                asyncio.run(main())

            thr = ThreadTrace('run', task_name, self, target=asyn_task, args=args, kwargs=kwargs, daemon=True)
            thr.start()
            self.running_tasks.update({'STOP_ATask_' + task_name: thr})
            self.running_tasks['RUN_ATask_' + task_name].kill()
        except Exception as e:
            self.display('Error in starting task ' + task_name)
            self.display(e)
        finally:
            pass

    def stop_asyncio_tasks(self, task_names, *args, **kwargs):
        """
        stop multiple asyncio tasks similarly to starting multiple asyncio tasks, but using the stop methods. Note:
        this will not stop multiple asyncio tasks if the asyncio tasks have not been run all together using
        "start_asyncio_tasks"

        :param task_names: name of the tasks
        :type task_names: [str]

        :param args: task arguments
        :param kwargs: task keyword arguments

        :returns: None
        """
        try:
            tot_task_name = ''.join(task_names)
            for task_name in task_names:
                task = self.tasks[task_name]

                def asyn_task():
                    async def main():
                        t = asyncio.create_task(task.stop())
                        await t

                    asyncio.run(main())

                thr = ThreadTrace('run', task_name, self, target=asyn_task, args=args, kwargs=kwargs, daemon=True)
                thr.start()
                self.running_tasks.update({'STOP_ATask_' + task_name: thr})
            self.running_tasks['RUN_ATask_' + tot_task_name].kill()
        except Exception as e:
            self.display('Error in starting task ' + tot_task_name)
            self.display(e)
        finally:
            pass

    def send_command(self, queue, function_name, *args, **kwargs):
        """
        A function for making passing function commands between different processes easier
        :param queue:
        :type queue: Queue

        :param function_name: name of the function
        :type function_name: str

        :param args: task arguments

        :param kwargs: task keyword arguments

        :returns: None
        """
        to_pass = function_name, args, kwargs
        queue.put(to_pass)

    def execute_command(self, parsed_command):
        """
        A function for executing a function command

        :param parsed_command: a parsed command
        :type parsed_command: (function, (args), {kwargs})

        :returns: None
        """
        function = self.__getattribute__(parsed_command[0])
        function(*parsed_command[1], **parsed_command[2])


class ThreadTrace(threading.Thread):
    """
    A class for killable threads using traces. Inherits Thread from the threading library.
    """

    def __init__(self, task_method, task_name, flab, *args, **kwargs):
        """
        creates a ThreadTrace object, which can be killed via the kill command

        :param task_method: name of the method
        :type task_method: str

        :param task_name: name of the task
        :type task_name: str

        :param flab: a flab object
        :type flab: Flab

        :param args: arguments for the task

        :param kwargs: keyword arguments for the task

        :returns: None
        """
        self.task_method = task_method
        self.task_name = task_name
        self.flab = flab
        threading.Thread.__init__(self, *args, **kwargs)
        self.killed = False

    def start(self):
        """
        starts the thread

        :return: None
        """
        try:
            self.__run_backup = self.run
            self.run = self.__run
            threading.Thread.start(self)
        except Exception as e:
            self.flab.display(e)

    def __run(self):
        """
        creates a tracer for the thread

        :returns: None
        """
        try:
            sys.settrace(self.globaltrace)
            self.__run_backup()
            self.run = self.__run_backup
        except Exception as e:
            self.flab.display(e)

    def globaltrace(self, frame, event, arg):
        """
        Creates a global trace for the thread

        :param frame: frame

        :param event: event

        :param arg: argument

        :returns: localtrace
        """
        if event == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, event, arg):
        """
        Creates a local trace for the thread. If the thread is killed the thread will exit.

        :param frame: frame

        :param event: event

        :param arg: argument

        :return: localtrace
        """
        if self.killed:
            if event == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        """
        raises a flag to kill a thread

        :returns: None
        """
        self.killed = True
