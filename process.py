from im import ImageMagickConverter
from tesseract import Tesseract
from fits import Fits
import os

class GrangeDerivatives():
    def __init__(self, grange_image_dir, filetype="tif"):
        self.grange_image_dir = grange_image_dir
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
            image_output = (os.path.splitext(image_input)[0]+"_TN.jpg").replace("TIFFs", "TNs")
            image_convertor.convert_thumbnail(image_input, image_output)

        if self.islandora_jpg:
            image_output = (os.path.splitext(image_input)[0]+"_JPG.jpg").replace("TIFFs", "JPGs")
            image_convertor.convert_islandora_jpg(image_input, image_output)

    def __ocr_text(self, image_file):

        ocr_text = Tesseract(image_file)
        if self.ocr:
            ocr_text.get_text()

        if self.hocr:
            ocr_text.get_text(config_file="hocr")

    def __fits(self, image_file):

        f = Fits(image_file)
        f.get_fits()


    def __get_files(self):

        self._files_to_process = []
        for root, dirs, files in os.walk(self.grange_image_dir):
            for f in files:
                if f.endswith(self.filetype):
                    self._files_to_process.append(os.path.join(root, f))