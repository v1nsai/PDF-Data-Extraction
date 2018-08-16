# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 11:16:02 2018

@author: Brandon Croarkin
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 13:39:18 2018

@author: Brandon Croarkin
"""

from wand.image import Image
import pytesseract
import PIL
import os
import re
import pandas as pd
import numpy as np
from pandas import ExcelWriter
from io import BytesIO

def PDFCount(folder_location):
    PDFs = []
    for file in os.listdir(folder_location):
        if file.endswith(".pdf"):
            PDFs.append(file)
    return(len(PDFs))
    
def imageCount(image_folder_location):
    PNGs = []
    for image in os.listdir(image_folder_location):
        if image.endswith(".png"):
            PNGs.append(image)
    return(len(PNGs))
    

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

def crop(png, coords):
    """
    @param image_path: The path to the image to edit
    @param coords: A tuple of x/y coordinates (x1, y1, x2, y2)
    @param saved_location: Path to save the cropped image
    """
    swap = BytesIO()
    image_obj = PIL.Image.open(png)
    cropped_image = image_obj.crop(coords)
    cropped_image.save(swap)

    return swap


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

def findFormNumber(png):
    """
    @@file - the file to find the form number of
    This function takes in a file and spits out the form number associated with it
    """
        
    #crop bottom of image
    im = PIL.Image.open(png)
    width, height = im.size
    while True:
        try:    
            cropped_img = crop(image, (.04*width,.955*height,.95*width,.98*height))
            #run tesseract on crop
            text = pytesseract.image_to_string(PIL.Image.open(cropped_img))
            #clean output to just pull revision date with either dd/mm/yy or dd-mm-yy format
            matches = re.findall('(\d{2}[\/ ](\d{2}|January|Jan|February|Feb|March|Mar|April|Apr|May|May|June|Jun|July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec)[\/ ]\d{2,4})'
                     , text)
            #return output
            if matches:
                for match in matches:
                    return(match[0])
                    break
            elif not matches:
                print('nothing found in first crop')
                cropped_img = crop(image, (.04*width,.925*height,.95*width,.955*height))
    
                #run tesseract on crop
                text = pytesseract.image_to_string(PIL.Image.open(cropped_img))
    
                #clean output to just pull revision date with either dd/mm/yy or dd-mm-yy format
                matches = re.findall('(\d{2}[\/ ](\d{2}|January|Jan|February|Feb|March|Mar|April|Apr|May|May|June|Jun|July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec)[\/ ]\d{2,4})'
                     , text)
        
                #output answer
                for match in matches:
                    return(match[0])
    
            if not matches:
                print('nothing found in second crop')
                cropped_img = crop(image, (.04*width,.907*height,.95*width,.925*height))
            
                #run tesseract on crop
                text = pytesseract.image_to_string(PIL.Image.open(cropped_img))
            
                #clean output to just pull revision date with either dd/mm/yy or dd-mm-yy format
                matches = re.findall('(\d{2}[\/ ](\d{2}|January|Jan|February|Feb|March|Mar|April|Apr|May|May|June|Jun|July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec)[\/ ]\d{2,4})'
                             , text)
                
                #output answer
                for match in matches:
                    return(match[0])
            
            if not matches:
                print('nothing found in third crop. Trying dd-mm-yyyy format.')
                cropped_img = crop(image, (.04*width,.925*height,.95*width,.955*height))
            
                #run tesseract on crop
                text = pytesseract.image_to_string(PIL.Image.open(cropped_img))
            
                #clean output to just pull revision date with either dd/mm/yy or dd-mm-yy format
                matches = re.findall('(\d{2}[\- ](\d{2}|January|Jan|February|Feb|March|Mar|April|Apr|May|May|June|Jun|July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec)[\- ]\d{2,4})'
                             , text)
                
                #output answer
                for match in matches:
                    return(match[0])
                    
            if not matches:
                print('nothing found in forth crop.')
                cropped_img = crop(image, (.04*width,.80*height,.95*width,.83*height))
            
                #run tesseract on crop
                text = pytesseract.image_to_string(PIL.Image.open(cropped_img))
            
                #clean output to just pull revision date with either dd/mm/yy or dd-mm-yy format
                matches = re.findall('(\d{2}[\- ](\d{2}|January|Jan|February|Feb|March|Mar|April|Apr|May|May|June|Jun|July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec)[\- ]\d{2,4})'
                             , text)
                
                #output answer
                for match in matches:
                    return(match[0])
            
            if not matches: 
                print('nothing found in fifth crop')
                cropped_img = crop(image, (.04*width,.955*height,.95*width,.98*height))
            
                #run tesseract on crop
                text = pytesseract.image_to_string(PIL.Image.open(cropped_img))
            
                #clean output to just pull revision date with either dd/mm/yy or dd-mm-yy format
                matches = re.findall('(\d{2}[\- ](\d{2}|January|Jan|February|Feb|March|Mar|April|Apr|May|May|June|Jun|July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec)[\- ]\d{2,4})'
                             , text)
                
                #output answer
                for match in matches:
                    return(match[0])  
                    
            else:
                return('not found')
        
        except IOError:
            print("image file is truncated")
            break
    
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

def tesseract(crops):
    """
    @@param folder_location folder location for where cropped images are stored
    for tesseract to run on them
    Runs tesseract on all of the cropped images and exports the results into
    an excel spreadsheet containing the original file name, the field name, 
    the text tesseract originally extract, and the text cleaned after regex.
    """
    #set working directory to image_folder_location
    os.chdir(cropped_images_folder_location)

    #create list of png images to crop
    croppedImages = []
    for image in os.listdir(cropped_images_folder_location):
        if image.endswith(".png"):
            croppedImages.append(image)

    #create empty lists to add data to
    file = []
    field = []
    text = []
    cleaned_text = []
    
    #run tesseract on all of the images and then delete
    for i in range(len(croppedImages)):
        #pulling out the file name from beginning of string
        file.append(findOriginalFileName(croppedImages[i]))
        #pulling out the field name from middle of string
        field.append(findField(croppedImages[i]))
        #running tesseract on the image
        text.append(pytesseract.image_to_string(PIL.Image.open(croppedImages[i])))
        #delete cropped image so NiFi doesn't repeat process on same image
        os.remove(croppedImages[i])
        
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
    df_formatted = df.reset_index().pivot(index = 'File', columns = 'Field', values = 'CleanedText')    

    #clean dataframe
    for i in range(len(df_formatted)):
        df_formatted['Zip'][i] = df_formatted['Zip'][i].replace('O','0').replace(" ", "").replace("l","1")
        df_formatted['DateOfBirth'][i] = df_formatted['DateOfBirth'][i].replace('O','0').replace(" ", "").replace("\\","").replace("l","1").replace("'","").replace("‘","")
        if 'Telephone' in df_formatted:
            if df_formatted['Telephone'][i] is None:
                continue
            else:
                df_formatted['Telephone'][i] = df_formatted['Telephone'][i].replace('(','').replace(')',"").replace(" ", "").replace("-","")
        else:
            continue
        
    ###make a second dataframe with just the main columns of interest
    #make the list of columns to grab
    columns = ['LastName','FirstName', 'DateOfBirth', 'SocialSecurity', 'Attestation',
               'Alien # for Permanent Residence', 'Alien # for Work Authorization', 
               'StreetAddress', 'City', 'State', 'Zip', 'TranslatorName', 
               'List A - DocumentTitle', 'List A - DocumentNumber', 
               'List B - DocumentTitle', 'List B - DocumentNumber', 
               'List C - DocumentTitle', 'List C - DocumentNumber', 
               'DateOfHire']
    
    #create a dictionary to get the text value needed 
    attestation_dict = {0: 'A citizen of the United States',
                        1: 'A noncitizen of the United States',
                        2: 'A lawful permanent resident (Alien #)',
                        3: 'An alien authorized to work'
            }   
    
    #choose the selected columns from df_clean
    df_clean = df_formatted.loc[:,columns]
    
    #create columns to add to df_clean
    AlienAdmissionNumber = []
    DocumentTitle = []
    DocumentNumber = []
    
    #update values in the rows
    for i in range(len(df_formatted)):
        #find the index value of the K in Attestation
        try:
            df_clean['Attestation'][i] = attestation_dict[df_formatted['Attestation'][i].find('K')]
        except KeyError:
            df_clean['Attestation'][i] = "Attestation not found"
        
        #use Alien # to help fill in Attestation
        if (df_clean['Attestation'][i] == 'Attestation not found'):
            if (df_formatted['Alien # for Permanent Residence'][i] != 'No value found') & (df_formatted['Alien # for Permanent Residence'][i] is not None):
                df_clean['Attestation'][i] = 'A lawful permanent resident (Alien #)'
            elif (df_formatted['Alien # for Work Authorization'][i] != 'No value found') & (df_formatted['Alien # for Work Authorization'][i] is not None):
                df_clean['Attestation'][i] = 'An alien authorized to work'
            else:
                continue
        else:
            continue
    for i in range(len(df_formatted)):
        #set A# or Admission# value depending on Attestation
        if df_clean['Attestation'][i] == 'A citizen of the United States':
            AlienAdmissionNumber.append('NA')
        elif (df_clean['Attestation'][i] == 'A lawful permanent resident (Alien #)'):
            AlienAdmissionNumber.append(df_clean['Alien # for Permanent Residence'][i])            
        elif (df_clean['Attestation'][i] == 'An alien authorized to work'):
            AlienAdmissionNumber.append(df_clean['Alien # for Work Authorization'][i])  
        else:
            AlienAdmissionNumber.append('NA')

    for i in range(len(df_formatted)):      
              
        #set document title
        if (df_clean['List A - DocumentTitle'][i] != 'No value found') and (df_clean['List A - DocumentTitle'][i] is not None):
            DocumentTitle.append(df_clean['List A - DocumentTitle'][i])
        else:
            if (df_clean['List B - DocumentTitle'][i] is not None) & (df_clean['List C - DocumentTitle'][i] is not None):
                DocumentTitle.append(df_clean['List B - DocumentTitle'][i] + " and " + df_clean['List C - DocumentTitle'][i])
            else:
                DocumentTitle.append("NA")
        
        #set document number
        if (df_clean['List A - DocumentNumber'][i] != 'No value found') and (df_clean['List A - DocumentNumber'][i] is not None):
            DocumentNumber.append(df_clean['List A - DocumentNumber'][i])
        else:
            if (df_clean['List B - DocumentNumber'][i] is not None) & (df_clean['List C - DocumentNumber'][i] is not None):
                DocumentNumber.append(df_clean['List B - DocumentNumber'][i] + " and " + df_clean['List C - DocumentNumber'][i])
            else:
                DocumentNumber.append("NA")
                
    #create new columns from the lists
    df_clean['A# or Admission#'] = AlienAdmissionNumber
    df_clean['DocumentTitle'] = DocumentTitle
    df_clean['DocumentNumber'] = DocumentNumber
                     
    #delete uneeded columns
    cols_to_delete = ['Alien # for Permanent Residence', 'Alien # for Work Authorization',
                      'List A - DocumentTitle', 'List B - DocumentTitle', 'List A - DocumentNumber',
                      'List B - DocumentNumber', 'List C - DocumentTitle', 'List C - DocumentNumber']
    
    df_clean.drop(cols_to_delete, axis = 1, inplace = True)  
    
    #order columns
    cols = ['LastName', 'FirstName', 'DateOfBirth', 'SocialSecurity', 'Attestation', 
            'A# or Admission#', 'StreetAddress', 'City', 'State', 'Zip', 'TranslatorName',
            'DocumentTitle', 'DocumentNumber', 'DateOfHire']
    
    df_clean = df_clean[cols]
    
    #fill in None values with NA
    df_clean.fillna(value = "NA", inplace = True)
           
    #output files
    writer = ExcelWriter('i9Export(FullData).xlsx')
    df_formatted.to_excel(writer)
    writer.save()
    
    writer = ExcelWriter('i9Export(SubsetData).xlsx')
    df_clean.to_excel(writer)
    writer.save()
    
def setImageCoords(file, page_number):
    image = file
    im = PIL.Image.open(image)
    width, height = im.size
    
    formNumber = findFormNumber(image)
    
    if formNumber == '02/02/09':
        #listing out the (x1, y1, x2, y2) coordinates of information on each of 
        #the different forms
        global image_coords_020209
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
     
    elif formNumber == '08/07/09':
        global image_coords_080709
        image_coords_080709 = {'LastName':(.055*width,.17*height,.37*width,.205*height),
                'FirstName': (.37*width,.17*height,.61*width,.205*height), 
                'DateOfBirth': (.69*width,.205*height,.94*width,.241*height),
                'SocialSecurity': (.69*width,.241*height,.94*width,.277*height),
                'Attestation': (.49*width,.29*height,.515*width,.367*height),
                'Alien # for Permanent Residence': (.725*width,.325*height,.945*width,.345*height),
                'Alien # for Work Authorization': (.81*width,.345*height,.94*width,.363*height),
                'StreetAddress': (.055*width,.205*height,.58*width,.241*height),
                'City': (.055*width,.241*height,.34*width,.277*height),
                'State': (.34*width,.241*height,.58*width,.277*height),
                'Zip': (.58*width,.241*height,.68*width,.277*height),
                'WorkAuthorization': (),
                'Translator': (.515*width,.432*height,.88*width,.47*height),
                'DocumentTitle1': (.14*width,.561*height,.36*width,.59*height),
                'DocumentTitle2': (.39*width,.561*height,.625*width,.586*height),
                'DocumentTitle3': (.71*width,.561*height,.945*width,.586*height),
                'Issuing Authority1': (.15*width,.586*height,.358*width,.607*height),
                'Issuing Authority2': (.39*width,.586*height,.625*width,.607*height),
                'Issuing Authority3': (.71*width,.586*height,.945*width,.607*height),
                'DocumentNumber1': (.13*width,.606*height,.358*width,.625*height),
                'DocumentNumber2': (.39*width,.606*height,.625*width,.625*height),
                'DocumentNumber3': (.71*width,.606*height,.945*width,.625*height),
                'DocumentNumber4': (.13*width,.645*height,.358*width,.663*height),                
                'Expiration Date1': (.225*width,.625*height,.351*width,.645*height),
                'Expiration Date2': (.39*width,.625*height,.625*width,.645*height),
                'Expiration Date3': (.71*width,.625*height,.945*width,.645*height),
                'Expiration Date4': (.22*width,.6624*height,.358*width,.683*height),
                'DateOfHire': (),
                'MiddleInitial': (.61*width,.17*height,.685*width,.205*height),
                'ApartmentNo': (.57*width,.205*height,.66*width,.241*height)}
        
    elif formNumber == '05/07/87':   
        global image_coords_050787
        image_coords_050787 = {'LastName':(.075*width,.133*height,.38*width,.1525*height),
                'FirstName': (.38*width,.133*height,.56*width,.1525*height), 
                'MiddleInitial': (.56*width,.133*height,.74*width,.1525*height),
                'MaidenName': (.74*width,.133*height,.95*width,.1525*height),
                'StreetAddress': (.08*width,.1612*height,.38*width,.182*height),
                'City': (.38*width,.1612*height,.56*width,.182*height),
                'State': (.56*width,.1612*height,.735*width,.182*height),
                'Zip': (.735*width,.1612*height,.92*width,.182*height),
                'DateOfBirth': (.07*width,.1923*height,.41*width,.211*height),
                'SocialSecurity': (.51*width,.1923*height,.91*width,.211*height),
                'EmailAddress': (),
                'Telephone': (),
                'Attestation': (.085*width,.228*height,.12*width,.275*height),
                'Alien # for Permanent Residence': (.503*width,.24*height,.655*width,.26*height),
                'Date Expiration of Work Authorization': (.62*width,.2735*height,.78*width,.29*height),
                'Alien # for Work Authorization': (.732*width,.26*height,.911*width,.276*height),
                'Admission # for Work Authorization': (.235*width,.2735*height,.369*width,.29*height),
                'I-94 Admission Number': (),
                'ForeignPassport': (),
                'Country of Issuance': (),
                'TranslatorName': (.51*width,.406*height,.833*width,.424*height),
                'TranslatorAddress': (),
                'TranslatorDateOfSignature': (),
                'List A - DocumentTitle': (.06*width,.632*height,.09*width,.72*height),
                'List A - IssuingAuthority': (),
                'List A - DocumentNumber': (.076*width,.782*height,.315*width,.8*height),
                'List A - ExpirationDate': (.067*width,.827*height,.315*width,.845*height),
                'List B - DocumentTitle': (.38*width,.61*height,.4*width,.73*height),
                'List B - IssuingAuthority': (),
                'List B - DocumentNumber': (.3913*width,.782*height,.63*width,.8*height),
                'List B - ExpirationDate': (.3913*width,.827*height,.63*width,.845*height),
                'List C - DocumentTitle': (.7*width,.61*height,.72*width,.73*height),
                'List C - IssuingAuthority': (),
                'List C - DocumentNumber': (.712*width,.782*height,.95*width,.8*height),
                'List C - Expiration Date': (.712*width,.827*height,.95*width,.845*height),
                'DateOfHire': (),
                'Name of Employee Representative': (.42*width,.905*height,.8*width,.924*height),
                'Title': (.8*width,.905*height,.95*width,.924*height),
                'EmployerBusinessName': (.07*width,.936*height,.4*width,.954*height),
                'EmployerStreetAddress': (.42*width,.935*height,.80*width,.954*height),
                'Date Signed by Employer': (.785*width,.925*height,.95*width,.953*height),
                'List A - DocumentTitle - Third Section': (),
                'List A - IssuingAuthority - Third Section': (),
                'List A - DocumentNumber - Third Section': (),
                'List A - Document Expiration Date - Third Section': (),
                'Employee Info from Section 1': ()}
        
    elif formNumber == '05/31/05':
        global image_coords_053105
        image_coords_053105 = {'LastName':(.05*width,.168*height,.37*width,.189*height),
                'FirstName': (.37*width,.168*height,.57*width,.189*height), 
                'MiddleInitial': (.57*width,.168*height,.67*width,.189*height),
                'MaidenName': (.68*width,.168*height,.95*width,.189*height),
                'StreetAddress': (.05*width,.202*height,.67*width,.22*height),
                'City': (.05*width,.233*height,.34*width,.251*height),
                'State': (.34*width,.233*height,.57*width,.251*height),
                'Zip': (.57*width,.233*height,.67*width,.251*height),
                'DateOfBirth': (.68*width,.203*height,.95*width,.22*height),
                'SocialSecurity': (.68*width,.233*height,.95*width,.251*height),
                'EmailAddress': (),
                'Telephone': (),
                'Attestation': (.515*width,.263*height,.538*width,.32*height),
                'Alien # for Permanent Residence': (.782*width,.285*height,.97*width,.305*height),
                'Date Expiration of Work Authorization': (.73*width,.3026*height,.815*width,.32*height),
                'Alien # for Work Authorization': (.682*width,.3152*height,.97*width,.331*height),
                'Admission # for Work Authorization': (),
                'I-94 Admission Number': (),
                'ForeignPassport': (),
                'Country of Issuance': (),
                'TranslatorName': ((.513*width,.41*height,.88*width,.423*height)),
                'TranslatorAddress': (.1*width,.436*height,.67*width,.454*height),
                'TranslatorDateOfSignature': (.68*width,.436*height,.88*width,.454*height),
                'List A - DocumentTitle': (.14*width,.513*height,.34*width,.534*height),
                'List A - IssuingAuthority': (.15*width,.533*height,.34*width,.558*height),
                'List A - DocumentNumber': (.14*width,.558*height,.34*width,.579*height),
                'List A - ExpirationDate': (.22*width,.581*height,.34*width,.605*height),
                'List B - DocumentTitle': (.38*width,.513*height,.618*width,.534*height),
                'List B - IssuingAuthority': (.38*width,.533*height,.618*width,.558*height),
                'List B - DocumentNumber': (.38*width,.558*height,.618*width,.579*height),
                'List B - ExpirationDate': (.38*width,.581*height,.618*width,.605*height),
                'List C - DocumentTitle': (.7*width,.513*height,.96*width,.534*height),
                'List C - IssuingAuthority': (.7*width,.533*height,.96*width,.558*height),
                'List C - DocumentNumber': (.7*width,.558*height,.96*width,.579*height),
                'List C - Expiration Date': (.7*width,.581*height,.96*width,.605*height),
                'DateOfHire': (.398*width,.686*height,.491*width,.7*height),
                'Name of Employee Representative': (.394*width,.739*height,.68*width,.758*height),
                'Title': (.69*width,.739*height,.96*width,.758*height),
                'EmployerBusinessName': (.04*width,.772*height,.305*width,.797*height),
                'EmployerStreetAddress': (.307*width,.772*height,.685*width,.797*height),
                'Date Signed by Employer': (.688*width,.772*height,.96*width,.797*height),
                'List A - DocumentTitle - Third Section': (.13*width,.605*height,.34*width,.627*height),
                'List A - IssuingAuthority - Third Section': (),
                'List A - DocumentNumber - Third Section': (),
                'List A - Document Expiration Date - Third Section': (.22*width,.63*height,.34*width,.656*height),
                'Employee Info from Section 1 - LastName': (),
                'Employee Info from Section 1 - FirstName': (), 
                'Employee Info from Section 1 - Middle Initial': ()
                }
        
    elif formNumber == '06/05/07': 
        global image_coords_060507
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
                        'DateOfHire': (),
                        'MiddleInitial': (.58*width,.185*height,.685*width,.221*height),
                        'ApartmentNo': (.58*width,.2215*height,.685*width,.2454*height)}
        
    elif (formNumber == '03/08/13') & (page_number == 6):
        global image_coords_030813_pg6
        image_coords_030813_pg6 = {'LastName':(.06*width,.225*height,.345*width,.246*height),
                'FirstName': (.346*width,.225*height,.58*width,.246*height), 
                'MiddleInitial': (.58*width,.225*height,.66*width,.246*height),
                'MaidenName': (.665*width,.225*height,.94*width,.246*height),
                'StreetAddress': (.06*width,.263*height,.39*width,.287*height),
                'City': (.5*width,.263*height,.72*width,.287*height),
                'State': (.73*width,.263*height,.803*width,.287*height),
                'Zip': (.804*width,.263*height,.93*width,.287*height),
                'DateOfBirth': (.06*width,.301*height,.23*width,.325*height),
                'SocialSecurity': (.23*width,.301*height,.405*width,.325*height),
                'EmailAddress': (.406*width,.301*height,.75*width,.325*height),
                'Telephone': (.755*width,.301*height,.94*width,.325*height),
                'Attestation': (.055*width,.385*height,.085*width,.48*height),
                'Alien # for Permanent Residence': (.563*width,.42*height,.81*width,.445*height),
                'Date Expiration of Work Authorization': (.53*width,.447*height,.662*width,.475*height),
                'Alien # for Work Authorization': (.383*width,.505*height,.62*width,.53*height),
                'I-94 Admission Number': (.297*width,.53*height,.62*width,.57*height),
                'Foreign Passport': (.294*width,.6*height,.72*width,.63*height),
                'Country of Issuance': (.254*width,.628*height,.72*width,.656*height),
                'TranslatorName': (.06*width,.857*height,.94*width,.88*height),
                'TranslatorAddress': (.06*width,.892*height,.94*width,.915*height),
                'TranslatorDateOfSignature': (.75*width,.822*height,.94*width,.834*height)}
    
    elif (formNumber == '03/08/13') & (page_number == 7):
        global image_coords_030813_pg7
        image_coords_030813_pg7 = {'List A - DocumentTitle': (.06*width,.205*height,.344*width,.222*height),
                'List A - IssuingAuthority': (.06*width,.233*height,.344*width,.249*height),
                'List A - DocumentNumber': (.06*width,.259*height,.344*width,.277*height),
                'List A - DocumentExpirationDate': (.06*width,.2905*height,.344*width,.308*height),
                'List A - DocumentTitle - Second Section': (.06*width,.32*height,.344*width,.337*height),
                'List A - IssuingAuthority - Second Section': (.06*width,.3475*height,.344*width,.3632*height),
                'List A - DocumentNumber - Second Section': (.06*width,.3738*height,.344*width,.390*height),
                'List A - Document Expiration Date - Second Section': (.06*width,.4005*height,.344*width,.4165*height),
                'List B - DocumentTitle': (.358*width,.205*height,.65*width,.222*height),
                'List B - IssuingAuthority': (.358*width,.233*height,.65*width,.249*height),                
                'List B - DocumentNumber': (.358*width,.259*height,.65*width,.277*height),
                'List B - DocumentExpirationDate': (.358*width,.2905*height,.65*width,.308*height),
                'List C - DocumentTitle': (.655*width,.205*height,.94*width,.222*height),
                'List C - IssuingAuthority': (.655*width,.233*height,.94*width,.249*height),
                'List C - DocumentNumber': (.655*width,.259*height,.94*width,.277*height),
                'List C - DocumentExpirationDate': (.655*width,.2905*height,.94*width,.308*height),
                'DateOfHire': (.445*width,.605*height,.59*width,.623*height),
                'Name of Employee Representative': (.06*width,.6775*height,.55*width,.702*height),
                'Title': (.605*width,.641*height,.94*width,.665*height),
                'EmployerBusinessName': (.58*width,.6775*height,.94*width,.702*height),
                'EmployerStreetAddress': (.06*width,.7135*height,.496*width,.739*height),
                'Date Signed by Employer': (.452*width,.641*height,.604*width,.665*height),
                'List A - DocumentTitle - Third Section': (.06*width,.43*height,.345*width,.449*height),
                'List A - IssuingAuthority - Third Section': (.06*width,.46*height,.345*width,.476*height),
                'List A - DocumentNumber - Third Section': (.06*width,.487*height,.345*width,.5065*height),
                'List A - Document Expiration Date - Third Section': (.06*width,.5188*height,.345*width,.537*height),
                'Employee Info from Section 1': ()}


    
    else:
        print("Dimensions not found for form number" + formNumber)
    
    im.close()

image_coords_020209 = {}
image_coords_050787 = {}
image_coords_060507 = {}
image_coords_080709 = {}
image_coords_053105 = {}
image_coords_030813_pg6 = {}
image_coords_030813_pg7 = {}

def switchCoords(form_number):
    switcher = {
            '02/02/09': image_coords_020209,
            '05/07/87': image_coords_050787,
            '06/05/07': image_coords_060507,
            '08/07/09': image_coords_080709,
            '05/31/05': image_coords_053105
    }
    coords = switcher.get(form_number, "Invalid form number")
    return(coords)

def switchCoords2(form_number, page_number):
    if form_number == '03/08/13':
        if page_number == 6:
            coords = image_coords_030813_pg6
            return(coords)
        elif page_number == 7:
            coords = image_coords_030813_pg7
            return(coords)
        else:
            print("This page does not contain data")
    else:
        switcher = {
                '02/02/09': image_coords_020209,
                '05/07/87': image_coords_050787,
                '06/05/07': image_coords_060507,
                '08/07/09': image_coords_080709,
                '05/31/05': image_coords_053105
        }
        coords = switcher.get(form_number, "Invalid form number")
        return(coords)

def PNG2Data(images):
    crops = []

    #loop through files in folder and find their form number
    for index, image in images:

        #find the form number and page number
        form_number = findFormNumber(image)
        
        #check if form_number found. If not, continue to next image. 
        if form_number is None:
            continue
        
        page_number = index
        
        #set image coordinates
        setImageCoords(image)
        
        #find coords needed for form number
        coords = switchCoords2(form_number, page_number)
        
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
                        crops.append(crop(image, value))
             else:
                 print("Not a data form")
        else:
             if (page_info[form_number][0] == page_number) or (page_info[form_number][1] == page_number):
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
                        crops.append(crop(image, value))
             else:
                 print("Not a data form")
                 
    #run tesseract on folder with cropped images
    tesseract(crops)
    
if __name__ == '__main__':
    folder_location = 'C:\\Users\\Brandon Croarkin\\Documents\\GreenZone\\OCR\\NiFiTesting'
    output_directory = 'PythonPNGs'
    
    #convert PDFs to images
    PDF2PNG(folder_location, output_directory, resolution = 600)
    
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
    
    ###Run PNG2Data on folder with cropped images when there are images in folder
    image_folder_location = 'C:\\Users\\Brandon Croarkin\\Documents\\GreenZone\\OCR\\NiFiTesting\\PythonPNGs'
    
    #get count of PDF's in folder (should only run PDF2PNG when none in folder)
    PDFcount = PDFCount(folder_location)
    
    #get count of images in image folder (should only run PDF2PNG when there are images)
    imageCounts = imageCount(image_folder_location)
    
    if (imageCounts > 0) & (PDFcount == 0):
        PNG2Data(image_folder_location)
    else:
        print("No images to extract text from.")