# PDF-Data-Extraction

PDF data extraction deals with extracting the text data from scanned PDF's where OCR is needed. Python is used to tag a file with a UUID,  split PDF's into unique pages, read the form number from a page, read the page number from a page, crop the image into it's component data parts, run tesseract on these cropped images, and stored into a dataframe. This data will then be stored in HBase. 
