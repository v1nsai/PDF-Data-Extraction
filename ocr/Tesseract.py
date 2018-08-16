# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 15:21:11 2018

@author: Brandon Croarkin
"""

import pytesseract
import os
import re
import pandas as pd
from pandas import ExcelWriter

os.chdir('C:\\Users\\Brandon Croarkin\\Documents\\GreenZone\\OCR\\PythonCroppedImages')

def tesseract(image_folder_location):
    """
    @@param folder_location folder location for where cropped images are stored
    for tesseract to run on them
    """
    #create list of png images to crop
    croppedImages = []
    for image in os.listdir(image_folder_location):
        if image.endswith(".png"):
            croppedImages.append(image)
    
    #create empty lists to add data to
    file = []
    field = []
    text = []
    cleaned_text = []
    
    #run tesseract on all of the images 
    for i in range(len(croppedImages)):
        #pulling out the file name from beginning of string
        file.append(re.search(r'^(.+?)_',croppedImages[i]).group())
        #pulling out the field name from middle of string
        field.append(re.search(r'(?<=\_)(.*?)(?=\.)',croppedImages[i]).group())
        #running tesseract on the image
        text.append(pytesseract.image_to_string(Image.open(croppedImages[i])))
        
    #pulling all the information after the heading
    for i in range(len(text)):
        cleaned_text.append(re.search(r'[^\n]+$',text[i]).group())

    #create dataframe of the values
    df = pd.DataFrame({'File': file, 
                  'Field': field, 
                  'TesseractText': text, 
                  'CleanedText': cleaned_text})
    
    #format dataframe into the Excel format 
    df_formatted = df.pivot(index = 'File', columns = 'Field', values = 'CleanedText')    

    #clean dataframe
    for i in range(len(df_formatted)):
       df_formatted['DateOfBirth'] = df_formatted['DateOfBirth'][i].replace('O','0').replace(" ", "")
       df_formatted['Telephone'] = df_formatted['Telephone'][i].replace('(','').replace(')',"").replace(" ", "").replace("-","")
    
    #output file
    writer = ExcelWriter('i9Export.xlsx')
    df_formatted.to_excel(writer)
    writer.save()

if __name__ == '__main__':
    folder_location = 'C:\\Users\\Brandon Croarkin\\Documents\\GreenZone\\OCR\\PythonCroppedImages'
    tesseract(folder_location)



        

    









                