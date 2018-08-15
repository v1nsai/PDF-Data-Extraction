# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 11:08:48 2018

@author: Brandon Croarkin
"""

from wand.image import Image
import os

def findFileName(file):
    """
    Removes all .* endings from a file to get just the filename
    """
    (name, ext) = os.path.splitext(file)
    return(name)
    
def PDF2PNG(folder_location, output_directory, resolution = 800):
    """
    Picks up all PDF files in a folder and outputs them as a PNG image
    with 800 resolution as default. This can be edited
    @@param folder_location folder location for where PDFs are stored
    @@param resolution specify density of image conversion
    """
    #set the working directory to the folder_location
    os.chdir(folder_location)
    
    #make a subdirectory to put the image exports if the directory
    #does not already exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)    
        
    #Find all PDF files in folder
    PDFs = []
    for file in os.listdir(folder_location):
        if file.endswith(".pdf"):
            PDFs.append(file)
    
    #loop through PDF files and convert them to PNG
    for i in range(len(PDFs)):
        with Image(filename=PDFs[i], resolution = resolution) as img:
            #find the filename
            filename = findFileName(PDFs[i])
            
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
    PDF2PNG(folder_location, output_directory, resolution = 600)