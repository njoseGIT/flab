# NeuralNetworkExample.py
# An example model class for neural network models
# Distributed under GNU GPL v3
# Nicholas A. Jose

from flab3.Templates import ModelTemplate
import tensorflow as tf
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

class Model(ModelTemplate.Model):

    model_name = 'NeuralNetworkExample' #name of the data object
    hidden_units = 64 # Number of units in the hidden layer (default is 64)
    epochs = 10 # number of training epochs
    batch_size = 32 # size of training batches
    X_prediction = []
    y_pred = []
    model = None
    X_train = []
    y_train = []
    X_test = []
    y_test = []

    def initalize(self):
        """
        Load the California Housing dataset

        :returns: None
        """

        try:
            housing = fetch_california_housing()
            self.X, self.y = housing.data, housing.target

            # Standardize the features
            scaler = StandardScaler()
            self.X = scaler.fit_transform(self.X)

            # Split the data into training and testing sets
            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)

        except Exception as e:
            self.flab.display('Error in loading boston datset in NeuralNetworkExample')
            self.flab.display(e)

        finally:
            pass

    def train(self):
        """
        Train a simple neural network for regression using TensorFlow/Keras.

        :returns: None
        """

        try:
            self.initalize()
            self.model = tf.keras.Sequential([
                tf.keras.layers.Dense(self.hidden_units, activation='relu', input_shape=(self.X_train.shape[1],)),
                tf.keras.layers.Dense(1)  # Output layer for regression (1 output unit)
            ])

            self.model.compile(optimizer='adam', loss='mean_squared_error')
            self.flab.vars['NeuralNetworkExample_history'] = self.model.fit(self.X_train, self.y_train, epochs=self.epochs, batch_size=self.batch_size)

        except Exception as e:
            self.flab.display('Error in training of ' + self.model_name)
            self.flab.display(e)

        finally:
            pass

    def predict(self):
        """
        Makes model prediction based on a given dataset

        :returns: y prediction
        """
        try:
            self.y_pred = None
            self.y_pred = self.model.predict(self.X_test).flatten()

        except Exception as e:
            self.flab.display('Error in prediction of ' + self.model_name)
            self.flab.display(e)

        finally:
            return self.y_pred

    def evaluate(self):
        """
        Description:

        :returns: None
        """
        try:
            # make prediction on test dataset
            y_pred = self.model.predict(self.X_test).flatten()

            # evaluate error of prediction
            mse = mean_squared_error(self.y_test, y_pred)
            r2 = r2_score(self.y_test, y_pred)

            self.flab.display(f'Mean Squared Error (MSE): {mse:.2f}')
            self.flab.display(f'R-squared (R2): {r2:.2f}')


        except Exception as e:
            self.flab.display('Error in evaluating ' + self.model_name)
            self.flab.display(e)

        finally:
            pass