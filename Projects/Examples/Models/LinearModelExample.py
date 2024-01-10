# LinearModelExample.py
# An example model class for linear models
# Distributed under GNU GPL v3
# Nicholas A. Jose

from flab3.Templates import ModelTemplate
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import cross_val_predict
from sklearn.linear_model import LinearRegression

class Model(ModelTemplate.Model):

    model_name = 'LinearModelExample' #name of the data object
    x = [[1], [2], [3]] # x data
    y = [1.1,2.4,3.8] # y data (actual)
    cross_validation_folds = 3 # number of cross-validation folds for evaluation
    model = LinearRegression()

    def train(self):
        """
        Fits the data to a line

        :returns: None
        """
        try:
            # Fit the model to the training data
            self.model.fit(self.x, self.y)

        except Exception as e:
            self.flab.display('Error in training of ' + self.model_name)
            self.flab.display(e)

        finally:
            pass


    def predict(self, x_values):
        """
        Makes a model prediction with given x values

        :returns: predicted y values
        :rtype: list
        """
        try:
            y_prediction = []
            x_values = [[value] for value in x_values]
            y_prediction = self.model.predict(x_values)
            self.flab.display(y_prediction)

        except Exception as e:
            self.flab.display('Error in prediction of ' + self.model_name)
            self.flab.display(e)

        finally:
            return y_prediction

    def evaluate(self):
        """
        Evaluates the model accuracy in terms of mean squared error and R^2.

        :returns: mean squared error, R^2 value
        :rtype: tuple
        """
        try:
            model_mean_squared_error = -1
            model_r2 = -1

            # Perform cross-validation
            y_predicted = cross_val_predict(self.model, self.x, self.y, cv=self.cross_validation_folds)

            # Calculate performance metrics
            model_mean_squared_error = mean_squared_error(self.y, y_predicted)
            model_r2 = r2_score(self.y, y_predicted)

        except Exception as e:
            self.flab.display('Error in training of ' + self.model_name)
            self.flab.display(e)

        finally:
            return model_mean_squared_error, model_r2
