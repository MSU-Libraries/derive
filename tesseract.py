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


