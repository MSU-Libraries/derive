"""Text extraction class(es)."""
from derivatives import Derivatives
from PyPDF2 import PdfFileReader

class Tesseract(Derivatives):

    """Class for handling OCR requests."""

    def __init__(self, file_path):
        """Init."""
        self.file_path = file_path

    def get_text(self, output_basename, config_file=""):
        """Run with config_file='hocr' for output in HTML.

        args:
            output_basename(str): the complete name of the file to write, sans extension.
            Tesseract will add the appropriate extension.
        kwargs:
            config_file(str): the config file for desired output. blank for OCR, 'hocr'
            for HTML output.
        """
        self.output_basename = output_basename
        self.name = "Text generation {0}".format(config_file)
        self.cmds = ["tesseract", self.file_path, self.output_basename, config_file]
        self.print_process()
        self.return_code = self.run_cmds()
        self.print_output()


class PdfText(Derivatives):

    """Extract text from PDF."""

    def __init__(self):
        """Init."""
        pass

    @staticmethod
    def get_text(self, file_path):
        """Run with config_file='hocr' for output in HTML.

        args:
            file_path(str): the complete name of the file to get text from.
        """
        full_text = ""
        full_text_file_location = file_path.replace(".pdf", ".txt")
        try:
            with open(file_path, "rb") as f:
                a = PdfFileReader(f)
                for i in range(a.getNumPages()):
                    full_text += a.getPage(i).extractText()
            with open(full_text_file_location, "w") as f:
                f.write(full_text.encode("UTF-8"))
            self.return_code = 0

        except Exception as e:
            self.return_code = 1
            print "Error: ".format(e)
