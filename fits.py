import os
import subprocess
from derivatives import Derivatives

class Fits(Derivatives):

    def __init__(self, file_path):

        self.file_path = file_path
        self.config_section = "fits"
        self.get_configs()

    def get_fits(self, output_file=None):
        """
        Generate fits output. Give fits_location the location of fits.sh
        """
        self.name = "FITS"
        self.output_file = output_file
        if not self.output_file:
            self.output_file = os.path.join(os.path.split(self.file_path)[0], 'fits.xml').replace("TIFFs", "FITS")
    
        self.cmds = (self.fits_commands.replace("fits_location", self.fits_location).replace("file_path", self.file_path).replace("output_file", self.output_file)).split()
        self.print_process()
        self.return_code = self.run_cmds()
        
        if self.return_code == 1:
            self.cmds = (self.fits_commands_alt.replace("fits_location", self.fits_location).replace("file_path", self.file_path).replace("output_file", self.output_file)).split()
            self.return_code = self.run_cmds()

        self.print_output()


