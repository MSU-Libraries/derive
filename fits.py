import os
import subprocess
from derivatives import Derivatives

class Fits(Derivatives):

    def __init__(self, file_path):
        self.file_path = file_path

    def get_fits(self, output_file=None, fits_location=""):
        """
        Generate fits output. Give fits_location the location of fits.sh
        """
        self.output_file = output_file
        if not self.output_file:
            self.output_file = os.path.join(os.path.split(self.file_path)[0], 'fits.xml')
        
        self.cmds = [os.path.join(fits_location, "fits.sh"), "-i", self.file_path, "-xc", "-o", self.output_file]
	returncode=Derivatives.run_cmds(self)
	if returncode == 1:
		self.cmds = [os.path.join(fits_location, "fits.sh"), "-i", self.file_path, "-x", "-o", self.output_file]
	        returncode=Derivatives.run_cmds(self)
		if returncode == 1:
			print "Both commands failed."
