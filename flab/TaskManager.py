#Flab
#TaskManager
#Version 2.0.1
#Published 17-Jul-2022
#Distributed under GNU GPL v3
#Author: Nicholas Jose
#Update: No longer contains Qthread capabilities to remove dependency on PyQt

import glob
import threading
import sys
import os
import asyncio
import importlib
from multiprocessing import Process

class TaskManager():

    description = 'Methods for loading, running and terminating tasks implementing python\'s threading ' \
                  'library, asyncio, and multiprocessing'
    version = '2.0.1'
    tasks = {} #dictionary of loaded tasks
    running_tasks = {} #dictionary of running tasks (i.e. instances of threads)
    load_all_tasks_completed = False

    def __init__(self):
        pass

    #load a single task into flab. The task name is given by the filename, without the '.py' at the end
    def load_task(self,task_name):
        load_err = ''
        try:
            module_name = 'Projects.' + os.path.split(os.getcwd())[1]+'.Tasks.' + task_name
            mo = importlib.import_module(module_name)
            nt = mo.Task(self)
            #dictionary entry
            mod = {task_name:mo}
            ntd = {task_name:nt}
            self.tasks.update(ntd)
            self.modules.update(mod)
        except Exception as e:
            load_err = load_err + 'Error loading task ' + task_name + '.'
            self.display(load_err)
            self.display(e)
        if load_err == '':
            self.display(task_name + ' loaded successfully.')
        return load_err

    #load a list of tasks into flab. task_names is an array of the task names (string)
    def load_tasks(self, task_names):
        load_err = ''
        for ta in task_names:
            ta_err = self.load_task(ta)
            load_err = load_err + ta_err
        if load_err == '':
            self.display('All tasks loaded successfully.')
        return load_err

    #load every task present in the current project's Tasks folder
    def load_all_tasks(self):
        try:
            cwd = os.getcwd()
            tasks = glob.glob(cwd+'/Tasks/*.py')
            task_names = []
            for t in tasks:
                task_names.append(t[len(cwd+'/Tasks/'):].replace('.py',''))
            self.load_tasks(sorted(task_names))
        except Exception as e:
            self.display(e)
            self.display('Error in loading tasks')
        finally:
            self.load_all_tasks_completed = True

    #reload a single task into the flab
    def reload_task(self,task_name):
        reload_err = ''
        try:
            mo = importlib.reload(self.modules[task_name])
            nt = self.modules[task_name].Task(self)
            #dictionary entry
            mod = {task_name:mo}
            ntd = {task_name:nt}
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

    #reload multiple tasks in a list
    def reload_tasks(self,task_names):
        reload_err = ''
        for ta in task_names:
            err = self.reload_task(ta)
            reload_err = reload_err + err
        if reload_err == '':
            self.display('All Tasks reloaded successfully')
        return reload_err

    #start a task using the "run" method. By default this runs each task as a thread, but if the task type is specified
    #otherwise, it will start the task as an asyncio thread or a process
    def start_task(self, task_name, *args, **kwargs):
        try:
            task = self.tasks[task_name]
            if hasattr(task,'task_type'):
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

    #load and start a task in one method
    def load_start_task(self, task_name, *args, **kwargs):
        try:
            self.load_task(task_name)
            self.start_task(task_name, *args, **kwargs)
        except Exception as e:
            self.display('Error in loading and starting task ' + task_name)
            self.display(e)
        finally:
            pass

    #reload and start a task in one method
    def reload_start_task(self, task_name, *args, **kwargs):
        try:
            self.reload_task(task_name)
            self.start_task(task_name, *args, **kwargs)
        except Exception as e:
            self.display('Error in loading and starting task ' + task_name)
            self.display(e)
        finally:
            pass

    #stop a task using the task's "stop" method. By default this runs each task as a thread, but if the task type is specified
    #otherwise, it will start the task as an asyncio thread or a process
    def stop_task(self, task_name, *args, **kwargs):
        try:
            task = self.tasks[task_name]
            if hasattr(task,'task_type'):
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

    #this method stops all running tasks
    def stop_all_tasks(self):
        try:
            current_tasks = self.running_tasks
            temp_tasks =[]
            for t in current_tasks:
                if t.__contains__('RUN_'):
                    temp_tasks.append(t)
            for t in temp_tasks:
                tt = t.replace('RUN_','')
                self.stop_task(tt)
        except Exception as e:
            print(e)
            self.display(e)
        finally:
            pass

    #start a thread with the run method, with input arguments args and kwargs
    def start_thread(self, task_name, *args, **kwargs):
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

    #stop a thread with the stop method, with input arguments args and kwargs
    def stop_thread(self, task_name, *args, **kwargs):
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

    # directly kills a thread
    def kill_thread(self, thread_name):
        thr = self.running_tasks[thread_name]
        thr.kill()
        thr.join()

    #displays task instances
    def display_running_tasks(self):
        self.display(self.running_tasks.keys())

    #display all threads that are still alive
    def display_alive_threads(self):
        for thr in self.running_tasks:
            try:
                if self.running_tasks[thr].is_alive() is True:
                    self.display(thr)
            finally:
                pass

    #returns task instances
    def get_running_task_names(self):
        running_task_names = []
        for i in self.running_tasks:
            if self.running_tasks[i].is_alive() is True:
                running_task_names.append(i)
        return running_task_names

    #start a process with the run method,  with input arguments args and kwargs
    def start_process(self, task_name, *args, blocking=False):
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

    #start multiple processes at once. args is a multidimensional tuple, where each element consists of the process arguments
    def start_processes(self, task_names, *args, blocking=False):
        try:
            procs = {}
            index = 0
            for t in task_names:
                process_class = self.tasks[t]
                process = Process(target=process_class.run, args=args[index])
                process.start()
                procs.update({'RUN_' + t: process})
                self.running_tasks.update({'RUN_' + t: process})
                index = index + 1
            for p in procs:
                procs[p].join()
            if blocking:
                for p in procs:
                    procs[p].join()
        except Exception as e:
            self.display('Error in starting processes ' + task_names)
            self.display(e)
        finally:
            pass

    #stop a process by terminating the running task, then calling the stop method of the process as another process.
    def stop_process(self, task_name, *args, blocking=True):
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

    #start an asyncio task by first creating an asyncio task to "main" from the run method, putting this into a separate
    #thread
    def start_asyncio_task(self, task_name, *args, **kwargs):
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

    #start multiple asyncio tasks within the same thread by creating one "main" method which is comprised of multiple
    #asyncio tasks created from task run methods
    def start_asyncio_tasks(self,task_names,*args,**kwargs):
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
            self.display('Error in starting task ' + tot_task_name)
            self.display(e)
        finally:
            pass

    #stop an asyncio task similarly to starting, but creating the main asyncio task from the stop method
    def stop_asyncio_task(self, task_name, *args, **kwargs):
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
            self.running_tasks['RUN_ATask_'+task_name].kill()
        except Exception as e:
            self.display('Error in starting task ' + task_name)
            self.display(e)
        finally:
            pass

    #stop multiple asyncio tasks similarly to starting multiple asyncio tasks, but using the stop methods. Note: this
    #will not stop multiple asyncio tasks if the asyncio tasks have not been run all together using "start_asyncio_tasks"
    def stop_asyncio_tasks(self, task_names, *args, **kwargs):
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
            self.running_tasks['RUN_ATask_'+tot_task_name].kill()
        except Exception as e:
            self.display('Error in starting task ' + tot_task_name)
            self.display(e)
        finally:
            pass

    #a function for passing function commands between different processes easier
    def send_command(self, queue, function_name, *args, **kwargs):
        to_pass = function_name, args, kwargs
        queue.put(to_pass)

    #a function for executing a function command, where the parsed command = (function, (args), {kwargs})
    def execute_command(self,parsed_command):
        function = self.__getattribute__(parsed_command[0])
        function(*parsed_command[1], **parsed_command[2])

#A class for killable threads using traces
class ThreadTrace(threading.Thread):

    def __init__(self, task_method, task_name, flab, *args, **kwargs):
        self.task_method = task_method
        self.task_name = task_name
        self.flab = flab
        threading.Thread.__init__(self, *args, **kwargs)
        self.killed = False

    #start the thread
    def start(self):
        try:
            self.__run_backup = self.run
            self.run = self.__run
            threading.Thread.start(self)
        except Exception as e:
            self.flab.display(e)

    #create trace
    def __run(self):
        try:
            sys.settrace(self.globaltrace)
            self.__run_backup()
            self.run = self.__run_backup
        except Exception as e:
            self.flab.display(e)

    #a global trace
    def globaltrace(self, frame, event, arg):
        if event == 'call':
            return self.localtrace
        else:
            return None

    #a local trace
    def localtrace(self, frame, event, arg):
        if self.killed:
            if event == 'line':
                raise SystemExit()
        return self.localtrace

    #a flag to kill a thread
    def kill(self):
        self.killed = True
