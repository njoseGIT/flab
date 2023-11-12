# Flab 3
# DataManager
# Distributed under GNU GPL v3
# Author: Nicholas Jose

from flab.Templates import TaskTemplate

class DataManager():

    """
    The DataManager module contains classes and methods for creating and manipulating data objects
    """

    data = {} #A dictionary that contains data objects
    load_all_data_completed = False # A boolean that indicates if all data objects have been loaded

    def __init__(self):
        pass

    def load_data(self, data_name):
        """
        Loads a data object into the Flab object

        :param data_name: the name of the data object
        :type data_name: str

        :returns: None
        """
        self.load_object(data_name,'.Data.','data','data','Data')

    def load_data_list(self, data_names):
        """
        Load multiple data objects into flab.

        :param data_names: list of data names
        :type data_names: [str]

        :returns: None
        """
        try:
            for d in data_names:
                self.load_data(d)
        except Exception as e:
            self.flab.display('Error in loading data')
            self.flab.display(e)
        finally:
            pass

    def load_all_data(self):
        """
        Load every data class present in the current project's Data folder

        :returns: None
        """
        try:
            self.load_all_objects('/Data/', 'data', 'data', 'Data')
        except Exception as e:
            self.display(e)
            self.display('Error in loading all data')
        finally:
            self.load_all_data_completed = True

    def reload_data(self, data_name):
        """
        Reload a single data object into a flab object

        :param data_name: name of the data
        :type data_name: str

        :returns: None
        """

        self.reload_object(data_name,'data','data','Data')

    def reload_data_list(self, data_names):
        """
        Reload a list of data objects.

        :param data_names: names of data objects in a list
        :type data_names: [str]

        :returns: None
        """
        reload_error = ''
        for data in data_names:
            error = self.reload_data(data)
            reload_error = reload_error + error
        if reload_error == '':
            self.display('All data reloaded successfully')
        return reload_error

    def update_data_file(self, data_name):
        """
        Starts a task to update a file with the current variable data.

        :param data_name: name of the data object
        :type data_name: str
        """
        try:
            if 'UpdateDataFile_' + data_name not in self.tasks:
                update_file_task = UpdateDataFileTask(self, data_name)
                self.tasks.update({'UpdateDataFile_' + data_name: update_file_task})
            self.start_task('UpdateDataFile_' + data_name)
        except Exception as e:
            self.display('Error in updating data file: ' + data_name)
            self.display(e)
        finally:
            pass

    def update_data_variable(self, data_name):
        """
        Updates flab variables with file data

        :param data_name: name of the data object
        :type data_name: str
        """
        try:
            if 'UpdateDataVariable_' + data_name not in self.tasks:
                update_data_task = UpdateDataVariableTask(self, data_name)
                self.tasks.update({'UpdateDataVariable_' + data_name: update_data_task})
            self.start_task('UpdateDataVariable_' + data_name)
        except Exception as e:
            self.display('Error in updating data variable: ' + data_name)
            self.display(e)
        finally:
            pass

class UpdateDataFileTask(TaskTemplate.Task):
    """
    A Task for updating data files.
    """

    task_name = 'UpdateDataFile'
    task_type = 'thread'
    task_stopped = False

    def __init__(self, flab_object, data_name):
        self.task_name = self.task_name + '_' + data_name
        self.data_name = data_name
        self.flab = flab_object

    def run(self):
        """
        parses and writes data object into file
        """
        try:

            success = True
            update_file = self.flab.data[self.data_name].get('update_file')
            update_file()

        except Exception as e:
            self.flab.display('Error in writing data to file - ' + self.data_name)
            self.flab.display(str(e))
            success = False

        finally:
            return success

    def stop(self):
        self.flab.tasks[self.task_name].task_stopped = True  # a flag to stop the script

class UpdateDataVariableTask(TaskTemplate.Task):
    """
    A Task for updating data variables.
    """

    task_name = 'UpdateDataVariable'
    task_type = 'thread'
    task_stopped = False

    def __init__(self, flab_object, data_name):
        self.task_name = self.task_name + '_' + data_name
        self.data_name = data_name
        self.flab = flab_object

    def run(self):
        """
        reads file data and parses into flab variables
        """
        try:
            success = True
            update_variable = self.flab.data[self.data_name].get('update_variable')
            update_variable()

        except Exception as e:
            self.display('Error in parsing data to flab - ' + self.data_name)
            self.display(str(e))
            success = False

        finally:
            return success

    def stop(self):
        '''
        stops task for updating variable

        :returns: None
        '''
        self.flab.tasks[self.task_name].task_stopped = True  # a flag to stop the script
