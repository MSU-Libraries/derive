
##Derivative Creation Tools

Use the code below to generate derivatives of `TIF` files.

In line `3` below, specify the derivative options you'd like to run. Currently supported outputs, along with the parameter used to invoke them, are:

+    JP2 (jp2)
+    Low quality JPG (jpeg_low_quality)
+    Thumbnail (tn)
+    FITS file metadata (fits)
+    OCR (ocr)
+    HOCR (hocr)

Appropriate tools must first be installed: ImageMagick, FITS, or Tesseract, depending on which derivatives are needed.

+ Image derivatives are generated using `ImageMagick`  commands found in the `settings.cfg` file. 
+ FITS metadata generated via FITS tool. Location of `fits.sh` should be specified in `settings.cfg`.
+ OCR and HOCR text files are generated using `Tesseract`.

The code presumes a certain directory structure,
    
        [Project Name]/
            TIFF/
            JP2/
            JPG/
            OCR/
            HOCR/
            FITS/
            
which should be created beforehand. The directory supplied in line `2` below should be to the *project* not the `TIFF` folder.


    from process import ImageDerivatives
    imd = ImageDerivatives("/link/to/project/dir")
    imd.make_image_derivatives(fits=True, tn=True, ocr=True)
