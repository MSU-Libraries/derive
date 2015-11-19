"""Build and run FITS commands."""

import os
from derivatives import Derivatives


class Fits(Derivatives):

    """Build and run FITS commands."""

    def __init__(self, file_path):
        """Initiate with file to process.

        args:
            file_path(str): path to file to run FITS on.
        """
        self.file_path = file_path
        self.config_section = "fits"
        self.get_configs()

    def get_fits(self, output_file=None):
        """Generate fits output.

        kwargs:
            output_file(str): location to store output, defaults to input path.
        """
        self.name = "FITS"
        self.output_file = output_file
        if not self.output_file:
            output_file_path = os.path.split(self.file_path)[0]\
                                      .replace("TIFFs", "FITs")
            self.output_file = os.path.join(output_file_path, 'fits.xml')
        self.cmds = self._create_cmds_fits(self.fits_commands, self.file_path,
                                          self.output_file)

        self.return_code = self.run_cmds()
        if self.return_code == 1:
            self.cmds = self._create_cmds_fits(self.fits_commands_alt,
                                              self.file_path, self.output_file)
            self.return_code = self.run_cmds()

        self.print_output()
