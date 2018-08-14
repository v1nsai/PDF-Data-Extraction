# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 11:16:02 2018

@author: Brandon Croarkin
"""

# -*- coding: utf-8 -*-

from wand.image import Image
import os
import re
import sys
import io
    
def PDF2PNG(flowFile, resolution):

    #convert pdf to an image
    with Image(file=flowFile, resolution=resolution) as img:
        
        #loop through pages of PDF
        for i, page in enumerate(img.sequence):
            with Image(page) as im:
                img.alpha_channel = False
                img.format = 'png'

                # I think the best approach would be to save PNGs into a Python array or list, then return that
                # object to the main thread for processing in the next function.  Not sure how though.....
                img.save(filename='test.png')

        # Can write PNG to stdout like this, but probably not what we want to do
        # img.save(flowFile)
        #
        # sys.stdout.buffer.write(flowFile.getvalue())

if __name__ == '__main__':
    folder_location = '/Users/doctor_ew/PycharmProjects/PDF-Data-Extraction'
    output_directory = 'PythonPNGs'
    
    # Put the incoming FlowFile into a dataframe
    flowFile = sys.stdin.buffer.read()
    flowFile = io.BytesIO(flowFile)
    #flowFile = sys.stdin.buffer.read()
    #file = 'i-9_02-02-09(Filled)(OCR).pdf'
    
    #convert PDFs to images
    PDF2PNG(flowFile, resolution=200)

