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
from im import ImageMagickConverter
from tesseract import Tesseract
from fits import Fits
import os

class GrangeDerivatives():
    def __init__(self, grange_image_dir, filetype="tif"):
        self.grange_image_dir = grange_image_dir
        self.grange_dir = grange_image_dir
        self.filetype=filetype
        self.__get_files()

    def make_issue_derivatives(self):
        pass


    def make_page_derivatives(self, fits=True, tn=True, islandora_jpg=True, jpeg_high_quality=False, jpeg_low_quality=False, jp2=False, ocr=True, hocr=True):
        self.tn = tn
        self.islandora_jpg = islandora_jpg
        self.jpeg_low_quality = jpeg_low_quality
        self.jpeg_high_quality = jpeg_high_quality
        self.jp2 = jp2
        self.ocr = ocr
        self.hocr = hocr

        image_methods = [tn, islandora_jpg, jpeg_high_quality, jpeg_low_quality, jp2]
        for image_file in self._files_to_process:
            print "Processing derivatives for {0}".format(image_file)

            if fits:

                self.__fits(image_file)
            
            if any(image_methods):
                
                self.__convert_images(image_file)

            if ocr or hocr:

                self.__ocr_text(image_file)



    def __convert_images(self, image_input):

        image_convertor = ImageMagickConverter()

        if self.tn:
            image_output = os.path.join(self.grange_dir, "TN")+os.path.splitext(os.path.split(image_input)[1])[0]+"_TN.jpg"
            image_convertor.convert_thumbnail(image_input, image_output)

        if self.jp2:
            image_output = os.path.join(self.grange_dir.replace("TIFF", "JP2"), os.path.splitext(os.path.split(image_input)[1])[0]+"_JP2.jp2")
            image_convertor.convert_jp2(image_input, image_output)

        if self.jpeg_low_quality:
            image_output = os.path.join(self.grange_dir, "JPG")+os.path.splitext(os.path.split(image_input)[1])[0]+"_JPG_LOW.jpg"
            image_convertor.convert_jpeg_low(image_input, image_output)

    def __ocr_text(self, image_file):

        ocr_text = Tesseract(image_file)
        if self.ocr:
            ocr_text.get_text(output_basename=os.path.join(self.grange_dir, "OCR")+os.path.splitext(os.path.split(image_file)[1])[0])

        if self.hocr:
            ocr_text.get_text(output_basename=os.path.join(self.grange_dir, "OCR")+os.path.splitext(os.path.split(image_file)[1])[0], config_file="hocr")

    def __fits(self, image_file):

        f = Fits(image_file)
        f.get_fits(output_file=os.path.join(self.grange_dir, "FITS")+os.path.splitext(os.path.split(image_file)[1])[0])


    def __get_files(self):

        self._files_to_process = []
        for root, dirs, files in os.walk(self.grange_image_dir):
            for f in files:
                if f.endswith(self.filetype):
                    self._files_to_process.append(os.path.join(root, f))