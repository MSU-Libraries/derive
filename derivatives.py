"""Default methods to apply to all derivatives."""
import subprocess
import os
from ConfigParser import ConfigParser


class Derivatives():

    """Default methods to apply to all derivatives."""

    def __init__(self):
        """Load configs from config file."""
        self.config_section = "dirs"
        self.get_configs()

    def run_cmds(self):
        """Run self.cmds object."""
        process = 1
        try:
            # print "Running: {0}".format(" ".join(self.cmds))
            process = subprocess.check_call(self.cmds,
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE)

        except Exception as e:

            print e

        finally:
            if process != 0:
                print process

        return process

    def get_configs(self):
        """Load all configs from config file."""
        config = ConfigParser()
        cwd = os.path.dirname(os.path.abspath(__file__))
        config.read(os.path.join(cwd, "settings.cfg"))
        for name, value in config.items(self.config_section):
            setattr(self, name, value)


    def print_process(self):

        pass
        # print "===Starting {0}".format(self.name)

    def print_output(self):

        if self.return_code == 0:
            pass
            # print "====={0} succeeded".format(self.name)
        else:
            pass
            # print "====={0} failed".format(self.name)

    def _create_cmds(self, base_cmd, input_file, output_file):
        """Combine command string with file input and outputs.

        args:
            base_cmd(str): string of commands from config file.
            input(str): path to input file.
            output(str): path to output file.

        returns:
            (list): commands to execute.
        """
        input_file_clean = input_file.replace(" ", "|||")
        output_file_clean = output_file.replace(" ", "|||")
        cmds = base_cmd.replace("input_file", input_file_clean)\
                       .replace("output_file", output_file_clean).split()
        return [c.replace("|||", " ") for c in cmds]

    def _create_cmds_fits(self, base_cmd, input_file, output_file):
        """Combine commands for FITS deriv generation.

        args:
            base_cmd(str): string of commands from config file.
            input(str): path to input file.
            output(str): path to output file.

        returns:
            (list): commands to execute.
        """
        input_file_clean = input_file.replace(" ", "|||")
        output_file_clean = output_file.replace(" ", "|||")
        cmds = base_cmd.replace("file_path", input_file_clean)\
                       .replace("output_file", output_file_clean)\
                       .replace("fits_location", self.fits_location)\
                       .split()
        return [c.replace("|||", " ") for c in cmds]
