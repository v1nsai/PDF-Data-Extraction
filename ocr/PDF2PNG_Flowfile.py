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
    # Declare the empty list of PNGs
    PNGs = []

    #convert pdf to an image
    with Image(file=flowFile, resolution=resolution) as img:
        
        #loop through pages of PDF and convert each into a separate PNG
        for i, page in enumerate(img.sequence):
            with Image(page) as im:
                img.alpha_channel = False
                img.format = 'png'

                # create a list of PNGs to return to the main thread to be passed to the next function
                # Haven't tested this, a File() object might be more appropriate but I think either will work
                swapPNG = io.BytesIO()
                img.save(swapPNG)
                PNGs = PNGs.append(swapPNG)
        return PNGs


        # Can write PNG to stdout like this, but probably not what we want to do
        # img.save(flowFile)
        #
        # sys.stdout.buffer.write(flowFile.getvalue())

if __name__ == '__main__':

    # Put the incoming FlowFile into a dataframe
    flowFile = sys.stdin.buffer.read()
    flowFile = io.BytesIO(flowFile)
    
    #convert PDFs to images
    PNGs = PDF2PNG(flowFile, resolution=200)

    for png in PNGs: