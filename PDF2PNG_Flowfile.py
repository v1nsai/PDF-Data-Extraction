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

def findFileName(file):
    """
    Removes all .* endings from a file to get just the filename
    """
    (name, ext) = os.path.splitext(file)
    return(name)
    
def PDF2PNG(flowFile, output_directory, resolution = 500):
    """
    Picks up all PDF files in a folder and outputs them as a PNG image
    with 800 resolution as default. This can be edited
    @@param folder_location folder location for where PDFs are stored
    @@param resolution specify density of image conversion
    """
    
    #make a subdirectory to put the image exports if the directory
    #does not already exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)    
        
    #convert pdf to an image
    with Image(filename=flowFile, resolution = resolution) as img:
        #find the filename
        filename = findFileName(flowFile)
        
        #loop through pages of PDF
        for i, page in enumerate(img.sequence):
            with Image(page) as im:
                im.alpha_channel = False
            
                #save PNG export in subfolder
                im.save(filename= output_directory + 
                        '/' + filename + 'page-%s.png' % i)
        
        #delete file so NiFi doesn't repeat process on it
        os.remove(filename + ".pdf")

if __name__ == '__main__':
    folder_location = 'C:\\Users\\Brandon Croarkin\\Documents\\GreenZone\\OCR\\NiFiTesting'
    output_directory = 'PythonPNGs'
    
    # Put the incoming FlowFile into a dataframe
    flowFile = sys.stdin.buffer.read()
    flowFile = io.BytesIO(flowFile)
    #flowFile = sys.stdin.buffer.read()
    #file = 'i-9_02-02-09(Filled)(OCR).pdf'
    
    #convert PDFs to images
    PDF2PNG(flowFile, output_directory, resolution = 200)

