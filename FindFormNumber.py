# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 15:06:56 2018

@author: Brandon Croarkin
"""

import pytesseract
from PIL import Image
import os
import re
import pandas as pd
import numpy as np
from shutil import copyfile

#listing out what page the information we want is on for each form
page_info = {'05/07/87': 0,
             '11-21-91(L)': 0,
             '11-21-91(R)': 1,
             '05/31/05': 1,
             '06/05/07': 2,
             '02/02/09': 3,
             '08/07/09': 3,
             '03/08/13': (6,7),
             '11/14/2016': (0,1),
             '07/17/17': (0,1)
             }

def crop(image_path, coords, saved_location):
    """
    @param image_path: The path to the image to edit
    @param coords: A tuple of x/y coordinates (x1, y1, x2, y2)
    @param saved_location: Path to save the cropped image
    """
    image_obj = Image.open(image_path)
    cropped_image = image_obj.crop(coords)
    cropped_image.save(saved_location)
    cropped_image.show()

def findFileName(file):
    """
    Removes all .* endings from a file to get just the filename
    """
    (name, ext) = os.path.splitext(file)
    return(name)

def findFormNumber(file):
    """
    @@file - the file to find the form number of
    This function takes in a file and spits out the form number associated with it
    """
    #crop bottom of image
    image = file
    im = Image.open(file)
    width, height = im.size
    crop(image, (.04*width,.955*height,.95*width,.98*height), 'FormNumber/FormNo.png')
    
    #run tesseract on crop
    text = pytesseract.image_to_string(Image.open('FormNumber/FormNo.png'))
    
    #clean output to just pull revision date with either dd/mm/yy or dd-mm-yy format
    matches = re.findall('(\d{2}[\/ ](\d{2}|January|Jan|February|Feb|March|Mar|April|Apr|May|May|June|Jun|July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec)[\/ ]\d{2,4})'
                     , text)

    if matches:
        for match in matches:
            return(match[0])
    elif not matches:
        print('nothing found in first crop')
        crop(image, (.04*width,.925*height,.95*width,.955*height), 'FormNumber/FormNo.png')
    
        #run tesseract on crop
        text = pytesseract.image_to_string(Image.open('FormNumber/FormNo.png'))
    
        #clean output to just pull revision date with either dd/mm/yy or dd-mm-yy format
        matches = re.findall('(\d{2}[\/ ](\d{2}|January|Jan|February|Feb|March|Mar|April|Apr|May|May|June|Jun|July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec)[\/ ]\d{2,4})'
                     , text)
        
        #output answer
        for match in matches:
            return(match[0])
    
    if not matches:
        print('nothing found in second crop')
        crop(image, (.04*width,.907*height,.95*width,.925*height), 'FormNumber/FormNo.png')
    
        #run tesseract on crop
        text = pytesseract.image_to_string(Image.open('FormNumber/FormNo.png'))
    
        #clean output to just pull revision date with either dd/mm/yy or dd-mm-yy format
        matches = re.findall('(\d{2}[\/ ](\d{2}|January|Jan|February|Feb|March|Mar|April|Apr|May|May|June|Jun|July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec)[\/ ]\d{2,4})'
                     , text)
        
        #output answer
        for match in matches:
            return(match[0])
            
    if not matches:
        print('nothing found in third crop. Trying dd-mm-yyyy format.')
        crop(image, (.04*width,.925*height,.95*width,.955*height), 'FormNumber/FormNo.png')
    
        #run tesseract on crop
        text = pytesseract.image_to_string(Image.open('FormNumber/FormNo.png'))
    
        #clean output to just pull revision date with either dd/mm/yy or dd-mm-yy format
        matches = re.findall('(\d{2}[\- ](\d{2}|January|Jan|February|Feb|March|Mar|April|Apr|May|May|June|Jun|July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec)[\- ]\d{2,4})'
                     , text)
        
        #output answer
        for match in matches:
            return(match[0])
            
    if not matches:
        print('nothing found in forth crop.')
        crop(image, (.04*width,.80*height,.95*width,.83*height), 'FormNumber/FormNo.png')
    
        #run tesseract on crop
        text = pytesseract.image_to_string(Image.open('FormNumber/FormNo.png'))
    
        #clean output to just pull revision date with either dd/mm/yy or dd-mm-yy format
        matches = re.findall('(\d{2}[\- ](\d{2}|January|Jan|February|Feb|March|Mar|April|Apr|May|May|June|Jun|July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec)[\- ]\d{2,4})'
                     , text)
        
        #output answer
        for match in matches:
            return(match[0])
    
    if not matches: 
        print('nothing found in fifth crop')
        crop(image, (.04*width,.955*height,.95*width,.98*height), 'FormNumber/FormNo.png')
    
        #run tesseract on crop
        text = pytesseract.image_to_string(Image.open('FormNumber/FormNo.png'))
    
        #clean output to just pull revision date with either dd/mm/yy or dd-mm-yy format
        matches = re.findall('(\d{2}[\- ](\d{2}|January|Jan|February|Feb|March|Mar|April|Apr|May|May|June|Jun|July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec)[\- ]\d{2,4})'
                     , text)
        
        #output answer
        for match in matches:
            return(match[0])  
            
    else:
        return('not found')

def findPageNumber(file):
    """
    @@file file to determine page number of
    This function intakes a file and spits out the page number based on
    the file name.
    Note: the file name should already contain the page number in the filename
    due to the PDF2PNG function that attaches the page number to the filename.
    This function is just extracting that number from the filename.
    """
    matches = re.findall('(?<=page-)(.*)(?=.png)', file)
    matches = np.asarray(matches)
    matches = int(matches)
    return(matches)
    
def routeDataPages(file):
    """
    @@file file to determine whether it should be routed forward
    """
    #make a subdirectory to put the image exports if the directory
    #does not already exist
    if not os.path.exists('FilesToCrop'):
        os.makedirs('FilesToCrop')
    
    #find form number
    form_number = findFormNumber(file)
    
    #find page number
    page_number = findPageNumber(file)
    
    #if the page number of file is the matches with the dictionary
    #values for the page of the form with data, then it is routed
    #to a new directory to be cropped
    if isinstance(page_info[form_number], int):
        if page_info[form_number] == page_number:
            copyfile(file, 'FilesToCrop/' + file)
            print("Success! File has been routed.")
        else:
            print("Not a data page")
    else:
        if page_info[form_number][0] == page_number or page_info[form_number][1] == page_number:
            copyfile(file, 'FilesToCrop/' + file)
            print("Success! File has been routed.")
        else:
            print("Not a data page")

    
#############TESTING

###test routeDataPages parts
form_number = findFormNumber('i-9_02-02-09(Filled)page-3.png')
page_number = findPageNumber('i-9_02-02-09(Filled)page-3.png')
len(page_info[form_number])

#should copy to FilesToCrop folder and give success message
routeDataPages('i-9_02-02-09(Filled)page-3.png')

routeDataPages('i-9_03-08-13(Filled)page-6.png')
routeDataPages('i-9_03-08-13(Filled)page-7.png')

#test routeDataPages on forms with two data pages
form_number = findFormNumber('i-9_11-14-16(Filled)page-0.png')
page_number = findPageNumber('i-9_11-14-16(Filled)page-0.png')

if isinstance(page_info[form_number], int):
     if page_info[form_number] == page_number:
        print("Integer Data page")
     else:
        print("Not an integer data page")
else:
     if page_info[form_number][0] == page_number or page_info[form_number][1] == page_number:
        print("Tuple data page")
     else:
        print("Not a tuple data page")
        
type(page_info[form_number])

#should print "Not a data page"
routeDataPages('i-9_02-02-09(Filled)page-2.png')

###test routeDataPages function on all files in folder
for i in range(len(images)):
    #route data pages
    routeDataPages(images[i])


###test form number function on all files in folder
        
#Make a vector of PNG files in a directory so it can repeat 
#process on all files in directory
images = []
folder_location = 'C:\\Users\\Brandon Croarkin\\Documents\\GreenZone\\OCR\\I9 Forms - Filled\\PythonPNGs'
for image in os.listdir(folder_location):
    if image.endswith(".png"):
        images.append(image)

#make empty lists that we can make into a dataframe later
filenames = []
form_no = []

#loop through files in folder and find their form number
for i in range(len(images)):
    #find the filename
    filenames.append(findFileName(images[i]))

    #find the form number
    form_no.append(findFormNumber(images[i]))

#create dataframe of the values
df = pd.DataFrame({'File': filenames, 
                  'Form_No': form_no})
    
###test structure
def findFormNumber(file):
    #crop bottom of image
    image = file
    im = Image.open(file)
    width, height = im.size
    crop(image, (.04*width,.955*height,.95*width,.98*height), 'FormNumber/FormNo.png')
    
    #run tesseract on crop
    text = pytesseract.image_to_string(Image.open('FormNumber/FormNo.png'))
    
    #clean output to just pull revision date with either dd/mm/yy or dd-mm-yy format
    matches = re.findall('(\d{2}[\/ ](\d{2}|January|Jan|February|Feb|March|Mar|April|Apr|May|May|June|Jun|July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec)[\/ ]\d{2,4})'
                     , text)

    if matches:
        for match in matches:
            return(match[0])
    elif not matches:
        print('nothing found in first crop')
        crop(image, (.04*width,.925*height,.95*width,.955*height), 'FormNumber/FormNo.png')
    
        #run tesseract on crop
        text = pytesseract.image_to_string(Image.open('FormNumber/FormNo.png'))
    
        #clean output to just pull revision date with either dd/mm/yy or dd-mm-yy format
        matches = re.findall('(\d{2}[\/ ](\d{2}|January|Jan|February|Feb|March|Mar|April|Apr|May|May|June|Jun|July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec)[\/ ]\d{2,4})'
                     , text)
        
        #output answer
        for match in matches:
            return(match[0])
    
    if not matches:
        print('nothing found in second crop')
        crop(image, (.04*width,.907*height,.95*width,.925*height), 'FormNumber/FormNo.png')
    
        #run tesseract on crop
        text = pytesseract.image_to_string(Image.open('FormNumber/FormNo.png'))
    
        #clean output to just pull revision date with either dd/mm/yy or dd-mm-yy format
        matches = re.findall('(\d{2}[\/ ](\d{2}|January|Jan|February|Feb|March|Mar|April|Apr|May|May|June|Jun|July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec)[\/ ]\d{2,4})'
                     , text)
        
        #output answer
        for match in matches:
            return(match[0])
            
    if not matches:
        print('nothing found in third crop. Trying dd-mm-yyyy format.')
        crop(image, (.04*width,.925*height,.95*width,.955*height), 'FormNumber/FormNo.png')
    
        #run tesseract on crop
        text = pytesseract.image_to_string(Image.open('FormNumber/FormNo.png'))
    
        #clean output to just pull revision date with either dd/mm/yy or dd-mm-yy format
        matches = re.findall('(\d{2}[\- ](\d{2}|January|Jan|February|Feb|March|Mar|April|Apr|May|May|June|Jun|July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec)[\- ]\d{2,4})'
                     , text)
        
        #output answer
        for match in matches:
            return(match[0])
            
    if not matches:
        print('nothing found in forth crop.')
        crop(image, (.04*width,.80*height,.95*width,.83*height), 'FormNumber/FormNo.png')
    
        #run tesseract on crop
        text = pytesseract.image_to_string(Image.open('FormNumber/FormNo.png'))
    
        #clean output to just pull revision date with either dd/mm/yy or dd-mm-yy format
        matches = re.findall('(\d{2}[\- ](\d{2}|January|Jan|February|Feb|March|Mar|April|Apr|May|May|June|Jun|July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec)[\- ]\d{2,4})'
                     , text)
        
        #output answer
        for match in matches:
            return(match[0])
    
    if not matches: 
        print('nothing found in fifth crop')
        crop(image, (.04*width,.955*height,.95*width,.98*height), 'FormNumber/FormNo.png')
    
        #run tesseract on crop
        text = pytesseract.image_to_string(Image.open('FormNumber/FormNo.png'))
    
        #clean output to just pull revision date with either dd/mm/yy or dd-mm-yy format
        matches = re.findall('(\d{2}[\- ](\d{2}|January|Jan|February|Feb|March|Mar|April|Apr|May|May|June|Jun|July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec)[\- ]\d{2,4})'
                     , text)
        
        #output answer
        for match in matches:
            return(match[0])  
            
    else:
        return('not found')
            
        
findFormNumber('i-9_11-21-91(R)(Filled)page-2.png')
    
##Below is just for testing for cropping for form number
if __name__ == '__main__':
   image = 'i-9_07-17-17(Filled)page-0.png'
   im = Image.open('i-9_07-17-17(Filled)page-0.png')
   width, height = im.size
   crop(image, (.04*width,.91*height,.95*width,.925*height), 'FormNumber/FormNo.png')
   
#run tesseract on a cropped image
text = pytesseract.image_to_string(Image.open('FormNumber/FormNo.png'))

#extract the rev date from the string
matches = re.findall('(\d{2}[\/ ](\d{2}|January|Jan|February|Feb|March|Mar|April|Apr|May|May|June|Jun|July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec)[\/ ]\d{2,4})'
                     , text)

for match in matches:
    print(match[0])

#extract the rev date from the string (version 2)
matches = re.search(r'\d{2}-\d{2}-\d{2}', text)
matches