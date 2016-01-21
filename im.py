"""Build commands to create derivatives."""

from derivatives import Derivatives


class ImageMagickConverter(Derivatives):

    """Methods for generating image derivatives with ImageMagick.

    All conversion methods require an input an output path as strings.
    """

    def __init__(self, image_type="tif"):
        """Initialize class.

        kwargs:
            image_type(str): type of image to process, so far only tif support.
        """
        self.config_section = image_type
        self.get_configs()

    def convert_jpeg_low(self, input_tif, output_jpg):
        """Protocol for conversion."""
        self.name = "JPEG low-quality conversion"
        self.cmds = self._create_cmds(self.jpeg_low, input_tif, output_jpg)
        self.print_process()
        self.return_code = self.run_cmds()
        self.print_output()

    def convert_jpeg_high(self, input_tif, output_jpg):
        """Protocol for conversion."""
        self.name = "JPEG high-quality conversion"
        self.cmds = self._create_cmds(self.jpeg_high, input_tif, output_jpg)
        self.print_process()
        self.return_code = self.run_cmds()
        self.print_output()

    def convert_thumbnail(self, input_tif, output_jpg):
        """Protocol for conversion."""
        self.name = "Thumbnail conversion"
        self.cmds = self._create_cmds(self.thumbnail, input_tif, output_jpg)
        self.print_process()
        self.return_code = self.run_cmds()
        self.print_output()

    def convert_jp2(self, input_tif, output_jpg):
        """Protocol for conversion."""
        self.name = "JP2 conversion"
        self.cmds = self._create_cmds(self.jp2, input_tif, output_jpg)
        self.print_process()
        self.return_code = self.run_cmds()
        self.print_output()

    def convert_pdf_preview(self, input_file, output_jpg):
        """Protocol for conversion."""
        self.name = "PREVIEW conversion"
        self.cmds = self._create_cmds(self.pdf_preview, input_file+"[0]", output_jpg)
        self.print_process()
        self.return_code = self.run_cmds()
        self.print_output()

    def convert_pdf_tn(self, input_file, output_jpg):
        """Protocol for conversion."""
        self.name = "Thumbnail conversion"
        self.cmds = self._create_cmds(self.pdf_tn, input_file+"[0]", output_jpg)
        self.print_process()
        self.return_code = self.run_cmds()
        self.print_output()
