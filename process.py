#!/usr/bin/env python
# -*- coding: utf-8 -*-

from im import ImageMagickConverter
from tesseract import Tesseract
from fits import Fits
import os
import re

class ImageDerivatives():
    """Pull together a set of methods for creating derivatives of image files, usually TIFFs."""

    def __init__(self, project_dir, filetype="tif", flat_dir=True):
        """
        Initialize processing of project_dir, gathering all files of the specified type.

        Positional arguments:
        project_dir (str) -- location of all sub-directories, i.e. TIFF, TN, JPG, etc, or parent directory of all files to be processed, if flat_dir is False.

        Keyword arguments:
        filetype (str) -- file type to be collected and processed; only tested with 'tif'
        flat_dir (bool) -- set flat_dir to true if all files are found in the specified directory, not subfolders; otherwise, set to false.
        """
        self.project_dir = project_dir
        self.filetype=filetype
        self.flat_dir = flat_dir
        self.__get_files()


    def make_image_derivatives(self, fits=False, tn=False, islandora_jpg=False, jpeg_high_quality=False, jpeg_low_quality=False, jp2=False, ocr=False, hocr=False):
        """
        Start processing of derivatives.

        Keyword arguments:
        [all] (bool) -- Specify true for each derivative type to be created.
        """
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
        """
        Container for image->image conversions. 

        Positional arguments:
        image_input (str) -- this should simply be the filename (not full path)
        """

        image_convertor = ImageMagickConverter()

        # Get the path and 'basename' of the file, i.e. the filename sans extension.
        self.derivative_path, derivative_filename = os.path.split(image_input)
        self.derivative_basename = os.path.splitext(derivative_filename)[0]
        
        if self.tn:
            
            image_output = self.__get_output_path("TN")
            image_convertor.convert_thumbnail(image_input, image_output)

        if self.jp2:
            
            image_output = self.__get_output_path("JP2")
            image_convertor.convert_jp2(image_input, image_output)

        if self.jpeg_low_quality:
    
            image_output = self.__get_output_path("JPG")
            image_convertor.convert_jpeg_low(image_input, image_output)

    def __ocr_text(self, image_file, remove_dtd=True):
        """
        Container for image->txt conversions, including OCR and HOCR. 

        Positional arguments:
        image_file (str) -- this should simply be the filename
        remove_dtd (bool) -- the presence of a DTD URL to resolve disrupts the xalan XSLT transformation that Gsearch uses; use this parameter to remove the DTD reference.
        """

        ocr_text = Tesseract(image_file)
        if self.ocr:
            ocr_text.get_text(output_basename=os.path.join(self.project_dir, "OCR")+os.path.splitext(os.path.split(image_file)[1])[0])

        if self.hocr:
            ocr_text.get_text(output_basename=os.path.join(self.project_dir, "OCR")+os.path.splitext(os.path.split(image_file)[1])[0], config_file="hocr")
            if remove_dtd:
                with open(os.path.join(self.project_dir, "OCR", os.path.splitext(os.path.split(image_file)[1])[0]+".html"), "r") as input_file:
                    text = input_file.read()
            
                with open(os.path.join(self.project_dir, "OCR", os.path.splitext(os.path.split(image_file)[1])[0]+".html"), "w") as output_file:
                    output_file.write(re.sub(r'<!DOCTYPE.*?>', "<!DOCTYPE html>", text, flags=re.DOTALL))

    def __fits(self, image_file):
        """
        Container for image analysis process. 

        Positional arguments:
        image_file (str) -- this should simply be the filename
        """
        f = Fits(image_file)
        f.get_fits(output_file=os.path.join(self.project_dir, "FITS", os.path.splitext(os.path.split(image_file)[1])[0]+"_FITS.xml"))


    def __get_files(self):
        """Traverse the supplied directory from __init__ and find all files matching the specified type (file ending)"""

        self._files_to_process = []
        # Method for working only with 1 folder.
        if self.flat_dir:
            for fp in os.listdir(os.path.join(self.project_dir, "TIFF")):
            	if fp.endswith(self.filetype):
            		self._files_to_process.append(os.path.join(self.project_dir, "TIFF", fp))
        # Method for traversing a tree to get all files. 
        else:
            for root, dirs, files in os.walk(self.project_dir):
                for f in files:
                    if f.endswith(self.filetype):
                        self._files_to_process.append(os.path.join(root, f))
        

    def __get_output_path(self, deriv_type):
        """
        Return output path for derivative file.

        args:
        deriv_type (str) -- shorthand for type of derivative, e.g. "TN", "JPG", "JP2", etc.
        """
        deriv_suffix = {
                        "TN":"_TN.jpg",
                        "JPG":"_JPG.jpg",
                        "JP2":"_JP2.jpg",
        }

        if self.flat_dir:
            path_args = [self.derivative_path, deriv_type, self.derivative_basename+deriv_suffix[deriv_type]]

        else:
            path_args = [self.derivative_path, self.derivative_basename+deriv_suffix[deriv_type]]

        return os.path.join(*path_args)
