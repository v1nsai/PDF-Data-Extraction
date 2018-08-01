# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 11:08:48 2018

@author: Brandon Croarkin
"""

from wand.image import Image
from wand.color import Color
import os
 
os.chdir('C:\\Users\\Brandon Croarkin\\Documents\\GreenZone\\OCR\\I9 Forms - Filled')

def findFileName(file):
    """
    Removes all .* endings from a file to get just the filename
    """
    (name, ext) = os.path.splitext(file)
    return(name)
    
    
def PDF2PNG(folder_location, resolution = 800):
    """
    Picks up all PDF files in a folder and outputs them as a PNG image
    with 800 resolution as default. This can be edited
    @@param folder_location folder location for where PDFs are stored
    @@param resolution specify density of image conversion
    """
    #Find all PDF files in folder
    PDFs = []
    for file in os.listdir(folder_location):
        if file.endswith(".pdf"):
            PDFs.append(file)
    
    #make a subdirectory to put the image exports if the directory
    #does not already exist
    if not os.path.exists('PythonPNGs'):
        os.makedirs('PythonPNGs')
    
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
                    im.save(filename='PythonPNGs/' + filename + 'page-%s.png' % i)


if __name__ == '__main__':
    folder_location = 'C:\\Users\\Brandon Croarkin\\Documents\\GreenZone\\OCR\\I9 Forms - Filled'
    PDF2PNG(folder_location, resolution = 800)
    
    

#########TESTING
    
#testing the alpha remove
im = Image(filename='i-9_02-02-09(Filled).pdf', resolution=200)
for i, page in enumerate(im.sequence):
    with Image(page) as page_image:
        page_image.alpha_channel = False
        page_image.save(filename='PythonPNGs/temp3page-%s.png' % i)
        
#testing out the splitting feature            
with Image(filename='i-9_02-02-09(Filled).pdf', resolution = 200) as img:
    img.compression_quality = 99
    img.alpha_channel = 'remove'
    #make a subdirectory to put the image exports if the directory
    #does not already exist
    if not os.path.exists('PythonPNGs'):
        os.makedirs('PythonPNGs')
    #save PNG export in folder
    img.save(filename='PythonPNGs/temp3.png')
    
#loop through PDF files and convert them to PNG
for i in range(len(PDFs)):
    with Image(filename=PDFs[i], resolution = resolution) as img:
        #set image compression quality
        img.compression_quality = 99
        img.alpha_channel = 'remove'
        img.background_color = Color('white')
            
        #find the filename
        filename = findFileName(PDFs[i])
        
        #make a subdirectory to put the image exports if the directory
        #does not already exist
        if not os.path.exists('PythonPNGs'):
            os.makedirs('PythonPNGs')
                
        #save PNG export in subfolder
        img.save(filename='PythonPNGs/' + filename + '.png')