from Derivatives import Derivatives
from ConfigParser import ConfigParser
import os
import subprocess

class ImageMagickConverter(Derivatives):

    def __init__(self, image_type="tif"):

        self.config_section = image_type
        self.__get_configs()


    def convert_jpeg_low(self, input_tif, output_jpg):

        self.name = "JPEG low-quality conversion"
        self.cmds = self.jpeg_low.replace("image.tif", input_tif).replace("image.jpg", output_jpg)split()
        self.return_code = Derivatives.run_cmds()
        self.__print_output()

    def convert_jpeg_high(self, input_tif, output_jpg):

        self.name = "JPEG high-quality conversion"
        self.cmds = self.jpeg_high.replace("image.tif", input_tif).replace("image.jpg", output_jpg).split()
        self.return_code = Derivatives.run_cmds()
        self.__print_output()

    def convert_thumbnail(self, input_tif, output_jpg):

        self.name = "Thumbnail conversion"
        self.cmds = self.thumbnail.replace("image.tif", input_tif).replace("image.jpg", output_jpg).split()
        self.return_code = Derivatives.run_cmds()
        self.__print_output()

    def convert_islandora_jpg(self, input_tif, output_jpg):

        self.name = "Islandora JPG conversion"
        self.cmds = self.islandora_jpg.replace("image.tif", input_tif).replace("image.jpg", output_jpg).split()
        self.return_code = Derivatives.run_cmds()
        self.__print_output()


    def __get_configs(self):
        
        config = ConfigParser()
        cwd = os.path.dirname(os.path.abspath(__file__))
        config.read(os.path.join(cwd, "settings.cfg"))
        for name, value in config.items(self.config_section):
            setattr(self, name, value)


    def __print_output(self):

        if self.return_code == 0:
            print "{0} Succeeded".format(self.name)
        else:
            print "{0} Failed".format(self.name)  