from flab.Templates import DeviceTemplate
import pandas as pd
import glob
import os
from io import StringIO
from datetime import datetime
import time

class Device(DeviceTemplate.Device):
    device_name = 'AgilentLC'
    directory = "C:\\CHEM32"
    info = {
        'long_name': 'Agilent HPLC',
        'description': 'Wet lab HPLC connected to Vapourtec',
        'guide': 'Ensure connection and solvents are topped up before using any methods',
        'configuration': {
            'directory': {
                'unit': 'None',
                'description': 'Default data storage directory',
                'default':"C:\\CHEM32",
                'type': 'string'
            }

        },
        'methods': {
            'search_for_sample_hplc_file': {
                'description': 'This method search for the hplc result file',
                'guide': 'run this when the hplc method is completed',
            },
            'extract_peak_data': {
                'description': 'This method extracts analyzed peak data from a given results file',
                'guide': 'Some information',
                'parameters': {
                    'sample_hplc_path': {
                        'description': 'file path where sample data is stored',
                        'unit': 'NA',
                        'type': 'str',
                        #'default': ,
                    }
                }
            }
        }
    }

    def search_for_sample_hplc_file(self):
        """
        Searches for a sample HPLC file in the predefined directory and returns its path.

        Returns:
        str: Path of the newest HPLC file found in the directory.
        """
        try:
            directory = "C:\\CHEM32"
            file_extension = "*.xls"
            wait_time = 60
            poll_interval = 10

            hplc_path = os.path.join(directory, '**', file_extension)
            newest_hplc_time = 0

            timeout = 5
            tries = 0
            while tries <= timeout:
                hplc_files = glob.glob(hplc_path, recursive=True)
                self.flab.display(f'Available hplc files: {hplc_files}')
                if hplc_files:
                    latest_file = max(hplc_files, key=os.path.getmtime)
                    latest_file_time = os.path.getmtime(latest_file)
                    current_time = datetime.now().timestamp()

                    if current_time - latest_file_time < wait_time and latest_file_time != newest_hplc_time:
                        self.flab.display(f'Successfully found latest HPLC file on Shimadzu at {latest_file}')
                        return latest_file

                time.sleep(poll_interval)
                tries += 1
            if tries > timeout:
                self.flab.display('Could not find HPLC file path')
                
        except Exception as e:
            self.flab.display(f'Error in finding HPLC file path: {e}')
            return None

    def extract_peak_data(self,sample_hplc_path):
        """
        Extracts RT and area data from HPLC files.

        Args:
        sample_hplc_path (str): Directory path where HPLC files are located.

        Returns:
        DataFrame: A table with retention times and corresponding areas.
        """
        try:
            hplc_table = pd.read_excel(sample_hplc_path, sheet_name='IntResults1', usecols=['RetTime', 'Area'])

            hplc_table.columns = ['RT', 'Area']

            return hplc_table
        except Exception as e:
            self.flab.display(f'Error in extracting peak data: {e}')
            return None

    def get_product_area(self, table, product_retention_time = None, internal_standard_retention_time= None):
        """
        Finds the closest peak to the product RT and calculates the product area.
        Optionally calculates the ratio to the internal standard (IS) area.

        Args:
        table (DataFrame): Table containing RT and area data.
        product_retention_time (float): Retention time of the product in minutes
        internal_standard_retention_time (float, optional): Retention time of the internal standard in minutes

        Returns:
        float: Product area or ratio of product area to IS area.
        """
        try:
            product_rt_dev = abs(table['RT'] - product_retention_time)
            product_rt_idx = product_rt_dev.idxmin()

            if product_rt_dev[product_rt_idx] < 0.15:
                product_area = table.at[product_rt_idx, 'Area']
            else:
                product_area = 0

            if internal_standard_retention_time is not None and internal_standard_retention_time != '':
                is_rt_dev = abs(table['RT'] - internal_standard_retention_time)
                is_rt_idx = is_rt_dev.idxmin()

                if is_rt_dev[is_rt_idx] <= 0.15:
                    is_area = table.at[is_rt_idx, 'Area']
                    return product_area / is_area if is_area != 0 else 0

            return product_area
        except Exception as e:
            self.flab.display(f'Error could not get product area: {e}')


