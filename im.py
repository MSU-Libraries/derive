#!/usr/bin/env python
# -*- coding: utf-8 -*-

from derivatives import Derivatives
import os
import subprocess

class ImageMagickConverter(Derivatives):

    def __init__(self, image_type="tif"):

        self.config_section = image_type
        self.get_configs()

    def convert_jpeg_low(self, input_tif, output_jpg):

        self.name = "JPEG low-quality conversion"
        self.cmds = self.jpeg_low.replace("image.tif", input_tif).replace("image.jpg", output_jpg).split()
        self.print_process()
        self.return_code = self.run_cmds()
        self.print_output()

    def convert_jpeg_high(self, input_tif, output_jpg):

        self.name = "JPEG high-quality conversion"
        self.cmds = self.jpeg_high.replace("image.tif", input_tif).replace("image.jpg", output_jpg).split()
        self.print_process()
        self.return_code = self.run_cmds()
        self.print_output()

    def convert_thumbnail(self, input_tif, output_jpg):

        self.name = "Thumbnail conversion"
        self.cmds = self.thumbnail.replace("image.tif", input_tif).replace("image.jpg", output_jpg).split()
        self.print_process()
        self.return_code = self.run_cmds()
        self.print_output()

    def convert_jp2(self, input_tif, output_jpg):

        self.name = "JP2 conversion"
        self.cmds = self.jp2.replace("image.tif", input_tif).replace("image.jp2", output_jpg).split()
        self.print_process()
        self.return_code = self.run_cmds()
        self.print_output()
