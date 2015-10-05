
## Derivative Creation Tools

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

If the `flat_dir` parameter is set to "True" (this is the default), the code presumes a certain directory structure,
    
        [Project Name]/
            TIFF/
            JP2/
            JPG/
            OCR/
            HOCR/
            FITS/
            
which should be created beforehand. The directory supplied in line `2` below should be to the *project* not the `TIFF` folder.

If `flat_dir` is set to `false`, then derivatives will be created alongside the source file. In this case the directory specified in line `2` below should be any top-level directory above all files to be processed, and the script will look within subfolders to find any images of the type specified.


    from process import ImageDerivatives
    imd = ImageDerivatives("/Volumes/fedcom_ingest/GrangeVisitorTest/")
    imd.make_image_derivatives(hocr=True)

In this example, `flat_dir` is set to false, meaning all files that end with `.tif` will be processed. (The `filetype` keyword argument in the `ImageDerivatives` class instantiations defaults to ".tif".


    from process import ImageDerivatives
    imd = ImageDerivatives("/Volumes/fedcom_ingest/MICHILAC/batch 1/msuspccls_btn_cmp/cmp2/Cropped", flat_dir=False)
    imd.make_image_derivatives(jp2=True, tn=True, jpeg_low_quality=True)

####Hopefully this won't be needed again!
Code to remove the `doctype` declaration from all `HOCR` files. This `DTD` reference was interfering with the `Gsearch` transformation (using `xalan`), causing it to take 1 second for every page.


    import os
    import re
    base_path = "/Volumes/fedcom_ingest/GrangeVisitor/OCR"
    files = [f for f in os.listdir(base_path) if f.endswith("html")]
    for f in files:
        with open(os.path.join(base_path, f), "r") as input_file:
            text = input_file.read()
            
        with open(os.path.join(base_path, f), "w") as output_file:
            output_file.write(re.sub(r'<!DOCTYPE.*?>', "<!DOCTYPE html>", text, flags=re.DOTALL))
