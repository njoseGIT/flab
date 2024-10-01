from flab.Templates import DeviceTemplate
import pandas as pd
import glob
import os
from io import StringIO
from datetime import datetime
import time
import numpy as np

class Device(DeviceTemplate.Device):
    device_name = 'Avantes'
    directory = r"C:\Users\User\Desktop"
    file_extension = "*.dat"
    SB1 = 0
    SB2 = 0
    
    def search_time_series(self):
        
        avantes_path = os.path.join(self.directory, self.file_extension)
        
        try:

            avantes_files = glob.glob(avantes_path)
            self.flab.display(f'Available Avantes files: {avantes_files}')
            self.avantes_files = avantes_files
            
            
        except Exception as e:
            self.flab.display(f'Error in finding Avantes file path: {e}')
            return None
        
    def calculate_uv_data(self):

        starter_mark = "Time "

        for i in self.avantes_files:

            data = open(i, 'r').read()
            content = data[data.find(starter_mark):]
            table = pd.read_csv(StringIO(content), delimiter='\s+', engine='python')
            values = table["Function"].to_numpy()

            if i == r"C:\Users\User\Desktop\Baseline 2.dat":
                self.baseline = values[-5:]

            if i == r"C:\Users\User\Desktop\SB1.dat":
                mean = 0
                counter=0
                for j in values[-5:]:
                    j = j - self.baseline[counter]
                    mean += j
                    counter+=1
                self.SB1 = mean / 5

                self.flab.display(f"SB1: {round(self.SB1, 4)}")

            if i == r"C:\Users\User\Desktop\SB2.dat":
                mean = 0
                counter = 0
                for j in values[-5:]:
                    j = j - self.baseline[counter]
                    mean += j
                    counter += 1
                self.SB2 = mean / 5

                self.flab.display(f"SB2: {round(self.SB2, 4)}")
        return [self.SB1, self.SB2]
