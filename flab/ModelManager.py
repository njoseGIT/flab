# Flab 3
# ModelManager
# Distributed under GNU GPL v3
# Author: Nicholas Jose

from flab.Templates import TaskTemplate
import os
import glob

class ModelManager():

    """
    The ModelManager module contains classes and methods for creating and manipulating model objects
    """

    models = {} #A dictionary that contains data objects
    load_all_models_completed = False # A boolean that indicates if all data objects have been loaded

    def __init__(self):
        pass

    def load_model(self, model_name):
        """
        Loads a model object into the Flab object

        :param model_name: the name of the data object
        :type model_name: str

        :returns: None
        """
        self.load_object(model_name,'.Models.','model','models','Model')

    def load_models(self, model_names):
        """
        Load multiple model objects into flab.

        :param model_names: list of model names
        :type model_names: [str]

        :returns: None
        """
        try:
            for model_name in model_names:
                self.load_model(model_name)
        except Exception as e:
            self.flab.display('Error in loading model')
            self.flab.display(e)
        finally:
            pass

    def load_all_models(self):
        """
        Load every model class present in the current project's Model folder

        :returns: None
        """
        try:
            cwd = os.getcwd()
            models = glob.glob(cwd + '/Models/*.py')
            model_names = []
            for m in models:
                if not '__init__.py' in m:
                    model_names.append(m[len(cwd + '/Models/'):].replace('.py', ''))
            self.load_models(sorted(model_names))

        except Exception as e:
            self.display(e)
            self.display('Error in loading all models')
        finally:
            self.load_all_models_completed = True

    def reload_model(self, model_name):
        """
        Reload a single model object into a flab object

        :param model_name: name of the data
        :type model_name: str

        :returns: None
        """

        self.reload_object(model_name,'models','model','Model')

    def reload_model_list(self, model_names):
        """
        Reload a list of model objects.

        :param model_names: names of model objects in a list
        :type model_names: [str]

        :returns: None
        """
        reload_error = ''
        for model_name in model_names:
            error = self.reload_model(model_name)
            reload_error = reload_error + error
        if reload_error == '':
            self.display('All models reloaded successfully')
        return reload_error

    def train_model(self, model_name, *args, **kwargs):
        """
        Starts a task to train a model using the model's train method.
        In addition to model_name, passes any arguments needed by the model train method.

        :param model_name: name of the model object
        :type model_name: str
        """
        try:
            if 'TrainModel_' + model_name not in self.tasks:
                train_model_task = TrainModelTask(self, model_name)
                self.tasks.update({'TrainModel_' + model_name: train_model_task})
            self.start_task('TrainModel_' + model_name, *args, **kwargs)
        except Exception as e:
            self.display('Error in training model: ' + model_name)
            self.display(e)
        finally:
            pass

    def predict_model(self, model_name, *args, **kwargs):
        """
        Predicts an output from given inputs with the model.
        In addition to model_name, passes any arguments needed by the model predict method.


        :param model_name: name of the model object
        :type model_name: str
        """
        try:
            if 'PredictModel_' + model_name not in self.tasks:
                predict_model_task = PredictModelTask(self, model_name)
                self.tasks.update({'PredictModel_' + model_name: predict_model_task})
            self.start_task('PredictModel_' + model_name, *args, **kwargs)
        except Exception as e:
            self.display('Error in model prediction: ' + model_name)
            self.display(e)
        finally:
            pass

    def evaluate_model(self, model_name, *args, **kwargs):
        """
        Evaluates the model against a known set of data.
        In addition to model_name, passes any arguments needed by the model evaluate method.


        :param model_name: name of the model object
        :type model_name: str
        """
        try:
            if 'EvaluateModel_' + model_name not in self.tasks:
                evaluate_model_task = EvaluateModelTask(self, model_name)
                self.tasks.update({'EvaluateModel_' + model_name: evaluate_model_task})
            self.start_task('EvaluateModel_' + model_name, *args, **kwargs)
        except Exception as e:
            self.display('Error in model evaluation: ' + model_name)
            self.display(e)
        finally:
            pass

class TrainModelTask(TaskTemplate.Task):
    """
    A Task for updating data files.
    """

    task_name = 'TrainModel'
    task_type = 'thread'
    task_stopped = False

    def __init__(self, flab_object, model_name):
        self.task_name = self.task_name + '_' + model_name
        self.model_name = model_name
        self.flab = flab_object

    def run(self, *args, **kwargs):
        """
        trains the model
        """
        try:

            success = True
            train = self.flab.models[self.model_name].get('train')
            train(*args, **kwargs)

        except Exception as e:
            self.flab.display('Error in training model - ' + self.model_name)
            self.flab.display(str(e))
            success = False

        finally:
            return success

    def stop(self):
        self.flab.tasks[self.task_name].task_stopped = True  # a flag to stop the script

class PredictModelTask(TaskTemplate.Task):
    """
    A Task for running model predictions
    """

    task_name = 'PredictModel'
    task_type = 'thread'
    task_stopped = False

    def __init__(self, flab_object, model_name):
        self.task_name = self.task_name + '_' + model_name
        self.model_name = model_name
        self.flab = flab_object

    def run(self, *args,**kwargs):
        """
        runs model prediction task
        """
        try:
            success = True
            predict = self.flab.models[self.model_name].get('predict')
            predict(*args, **kwargs)

        except Exception as e:
            self.display('Error in model prediction - ' + self.model_name)
            self.display(str(e))
            success = False

        finally:
            return success

    def stop(self):
        '''
        stops task for model prediction

        :returns: None
        '''
        self.flab.tasks[self.task_name].task_stopped = True  # a flag to stop the script

class EvaluateModelTask(TaskTemplate.Task):
    """
    A Task for running model evaluation
    """

    task_name = 'EvaluateModel'
    task_type = 'thread'
    task_stopped = False

    def __init__(self, flab_object, model_name):
        self.task_name = self.task_name + '_' + model_name
        self.model_name = model_name
        self.flab = flab_object

    def run(self, *args,**kwargs):
        """
        runs model evaluation task
        """
        try:
            success = True
            evaluate = self.flab.models[self.model_name].get('evaluate')
            evaluate(*args, **kwargs)

        except Exception as e:
            self.display('Error in model evaluation - ' + self.model_name)
            self.display(str(e))
            success = False

        finally:
            return success

    def stop(self):
        '''
        stops task for model evaluation

        :returns: None
        '''
        self.flab.tasks[self.task_name].task_stopped = True  # a flag to stop the script
