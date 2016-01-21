"""Process derivatives."""
from im import ImageMagickConverter
from text import Tesseract, PdfText
from fits import Fits
import os
import re
import sqlite3 as lite
from datetime import datetime
import logging
import zipfile
import time
import subprocess

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class ProcessDerivatives():

    """Default container class for processing objects."""

    def __init__(self, project_dir, filetype="tif", flat_dir=True,
                 exclude_string="*", update_database=False):
        """Process project_dir, gathering all files of the specified type.

        Positional arguments:
        project_dir (str): location of all files.

        Keyword arguments:
        filetype (str): file type to be collected and processed;
            only tested with 'tif'
        flat_dir (bool): set flat_dir to true if all files are found in the
            specified directory, not subfolders; otherwise, set to false.
        exclude_string(str): string if present in filename or path to exclude
            from processing.
        update_database(bool): for use with django: update sqlite3 database.
        """
        self.project_dir = project_dir
        self.update_database = update_database
        self.filetype = filetype.lower()
        self.flat_dir = flat_dir
        self.exclude_string = exclude_string.lower()

    def get_files(self):
        """Make list of files to process.

        Traverse the supplied directory from __init__ and find all files
        matching the specified type (file ending)
        """
        for root, dirs, files in os.walk(self.project_dir):
            for f in files:
                filepath = os.path.join(root, f)
                if (f.lower().endswith(self.filetype) and
                   self.exclude_string not in filepath.lower()):
                    yield filepath

    def _fits(self, image_file):
        """
        Container for image analysis process.

        Positional arguments:
        image_file (str) -- filename with path.
        """
        f = Fits(image_file)
        f.get_fits(output_file=self._get_output_path("_FITS.xml"))
        self._fits_result = f.return_code

    def _get_output_path(self, deriv_suffix):
        """
        Return output path for derivative file.

        args:
        deriv_suffix (str) -- file ending to append to each created file.
        """
        path_args = [self.derivative_path, self.derivative_basename+deriv_suffix]
        return os.path.join(*path_args)

    def _convert_pdf_images(self, pdf_input):
        """Container for pdf->image converstions.

        args:
            pdf_input(str): path to pdf file

        """
        pdf_convertor = ImageMagickConverter(image_type="pdf")
        if self.tn:

            image_output = self._get_output_path("_TN.jpg")
            pdf_convertor.convert_pdf_tn(pdf_input, image_output)
            self.derive_results.append(pdf_convertor.return_code)

        if self.preview:

            image_output = self._get_output_path("_PREVIEW.jpg")
            pdf_convertor.convert_pdf_preview(pdf_input, image_output)
            self.derive_results.append(pdf_convertor.return_code)

    def _unzip(self, zip_path, unzip_path):
        """Unzip.

        args:
            zip_path(str): path to zip file.
            unzip_path(str): destination to unzip to.
        """
        try:
            unzip_cmds = ['unzip', zip_path, '-d', unzip_path]
            subprocess.check_call(unzip_cmds)
        except Exception as e:
            print "***Failed unzip at {0} with error:".format(zip_path)
            print e
        # z = zipfile.ZipFile(zip_path)
        # z.extractall(unzip_path)

    def _convert_images(self, image_input):
        """Container for image->image conversions.

        Positional arguments:
        image_input (str) -- this should simply be the filename (not full path)
        """
        image_convertor = ImageMagickConverter()

        if self.tn:

            image_output = self._get_output_path("_TN.jpg")
            image_convertor.convert_thumbnail(image_input, image_output)
            self.derive_results.append(image_convertor.return_code)

        if self.jp2:

            image_output = self._get_output_path("_JP2.jp2")
            image_convertor.convert_jp2(image_input, image_output)
            self.derive_results.append(image_convertor.return_code)

        if self.jpeg_low_quality:

            image_output = self._get_output_path("_JPG_LOW.jpg")
            image_convertor.convert_jpeg_low(image_input, image_output)
            self.derive_results.append(image_convertor.return_code)

        if self.jpeg_high_quality:

            image_output = self.__get_output_path("_JPG_HIGH.jpg")
            image_convertor.convert_jpeg_high(image_input, image_output)
            self.derive_results.append(image_convertor.return_code)

        if self.preview:
            image_output = self.__get_output_path("_PREVIEW.jpg")
            image_convertor.convert_preview(image_input, image_output)
            self.derive_results.append(image_convertor.return_code)


class PdfDerivatives(ProcessDerivatives):

    """Methods for creating derivatives of PDF objects."""

    def __init__(self, etd_dir, etd_deriv_dir=None, unzip_files=False,
                 update_database=False):
        """Initiate ProcessDerivatives and prepare for derivatives.

        args:
            etd_dir(str): path to zipped ETDs.

        kwargs:
            etd_deriv_dir(str): path to place unzipped ETDs with derivative files;
                must be supplied if 'unzip_file' is set to True.
            unzip_files(bool): Check ETD directory for files to unzip_files
                before generating derivatives.
        """
        ProcessDerivatives.__init__(self, etd_deriv_dir, filetype="pdf",
                                    update_database=update_database)
        self.etd_dir = etd_dir
        self.etd_deriv_dir = etd_deriv_dir
        if unzip_files:
            self._unzip_etds()

    def _unzip_etds(self):
        """Check to unzipped ETDs and unzip."""
        index = 0
        for etdzip in os.listdir(self.etd_dir):
            if etdzip.endswith("zip"):
                index += 1
                self._check_for_etd(etdzip)
        logging.debug("Completed processing {0} ETDs".format(index))

    def _check_for_etd(self, etdzip):
        """Look for ETD zip in ETD derivatives directory.

        args:
            etdzip(str): ETD zipfilename.
        """
        etd_name = os.path.splitext(etdzip)[0]
        zip_path = os.path.join(self.etd_dir, etdzip)
        zip_year = self._get_year(zip_path)
        unzip_path = os.path.join(self.etd_deriv_dir,
                                  zip_year,
                                  etd_name)

        if not os.path.exists(unzip_path):

            self._unzip(zip_path, unzip_path)
            print "Unzipped {0}".format(zip_path)

        else:
            print "Files already exists for {0}; Skipping.".format(zip_path)

    def _get_year(self, file_path):
        """Get year created for each ETD.

        args:
            zip_path(str): full path to file

        returns:
            year(str): the year the file was created
        """
        seconds_since_epoch = os.path.getctime(file_path)
        return str(time.localtime(seconds_since_epoch)[0])

    def make_pdf_derivatives(self, fits=False, tn=False, preview=False,
                             pdf2text=False, ocr=False, hocr=False):
        """
        Start processing of derivatives.

        Keyword arguments:
        [all] (bool) -- Specify true for each derivative type to be created.
        """
        self.fits = fits
        self.tn = tn
        self.preview = preview
        self.pdf2text = pdf2text
        self.ocr = ocr
        self.hocr = hocr
        failed_objects = 0
        successful_objects = 0
        for pdf in self.get_files():
            print "Processing derivatives for {0}".format(pdf)
            # Get the path and 'basename' of the file,
            # i.e. the filename sans extension
            self.derivative_path, derivative_file = os.path.split(pdf)
            self.derivative_basename = os.path.splitext(derivative_file)[0]
            # List of status codes for all processes; a 0 indicates success.
            self.derive_results = []

            if fits:

                self._fits(pdf)
                self.derive_results.append(self._fits_result)

            if tn or preview:

                self._convert_pdf_images(pdf)

            if ocr or hocr:

                self._ocr_text(pdf)

            if pdf2text:

                pdft = PdfText()
                pdft.get_text(pdf)

            if any(self.derive_results):
                failed_objects += 1
            else:
                successful_objects += 1

        if self.update_database:
            # TODO: flesh this out, move to own class?
            con = lite.connect('/var/www/repo-ingest/db.sqlite3')
            cur = con.cursor()
            cur.execute("UPDATE eulcom_jobstatus SET success_objects = ? WHERE Pid = ?",
                        (successful_objects, self.pidspace))
            cur.execute("UPDATE eulcom_jobstatus SET failed_objects = ? WHERE Pid = ?",
                        (failed_objects, self.pidspace))
            cur.execute("UPDATE eulcom_jobstatus SET jobCompletedTimeStamp=?  WHERE Pid = ?",
                        (datetime.now(), self.pidspace))
            con.commit()
            con.close()


class ImageDerivatives(ProcessDerivatives):

    """Methods for creating derivatives of image files, usually TIFFs."""

    def make_image_derivatives(self, fits=False, tn=False, islandora_jpg=False,
                               jpeg_high_quality=False, jpeg_low_quality=False,
                               jp2=False, ocr=False, hocr=False):
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
        image_methods = [tn, islandora_jpg, jpeg_high_quality,
                         jpeg_low_quality, jp2]

        successful_objects = 0
        failed_objects = 0
        for image_file in self.get_files:
            print "Processing derivatives for {0}".format(image_file)

            # Get the path and 'basename' of the file,
            # i.e. the filename sans extension
            self.derivative_path, derivative_file = os.path.split(image_file)
            self.derivative_basename = os.path.splitext(derivative_file)[0]
            # List of status codes for all processes; a 0 indicates success.
            self.derive_results = []

            if fits:

                self._fits(image_file)
                self.derive_results.append(self._fits_result)

            if any(image_methods):

                self._convert_images(image_file)

            if ocr or hocr:

                self._ocr_text(image_file)

            if any(self.derive_results):
                failed_objects += 1
            else:
                successful_objects += 1

        if self.update_database:
            # TODO: flesh this out, move to own class?
            con = lite.connect('/var/www/repo-ingest/db.sqlite3')
            cur = con.cursor()
            cur.execute("UPDATE eulcom_jobstatus SET success_objects = ? WHERE Pid = ?",
                        (successful_objects, self.pidspace))
            cur.execute("UPDATE eulcom_jobstatus SET failed_objects = ? WHERE Pid = ?",
                        (failed_objects, self.pidspace))
            cur.execute("UPDATE eulcom_jobstatus SET jobCompletedTimeStamp=?  WHERE Pid = ?",
                        (datetime.now(), self.pidspace))
            con.commit()
            con.close()

    def get_Pid(self, pid):
        """To store pid for updating the sucessful objects in sqlite database."""
        self.pidspace = pid

    def _ocr_text(self, image_file, remove_dtd=True):
        """Container for image->txt conversions, including OCR and HOCR.

        Positional arguments:
        image_file (str) -- this should simply be the filename
        remove_dtd (bool) -- the presence of a DTD URL to resolve disrupts the
            xalan XSLT transformation that Gsearch uses; use this parameter to
            remove the DTD reference.
        """
        ocr_text = Tesseract(image_file)
        image_basename = os.path.splitext(image_file)
        if self.ocr:
            ocr_text.get_text(image_basename)
            self.derive_results.append(ocr_text.status_code)

        if self.hocr:
            ocr_text.get_text(image_basename, config_file="hocr")
            if remove_dtd:
                with open(os.path.join(self.project_dir, "OCR", os.path.splitext(os.path.split(image_file)[1])[0]+".html"), "r") as input_file:
                    text = input_file.read()
            
                with open(os.path.join(self.project_dir, "OCR", os.path.splitext(os.path.split(image_file)[1])[0]+".html"), "w") as output_file:
                    output_file.write(re.sub(r'<!DOCTYPE.*?>', "<!DOCTYPE html>", text, flags=re.DOTALL))
