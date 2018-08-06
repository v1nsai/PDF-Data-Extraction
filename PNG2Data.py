# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 13:39:18 2018

@author: Brandon Croarkin
"""

import pytesseract
import PIL
import os
import re
import pandas as pd
import numpy as np
from pandas import ExcelWriter

def crop(image_path, coords, saved_location):
    """
    @param image_path: The path to the image to edit
    @param coords: A tuple of x/y coordinates (x1, y1, x2, y2)
    @param saved_location: Path to save the cropped image
    """
    image_obj = PIL.Image.open(image_path)
    cropped_image = image_obj.crop(coords)
    cropped_image.save(saved_location)
    cropped_image.show()

def findFileName(file):
    """
    Removes all .* endings from a file to get just the filename
    """
    (name, ext) = os.path.splitext(file)
    return(name)

def findOriginalFileName(file):
    """
    Removes all .* endings from a file to get just the filename and then removes
    extra fields added, which starts with the page number.
    Files will be in format [original filename][page number][field name].png
    Want to extract just the [original filename]

    """
    (name, ext) = os.path.splitext(file)
    matches = re.findall('.+?(?=page)', name)
    return(matches[0])

def findField(file):
    """
    Extracts the field name from the file. 
    Files will be in format [original filename][page number][field name].png
    Want to extract just the [field name]

    """
    (name, ext) = os.path.splitext(file)
    matches = re.findall('(?<=page-\d_).*$', name)
    return(matches[0])

def findFormNumber(file):
    """
    @@file - the file to find the form number of
    This function takes in a file and spits out the form number associated with it
    """
    #make a subdirectory to put the image exports if the directory
    #does not already exist
    if not os.path.exists('FormNumber'):
        os.makedirs('FormNumber')
        
    #crop bottom of image
    image = file
    im = PIL.Image.open(file)
    width, height = im.size
    crop(image, (.04*width,.955*height,.95*width,.98*height), 'FormNumber/FormNo.png')
    
    #run tesseract on crop
    text = pytesseract.image_to_string(PIL.Image.open('FormNumber/FormNo.png'))
    
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
        text = pytesseract.image_to_string(PIL.Image.open('FormNumber/FormNo.png'))
    
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
        text = pytesseract.image_to_string(PIL.Image.open('FormNumber/FormNo.png'))
    
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
        text = pytesseract.image_to_string(PIL.Image.open('FormNumber/FormNo.png'))
    
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
        text = pytesseract.image_to_string(PIL.Image.open('FormNumber/FormNo.png'))
    
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
        text = pytesseract.image_to_string(PIL.Image.open('FormNumber/FormNo.png'))
    
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

def tesseract(image_folder_location):
    """
    @@param folder_location folder location for where cropped images are stored
    for tesseract to run on them
    Runs tesseract on all of the cropped images and exports the results into
    an excel spreadsheet containing the original file name, the field name, 
    the text tesseract originally extract, and the text cleaned after regex.
    """
    #set working directory to image_folder_location
    os.chdir(image_folder_location)
    
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
        file.append(findOriginalFileName(croppedImages[i]))
        #pulling out the field name from middle of string
        field.append(findField(croppedImages[i]))
        #running tesseract on the image
        text.append(pytesseract.image_to_string(PIL.Image.open(croppedImages[i])))
        
    #pulling all the information after the heading
    for i in range(len(text)):
        if len(text[i]) > 0:
            cleaned_text.append(re.search(r'[^\n]+$',text[i]).group())
        #add in a "no value found" if empty    
        else:
            cleaned_text.append("No value found")

    #create dataframe of the values
    df = pd.DataFrame({'File': file, 
                  'Field': field, 
                  'TesseractText': text, 
                  'CleanedText': cleaned_text})
    
    #format dataframe into the Excel format 
    df_formatted = df.pivot(index = 'File', columns = 'Field', values = 'CleanedText')    

    #clean dataframe
    for i in range(len(df_formatted)):
        df_formatted['Zip'] = df_formatted['Zip'][i].replace('O','0').replace(" ", "")
        df_formatted['DateOfBirth'] = df_formatted['DateOfBirth'][i].replace('O','0').replace(" ", "")
        if 'Telephone' in df_formatted:
            df_formatted['Telephone'] = df_formatted['Telephone'][i].replace('(','').replace(')',"").replace(" ", "").replace("-","")
        else:
            continue
           
    #output file
    writer = ExcelWriter('i9Export.xlsx')
    df_formatted.to_excel(writer)
    writer.save()
    
def switchCoords(form_number):
    switcher = {
            '02/02/09': image_coords_020209,
            '05/07/87': image_coords_050787,
            '06/05/07': image_coords_060507,
            '08/07/09': image_coords_080709
    }
    coords = switcher.get(form_number, "Invalid form number")
    return(coords)

def PNG2Data(image_folder_location):
    """
    @@image_folder_location is the location of the images
    Takes all images in folder finds their form number and crops them based 
    on the respective form number, runs tesseract on all of the cropped images, 
    parses the text output and cleans it, then outputs the result into a 
    dataframe with the rows representing the file it came from, and the column 
    representing the field.
    """
    #####testing on all pages of 02-02-09, 05-07-87, 06-05-07, and 08-07-09
    
    #Make a vector of PNG files in the image directory so it can repeat 
    #process on all images in directory
    images = []
    os.chdir(image_folder_location)
    for image in os.listdir(image_folder_location):
        if image.endswith(".png"):
            images.append(image)
    
    #create empty lists to compile information
    filenames = []
    
    #make a subdirectory to put the image exports if the directory
    #does not already exist
    if not os.path.exists('CroppedImages'):
        os.makedirs('CroppedImages')
    
    #create variable for name of folder with cropped images
    cropped_images_folder_location = image_folder_location + '/CroppedImages'

    #make a subdirectory to put the form number image exports if the directory
    #does not already exist
    if not os.path.exists('FormNumber'):
        os.makedirs('FormNumber')
        
    #loop through files in folder and find their form number
    for image in images:
        #find the filename
        filename = findFileName(image)
        filenames.append(filename)
        
        #get image dimensions
        im = PIL.Image.open(image)
        width, height = im.size
        
        #close the file
        im.close()
        
        #find the form number and page number
        form_number = findFormNumber(image)
        
        #check if form_number found. If not, continue to next image. 
        if form_number is None:
            continue
        
        page_number = findPageNumber(image)
        
        #find coords needed for form number
        coords = switchCoords(form_number)
        
        #determine if this file contains data based on page_info lookup table and then
        #crop the image if it does
        if isinstance(page_info[form_number], int):
             if page_info[form_number] == page_number:
                #loop through the coordinates for each attribute and create a new image
                for key, value in coords.items():
                    #only do the crop if there is the correct number of dimensions
                    if len(value) != 4:
                        if len(value) == 0:
                            print(key, " has no coords yet.")
                            continue
                        else:
                            print(key, "has an incorrect number of dimensions.")
                            continue
                    else:
                        crop(image, value, 'CroppedImages/' + filename + '_' + key +'.png')
             else:
                 print("Not a data form")
        else:
             if page_info[form_number][0] == page_number or page_info[form_number][1] == page_number:
                #loop through the coordinates for each attribute and create a new image
                for key, value in coords.items():
                    #only do the crop if there is the correct number of dimensions
                    if len(value) != 4:
                        if len(value) == 0:
                            print(key, " has no coords yet.")
                        else:
                            print(key, "has an incorrect number of dimensions.")
                    else:
                        crop(image, value, 'CroppedImages/' + filename + '_' + key +'.png')
             else:
                 print("Not a data form")
                 
    #run tesseract on folder with cropped images
    tesseract(cropped_images_folder_location)
    
if __name__ == '__main__':
    ###TESTING
    #function to find a key with more than 4 values
    #for key, value in image_coords_020209.items():
    #if len(value) > 4:
    #    print(key)
    
    #testing on all pages of 02-02-09, 05-07-87, 06-05-07, and 08-07-09
    #current it is just dumping cropped images into a new folder
    
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
    
    #listing out the (x1, y1, x2, y2) coordinates of information on each of 
    #the different forms
    image_coords_020209 = {'LastName':(.055*width,.180*height,.37*width,.204*height),
                'FirstName': (.368*width,.180*height,.61*width,.205*height), 
                'MiddleInitial': (.610*width,.180*height,.686*width,.205*height),
                'MaidenName': (.69*width,.18*height,.94*width,.205*height),
                'StreetAddress': (.055*width,.217*height,.58*width,.240*height),
                'City': (.055*width,.252*height,.35*width,.275*height),
                'DateOfBirth': (.688*width,.217*height,.95*width,.240*height),
                'SocialSecurity': ((.688*width,.253*height,.95*width,.275*height)),
                'State': (.345*width,.252*height,.58*width,.275*height),
                'Zip': (.58*width,.252*height,.688*width,.275*height),
                'EmailAddress': (),
                'Telephone': (),
                'Attestation': (.49*width,.292*height,.515*width,.365*height),
                'Alien # for Permanent Residence': (.722*width,.325*height,.94*width,.345*height),
                'Date Expiration of Work Authorization': (.805*width,.362*height,.955*width,.377*height),
                'Alien # for Work Authorization': (.81*width,.346*height,.955*width,.365*height),
                'I-94 Admission Number': (),
                'Foreign Passport': (),
                'Country of Issuance': (),
                'TranslatorName': (.513*width,.443*height,.94*width,.469*height),
                'TranslatorAddress': (.104*width,.482*height,.67*width,.505*height),
                'TranslatorDateOfSignature': (.68*width,.482*height,.94*width,.505*height),
                'List A - DocumentTitle': (.145*width,.564*height,.363*width,.586*height),
                'List A - IssuingAuthority': (.15*width,.586*height,.363*width,.605*height),
                'List A - DocumentNumber': (.126*width,.606*height,.363*width,.625*height),
                'List A - DocumentExpirationDate': (.215*width,.625*height,.363*width,.644*height),
                'List A - DocumentTitle - Second Section': (),
                'List A - IssuingAuthority - Second Section': (),
                'List A - DocumentNumber - Second Section': (.13*width,.644*height,.363*width,.662*height),
                'List A - Document Expiration Date - Second Section': (.215*width,.662*height,.363*width,.682*height),
                'List B - DocumentTitle': (.38*width,.561*height,.64*width,.585*height),
                'List B - IssuingAuthority': (.38*width,.585*height,.64*width,.605*height),
                'List B - DocumentNumber': (.38*width,.6052*height,.64*width,.6245*height),
                'List B - DocumentExpirationDate': (.38*width,.6245*height,.64*width,.6445*height),
                'List C - DocumentTitle': (.7*width,.561*height,.95*width,.585*height),
                'List C - IssuingAuthority': (.7*width,.585*height,.95*width,.605*height),
                'List C - DocumentNumber': (.7*width,.6052*height,.95*width,.6245*height),
                'List C - DocumentExpirationDate': (.7*width,.6245*height,.95*width,.6445*height),
                'DateOfHire': (.16*width,.711*height,.278*width,.726*height),
                'Name of Employee Representative': (.394*width,.752*height,.698*width,.777*height),
                'Title': (.698*width,.752*height,.95*width,.777*height),
                'EmployerBusinessName': (.05*width,.7875*height,.698*width,.808*height),
                'EmployerStreetAddress': (),
                'Date Signed by Employer': (.698*width,.7875*height,.95*width,.808*height),
                'List A - DocumentTitle - Third Section': (),
                'List A - IssuingAuthority - Third Section': (),
                'List A - DocumentNumber - Third Section': (),
                'List A - Document Expiration Date - Third Section': (),
                'Employee Info from Section 1': ()}
    
    image_coords_050787 = {'LastName':(.069*width,.1215*height,.38*width,.1525*height),
                    'FirstName': (.38*width,.1215*height,.56*width,.1525*height), 
                    'DateOfBirth': (.07*width,.1819*height,.51*width,.211*height),
                    'SocialSecurity': (.51*width,.1819*height,.91*width,.211*height),
                    'Attestation': (.085*width,.228*height,.12*width,.275*height),
                    'Alien_AdmissionNo1': (.503*width,.24*height,.655*width,.26*height),
                    'Alien_AdmissionNo2': (.732*width,.26*height,.911*width,.276*height),
                    'Alien_AdmissionNo3': (.235*width,.2735*height,.369*width,.29*height),
                    'StreetAddress': (.08*width,.1519*height,.38*width,.182*height),
                    'City': (.38*width,.1519*height,.56*width,.182*height),
                    'State': (.56*width,.1519*height,.735*width,.182*height),
                    'Zip': (.735*width,.1519*height,.92*width,.182*height),
                    #'WorkAuthorization': (),
                    'Translator': (.51*width,.394*height,.833*width,.424*height),
                    'DocumentTitle1': (.06*width,.632*height,.09*width,.72*height),
                    'DocumentTitle2': (.38*width,.61*height,.4*width,.73*height),
                    'DocumentTitle3': (.7*width,.61*height,.72*width,.73*height),
                    'DocumentNumber1': (.076*width,.782*height,.315*width,.8*height),
                    'DocumentNumber2': (.3913*width,.782*height,.63*width,.8*height),
                    'DocumentNumber3': (.712*width,.782*height,.95*width,.8*height),
                    'DateOfHire': (.785*width,.925*height,.95*width,.953*height),
                    'MiddleInitial': (.56*width,.1215*height,.74*width,.1525*height)}
    
    image_coords_060507 = {'LastName':(.055*width,.185*height,.36*width,.221*height),
                    'FirstName': (.36*width,.185*height,.58*width,.221*height), 
                    'DateOfBirth': (.69*width,.2215*height,.95*width,.25*height),
                    'SocialSecurity': (.688*width,.257*height,.94*width,.291*height),
                    'Attestation': (.45*width,.306*height,.4752*width,.355*height),
                    'Alien_AdmissionNo1': (.71*width,.318*height,.95*width,.332*height),
                    'Alien_AdmissionNo2': (.61*width,.351*height,.95*width,.37*height),
                    'StreetAddress': (.055*width,.221*height,.57*width,.257*height),
                    'City': (.055*width,.257*height,.35*width,.291*height),
                    'State': (.35*width,.257*height,.57*width,.291*height),
                    'Zip': (.58*width,.257*height,.685*width,.291*height),
                    'WorkAuthorization': (.652*width,.334*height,.95*width,.351*height),
                    'TranslatorName': (.515*width,.433*height,.88*width,.469*height),
                    'TranslatorAddress': (.1*width,.47*height,.677*width,.497*height),
                    'TranslatorSignDate': (.678*width,.47*height,.9*width,.497*height),
                    'DocumentTitle1': (.14*width,.561*height,.36*width,.59*height),
                    'DocumentTitle2': (.39*width,.561*height,.625*width,.586*height),
                    'DocumentTitle3': (.71*width,.561*height,.945*width,.586*height),
                    'IssuingAuthority1': (.15*width,.586*height,.358*width,.607*height),
                    'IssuingAuthority2': (.39*width,.586*height,.625*width,.607*height),
                    'IssuingAuthority3': (.71*width,.586*height,.945*width,.607*height),
                    'DocumentNumber1': (.13*width,.606*height,.358*width,.625*height),
                    'DocumentNumber2': (.39*width,.606*height,.625*width,.625*height),
                    'DocumentNumber3': (.71*width,.606*height,.945*width,.625*height),
                    'DocumentNumber4': (.13*width,.645*height,.358*width,.663*height),                
                    'ExpirationDate1': (.225*width,.625*height,.351*width,.645*height),
                    'ExpirationDate2': (.39*width,.625*height,.625*width,.645*height),
                    'ExpirationDate3': (.71*width,.625*height,.945*width,.645*height),
                    'ExpirationDate4': (.22*width,.6624*height,.358*width,.683*height),
                    #'DateOfHire': (),
                    'MiddleInitial': (.58*width,.185*height,.685*width,.221*height),
                    'ApartmentNo': (.58*width,.2215*height,.685*width,.2454*height)}
    
    image_coords_080709 = {'LastName':(.055*width,.17*height,.37*width,.205*height),
                    'FirstName': (.37*width,.17*height,.61*width,.205*height), 
                    'DateOfBirth': (.69*width,.205*height,.94*width,.241*height),
                    'SocialSecurity': (.69*width,.241*height,.94*width,.277*height),
                    'Attestation': (.49*width,.29*height,.515*width,.367*height),
                    'Alien_AdmissionNo1': (.725*width,.325*height,.945*width,.345*height),
                    'Alien_AdmissionNo2': (.81*width,.345*height,.94*width,.363*height),
                    'StreetAddress': (.055*width,.205*height,.58*width,.241*height),
                    'City': (.055*width,.241*height,.34*width,.277*height),
                    'State': (.34*width,.241*height,.58*width,.277*height),
                    'Zip': (.58*width,.241*height,.68*width,.277*height),
                    #'WorkAuthorization': (),
                    'Translator': (.515*width,.432*height,.88*width,.47*height),
                    'DocumentTitle1': (.14*width,.561*height,.36*width,.59*height),
                    'DocumentTitle2': (.39*width,.561*height,.625*width,.586*height),
                    'DocumentTitle3': (.71*width,.561*height,.945*width,.586*height),
                    'IssuingAuthority1': (.15*width,.586*height,.358*width,.607*height),
                    'IssuingAuthority2': (.39*width,.586*height,.625*width,.607*height),
                    'IssuingAuthority3': (.71*width,.586*height,.945*width,.607*height),
                    'DocumentNumber1': (.13*width,.606*height,.358*width,.625*height),
                    'DocumentNumber2': (.39*width,.606*height,.625*width,.625*height),
                    'DocumentNumber3': (.71*width,.606*height,.945*width,.625*height),
                    'DocumentNumber4': (.13*width,.645*height,.358*width,.663*height),                
                    'ExpirationDate1': (.225*width,.625*height,.351*width,.645*height),
                    'ExpirationDate2': (.39*width,.625*height,.625*width,.645*height),
                    'ExpirationDate3': (.71*width,.625*height,.945*width,.645*height),
                    'ExpirationDate4': (.22*width,.6624*height,.358*width,.683*height),
                    #'DateOfHire': (),
                    'MiddleInitial': (.61*width,.17*height,.685*width,.205*height),
                    'ApartmentNo': (.57*width,.205*height,.66*width,.241*height)}
    
    ###Run PNG2Data on folder with cropped images
    image_folder_location = 'C:\\Users\\Brandon Croarkin\\Documents\\GreenZone\\OCR\\I9 Forms - Filled\\PythonPNGs\\FilesToCrop\\Testing'
    PNG2Data(image_folder_location)