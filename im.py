#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
COPYRIGHT © 2015
MICHIGAN STATE UNIVERSITY BOARD OF TRUSTEES
ALL RIGHTS RESERVED
 
PERMISSION IS GRANTED TO USE, COPY, CREATE DERIVATIVE WORKS AND REDISTRIBUTE
THIS SOFTWARE AND SUCH DERIVATIVE WORKS FOR ANY PURPOSE, SO LONG AS THE NAME
OF MICHIGAN STATE UNIVERSITY IS NOT USED IN ANY ADVERTISING OR PUBLICITY
PERTAINING TO THE USE OR DISTRIBUTION OF THIS SOFTWARE WITHOUT SPECIFIC,
WRITTEN PRIOR AUTHORIZATION.  IF THE ABOVE COPYRIGHT NOTICE OR ANY OTHER
IDENTIFICATION OF MICHIGAN STATE UNIVERSITY IS INCLUDED IN ANY COPY OF ANY
PORTION OF THIS SOFTWARE, THEN THE DISCLAIMER BELOW MUST ALSO BE INCLUDED.
 
THIS SOFTWARE IS PROVIDED AS IS, WITHOUT REPRESENTATION FROM MICHIGAN STATE
UNIVERSITY AS TO ITS FITNESS FOR ANY PURPOSE, AND WITHOUT WARRANTY BY
MICHIGAN STATE UNIVERSITY OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING
WITHOUT LIMITATION THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE. THE MICHIGAN STATE UNIVERSITY BOARD OF TRUSTEES SHALL
NOT BE LIABLE FOR ANY DAMAGES, INCLUDING SPECIAL, INDIRECT, INCIDENTAL, OR
CONSEQUENTIAL DAMAGES, WITH RESPECT TO ANY CLAIM ARISING OUT OF OR IN
CONNECTION WITH THE USE OF THE SOFTWARE, EVEN IF IT HAS BEEN OR IS HEREAFTER
ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
 
Written by Devin Higgins, 2015
(c) Michigan State University Board of Trustees
Licensed under GNU General Public License (GPL) Version 2.
"""
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
