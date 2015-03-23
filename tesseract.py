import os
import subprocess
from derivatives import Derivatives

class Tesseract(Derivatives):

    def __init__(self, file_path):
        
        self.file_path = file_path

    def get_text(self, output_basename=None, config_file=""):
        """
        Run with config_file='hocr' for output in HTML.
        """
        self.output_basename = output_basename
        self.name = "Text generation {0}".format(config_file)

        if not self.output_basename:
            self.output_basename = os.path.splitext(self.file_path)[0].replace("TIFFs", "OCR")
        
        self.cmds = ["tesseract", self.file_path, self.output_basename, config_file]
        self.print_process()
        self.return_code = self.run_cmds()
        self.print_output()


