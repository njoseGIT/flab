from flab.Templates import DeviceTemplate
import pandas as pd
import glob
import os
from io import StringIO
from datetime import datetime
import time
import numpy as np

class Device(DeviceTemplate.Device):
    device_name = 'ShimadzuLC'
    directory = r"C:\LabSolutions\Data\naoto\amidation\training data\20230813-Maxpro repeat"
    table = None
    info = {
        'long_name': 'Shimadzu HPLC',
        'description': 'Wet lab HPLC connected to Vapourtec',
        'guide': 'Ensure connection and solvents are topped up before using any methods',
        'configuration': {
            'directory': {
                'unit': 'None',
                'description': 'Default data storage directory',
                'default':"C:\LabSolutions\Data\naoto\amidation\training data\20230813-Maxpro repeat",
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
                        'type': 'str'
                    }
                }
            }
        }
    }

    def search_for_sample_hplc_file(self, directory = r"C:\LabSolutions\Data\naoto\amidation\training data\20230813-Maxpro repeat"):
        """
        Searches for a sample HPLC file in the predefined directory and returns its path.

        Returns:
        str: Path of the newest HPLC file found in the directory.
        """
        try:
            file_extension = "*.txt"
            wait_time = 10000000
            poll_interval = 1

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

    def extract_peak_data(self, sample_hplc_path):
        """
        Retrieves retention time (RT) and area data from an HPLC file.

        Args:
            sample_hplc_path (str): Path to the HPLC file.

        Returns:
            DataFrame: Table containing retention times and corresponding areas.
        """
        try:
            startmrk = "Peak#"
            endmrk = "[LC Chromatogram(AD2)]"

            hplcreport = open(sample_hplc_path, 'r').read()
            hplcstr = hplcreport[(hplcreport.find(startmrk)):(hplcreport.find(endmrk) - 2)]
            hplctable = pd.read_csv(StringIO(hplcstr), delimiter='\t')
            self.table = hplctable

            self.flab.display(self.table)

            return hplctable

        except Exception as e:
            self.flab.display(f'Error in extracting peak data: {e}')
        finally:
            self.flab.display(f'Task extract_peak_data completed.')

    def get_product_area(self, product_retention_time = None, internal_standard_retention_time= None):
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
            table = self.table

            hplcareas = table['Area'].to_numpy()
            hplcrt = table['R.Time'].to_numpy()

            prodrtdev = abs(np.subtract(hplcrt, product_retention_time))
            prodrtidx = np.where(prodrtdev == np.nanmin(prodrtdev))

            if prodrtdev[prodrtidx] < 0.15:
                product_peak_area = hplcareas[prodrtidx][0]
            else:
                product_peak_area = 0

            if internal_standard_retention_time is not None:
                isrtdev = abs(np.subtract(hplcrt, internal_standard_retention_time))
                isrtidx = np.where(isrtdev == np.nanmin(isrtdev))

                if isrtdev[isrtidx] < 0.15:
                    is_peak_area = hplcareas[isrtidx][0]
                else:
                    is_peak_area = 0

            if internal_standard_retention_time is not None:
                peak_area = product_peak_area / is_peak_area if is_peak_area != 0 else 0
            else:
                peak_area = product_peak_area

            self.flab.display(peak_area)

            return peak_area


        except Exception as e:
            self.flab.display(f'Error could not get product area: {e}')


