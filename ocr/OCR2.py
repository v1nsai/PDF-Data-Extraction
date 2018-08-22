# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 14:13:29 2018

@author: Brandon Croarkin
"""

from wand.image import Image
import sys
import io
import PIL
import pytesseract
import re
import json

image_coords_020209 = {}
image_coords_050787 = {}
image_coords_060507 = {}
image_coords_080709 = {}
image_coords_053105 = {}
image_coords_030813_pg7 = {}
image_coords_030813_pg8 = {}
image_coords_071717_pg1 = {} 
image_coords_071717_pg2 = {}
image_coords_111416_pg1 = {} 
image_coords_111416_pg2 = {}
image_coords_112191_L = {}
image_coords_112191_R = {}

def findFormNumber(file):
    """
    @@file - the file to find the form number of
    This function takes in a file and spits out the form number associated with it
    """        
    #crop bottom of image
    image = file
    im = PIL.Image.open(image)
    width, height = im.size
    
    while True:
        try:    
            swap = crop(image, (.04*width,.954*height,.95*width,.98*height))
            #run tesseract on crop
            text = pytesseract.image_to_string(PIL.Image.open(swap))
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
                swap = crop(image, (.04*width,.945*height,.95*width,.97*height))
    
                #run tesseract on crop
                text = pytesseract.image_to_string(PIL.Image.open(swap))
    
                #clean output to just pull revision date with either dd/mm/yy or dd-mm-yy format
                matches = re.findall('(\d{2}[\/ ](\d{2}|January|Jan|February|Feb|March|Mar|April|Apr|May|May|June|Jun|July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec)[\/ ]\d{2,4})'
                     , text)
        
                #output answer
                for match in matches:
                    return(match[0])
                    break
                
            elif not matches:
                print('nothing found in second crop')
                swap = crop(image, (.04*width,.925*height,.95*width,.955*height))

                #run tesseract on crop
                text = pytesseract.image_to_string(PIL.Image.open(swap))
    
                #clean output to just pull revision date with either dd/mm/yy or dd-mm-yy format
                matches = re.findall('(\d{2}[\/ ](\d{2}|January|Jan|February|Feb|March|Mar|April|Apr|May|May|June|Jun|July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec)[\/ ]\d{2,4})'
                     , text)
        
                #output answer
                for match in matches:
                    return(match[0])
                    break
    
            if not matches:
                print('nothing found in third crop')
                swap = crop(image, (.04*width,.907*height,.95*width,.925*height))
            
                #run tesseract on crop
                text = pytesseract.image_to_string(PIL.Image.open(swap))
            
                #clean output to just pull revision date with either dd/mm/yy or dd-mm-yy format
                matches = re.findall('(\d{2}[\/ ](\d{2}|January|Jan|February|Feb|March|Mar|April|Apr|May|May|June|Jun|July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec)[\/ ]\d{2,4})'
                             , text)
                
                #output answer
                for match in matches:
                    return(match[0])
                    break
            
            if not matches:
                print('nothing found in fourth crop. Trying dd-mm-yyyy format.')
                swap = crop(image, (.04*width,.925*height,.955*width,.955*height))
            
                #run tesseract on crop
                text = pytesseract.image_to_string(PIL.Image.open(swap))
            
                #clean output to just pull revision date with either dd/mm/yy or dd-mm-yy format
                matches = re.findall('(\d{2}[\- ](\d{2}|January|Jan|February|Feb|March|Mar|April|Apr|May|May|June|Jun|July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec)[\- ]\d{2,4})'
                             , text)
                
                #output answer
                for match in matches:
                    return(match[0]+'(R)')
                    break
                    
            if not matches:
                print('nothing found in fifth crop.')
                swap = crop(image, (.04*width,.80*height,.955*width,.83*height))
            
                #run tesseract on crop
                text = pytesseract.image_to_string(PIL.Image.open(swap))
            
                #clean output to just pull revision date with either dd/mm/yy or dd-mm-yy format
                matches = re.findall('(\d{2}[\- ](\d{2}|January|Jan|February|Feb|March|Mar|April|Apr|May|May|June|Jun|July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec)[\- ]\d{2,4})'
                             , text)
                
                #output answer
                for match in matches:
                    return(match[0]+'(L)')
                    break
            
            if not matches: 
                print('nothing found in sixth crop')
                swap = crop(image, (.04*width,.955*height,.95*width,.98*height))
            
                #run tesseract on crop
                text = pytesseract.image_to_string(PIL.Image.open(swap))
            
                #clean output to just pull revision date with either dd/mm/yy or dd-mm-yy format
                matches = re.findall('(\d{2}[\- ](\d{2}|January|Jan|February|Feb|March|Mar|April|Apr|May|May|June|Jun|July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec)[\- ]\d{2,4})'
                             , text)
                
                #output answer
                for match in matches:
                    return(match[0]+'(R)')  
                    break
                    
            if not matches:
                print('not found')
                break
        
        except IOError:
            print("image file is truncated")
            break

def findPageNumber(file):
    """
    @@file file to determine page number of
    This function intakes a file and spits out the page number based on
    cropping the file to find a page number
    """        
    #crop bottom of image
    image = file
    im = PIL.Image.open(image)
    width, height = im.size
    
    while True:
        try:    
            swap = crop(image, (.04*width,.955*height,.95*width,.98*height))
            #run tesseract on crop
            text = pytesseract.image_to_string(PIL.Image.open(swap))
            #clean output to just pull revision date with either dd/mm/yy or dd-mm-yy format
            matches = re.findall('Page (\d+)', text)
            #return output
            if matches:
                for match in matches:
                    return(int(match[0]))
                    break
            elif not matches:
                print('nothing found in first crop')
                swap = crop(image, (.04*width,.945*height,.95*width,.97*height))
    
                #run tesseract on crop
                text = pytesseract.image_to_string(PIL.Image.open(swap))
    
                #clean output to just pull revision date with either dd/mm/yy or dd-mm-yy format
                matches = re.findall('Page (\d+)', text)
        
                #output answer
                for match in matches:
                    return(int(match[0]))
                    break
            elif not matches:
                print('nothing found in second crop')
                swap = crop(image, (.04*width,.925*height,.95*width,.955*height))
    
                #run tesseract on crop
                text = pytesseract.image_to_string(PIL.Image.open(swap))
    
                #clean output to just pull revision date with either dd/mm/yy or dd-mm-yy format
                matches = re.findall('Page (\d+)', text)
        
                #output answer
                for match in matches:
                    return(int(match[0]))
                    break
    
            if not matches:
                print('nothing found in third crop')
                swap = crop(image, (.04*width,.907*height,.95*width,.925*height))
            
                #run tesseract on crop
                text = pytesseract.image_to_string(PIL.Image.open(swap))
            
                #clean output to just pull revision date with either dd/mm/yy or dd-mm-yy format
                matches = re.findall('Page (\d+)', text)
                
                #output answer
                for match in matches:
                    return(int(match[0]))
                    break
            
            if not matches:
                print('nothing found in fourth crop')
                swap = crop(image, (.04*width,.925*height,.95*width,.955*height))
            
                #run tesseract on crop
                text = pytesseract.image_to_string(PIL.Image.open(swap))
            
                #clean output to just pull revision date with either dd/mm/yy or dd-mm-yy format
                matches = re.findall('Page (\d+)', text)
                
                #output answer
                for match in matches:
                    return(int(match[0]))
                    break
                    
            if not matches:
                print('nothing found in fifth crop.')
                swap = crop(image, (.04*width,.80*height,.95*width,.83*height))
            
                #run tesseract on crop
                text = pytesseract.image_to_string(PIL.Image.open(swap))
            
                #clean output to just pull revision date with either dd/mm/yy or dd-mm-yy format
                matches = re.findall('Page (\d+)', text)
                
                #output answer
                for match in matches:
                    return(int(match[0]))
                    break
            
            if not matches: 
                print('nothing found in sixth crop')
                swap = crop(image, (.04*width,.955*height,.95*width,.98*height))
            
                #run tesseract on crop
                text = pytesseract.image_to_string(PIL.Image.open(swap))
            
                #clean output to just pull revision date with either dd/mm/yy or dd-mm-yy format
                matches = re.findall('Page (\d+)', text)
                
                #output answer
                for match in matches:
                    return(int(match[0]))
                    break
                    
            if not matches:
                print('not found')
                break
        
        except IOError:
            print("image file is truncated")
            break

def setImageCoords(file, formNumber, page_number):
    image = file
    im = PIL.Image.open(image)
    width, height = im.size
    
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
                        'MiddleInitial': (.61*width,.17*height,.685*width,.205*height),
                        'MaidenName': (),
                        'StreetAddress': (.055*width,.205*height,.58*width,.241*height),
                        'City': (.055*width,.241*height,.34*width,.277*height),
                        'State': (.34*width,.241*height,.58*width,.277*height),
                        'Zip': (.58*width,.241*height,.68*width,.277*height),
                        'DateOfBirth': (.69*width,.205*height,.94*width,.241*height),
                        'SocialSecurity': (.69*width,.241*height,.94*width,.277*height),
                        'Attestation': (.49*width,.29*height,.515*width,.367*height),
                        'Alien # for Permanent Residence': (.725*width,.325*height,.945*width,.345*height),
                        'Date Expiration of Work Authorization': (),
                        'I-94 Admission Number': (),
                        'ForeignPassport': (),
                        'Country of Issuance': (),
                        'Alien # for Work Authorization': (.81*width,.345*height,.94*width,.363*height),
                        'TranslatorName': (.515*width,.432*height,.88*width,.47*height),
                        'TranslatorAddress': (),
                        'TranslatorDateOfSignature': (),
                        'List A - DocumentTitle': (.14*width,.561*height,.36*width,.59*height),
                        'List A - IssuingAuthority': (.15*width,.586*height,.358*width,.607*height),
                        'List A - DocumentNumber': (.13*width,.606*height,.358*width,.625*height),
                        'List A - Expiration Date': (.225*width,.625*height,.351*width,.645*height),
                        'List B - DocumentTitle': (.39*width,.561*height,.625*width,.586*height),
                        'List B - IssuingAuthority': (.39*width,.586*height,.625*width,.607*height),
                        'List B - DocumentNumber': (.39*width,.606*height,.625*width,.625*height),
                        'List B - Expiration Date': (.39*width,.625*height,.625*width,.645*height),
                        'List C - DocumentTitle': (.71*width,.561*height,.945*width,.586*height),
                        'List C - IssuingAuthority': (.71*width,.586*height,.945*width,.607*height),
                        'List C - DocumentNumber': (.71*width,.606*height,.945*width,.625*height),
                        'List C - Expiration Date': (.71*width,.625*height,.945*width,.645*height),
                        'List A - DocumentNumber - Second Section': (.13*width,.645*height,.358*width,.663*height),                
                        'List A - Expiration Date -  Second Section': (.22*width,.6624*height,.358*width,.683*height),
                        'DateOfHire': (),
                        #'ApartmentNo': (.57*width,.205*height,.66*width,.241*height)
                        }
        
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
        image_coords_060507 = {'LastName':(.055*width,.197*height,.36*width,.221*height),
                'FirstName': (.36*width,.197*height,.58*width,.221*height), 
                'MiddleInitial': (.58*width,.197*height,.685*width,.221*height),
                'MaidenName': (.688*width,.197*height,.95*width,.221*height),
                'StreetAddress': (.055*width,.233*height,.57*width,.257*height),
                'City': (.055*width,.257*height,.35*width,.291*height),
                'State': (.35*width,.257*height,.57*width,.291*height),
                'Zip': (.58*width,.257*height,.685*width,.291*height),
                'DateOfBirth': (.69*width,.233*height,.95*width,.25*height),
                'SocialSecurity': (.688*width,.257*height,.94*width,.291*height),
                'Attestation': (.45*width,.306*height,.4752*width,.355*height),
                'Alien # for Permanent Residence': (.71*width,.318*height,.95*width,.332*height),
                'Date Expiration of Work Authorization': (.652*width,.332*height,.95*width,.349*height),
                'Alien # for Work Authorization': (.61*width,.349*height,.95*width,.368*height),
                'Admission # for Work Authorization': (),
                'I-94 Admission Number': (),
                'ForeignPassport': (),
                'Country of Issuance': (),
                'TranslatorName': (.515*width,.433*height,.88*width,.469*height),
                'TranslatorAddress': (.1*width,.47*height,.677*width,.497*height),
                'TranslatorDateOfSignature': (.678*width,.47*height,.9*width,.497*height),
                'List A - DocumentTitle': (.14*width,.561*height,.36*width,.59*height),
                'List A - IssuingAuthority': (.15*width,.586*height,.358*width,.607*height),
                'List A - DocumentNumber': (.13*width,.606*height,.358*width,.625*height),
                'List A - Expiration Date': (.225*width,.625*height,.351*width,.645*height),
                'List B - DocumentTitle': (.39*width,.561*height,.625*width,.586*height),
                'List B - IssuingAuthority': (.39*width,.586*height,.625*width,.607*height),
                'List B - DocumentNumber': (.39*width,.606*height,.625*width,.625*height),
                'List B - Expiration Date': (.39*width,.625*height,.625*width,.645*height),
                'List C - DocumentTitle': (.71*width,.561*height,.945*width,.586*height),
                'List C - IssuingAuthority': (.71*width,.586*height,.945*width,.607*height),
                'List C - DocumentNumber': (.71*width,.606*height,.945*width,.625*height),                
                'List C - Expiration Date': (.71*width,.625*height,.945*width,.645*height),
                'List A - DocumentTitle - Second Section': (),
                'List A - IssuingAuthority - Second Section': (),
                'List A - DocumentNumber - Second Section': (.13*width,.645*height,.358*width,.663*height),
                'List A - Document Expiration Date - Second Section': (.22*width,.6624*height,.358*width,.683*height),
                'DateOfHire': (.162*width,.711*height,.273*width,.726*height),
                #'ApartmentNo': (.58*width,.233*height,.685*width,.2454*height)
                }
        
    elif (formNumber == '03/08/13') & (page_number == 7):
        global image_coords_030813_pg7
        image_coords_030813_pg7 = {'LastName':(.06*width,.225*height,.345*width,.246*height),
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
    
    elif (formNumber == '03/08/13') & (page_number == 8):
        global image_coords_030813_pg8
        image_coords_030813_pg8 = {'List A - DocumentTitle': (.06*width,.205*height,.344*width,.222*height),
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

    elif (formNumber == '11/14/2016') & (page_number == 1):
        global image_coords_111416_pg1
        image_coords_111416_pg1 = {'LastName':(.06*width,.242*height,.335*width,.265*height),
                        'FirstName': (.34*width,.242*height,.582*width,.265*height), 
                        'MiddleInitial': (.586*width,.242*height,.689*width,.265*height),
                        'MaidenName': (.69*width,.242*height,.93*width,.265*height),
                        'StreetAddress': (.06*width,.279*height,.39*width,.303*height),
                        #'AptNo': (.395*width,.279*height,.493*width,.303*height),
                        'City': (.494*width,.279*height,.738*width,.303*height),
                        'State': (.74*width,.279*height,.802*width,.303*height),
                        'Zip': (.804*width,.279*height,.93*width,.303*height),
                        'DateOfBirth': (.06*width,.318*height,.241*width,.346*height),
                        'SocialSecurity': (.243*width,.318*height,.438*width,.346*height),
                        'EmailAddress': (.439*width,.318*height,.72*width,.346*height),
                        'Telephone': (.721*width,.318*height,.93*width,.346*height),
                        'Attestation': (.06*width,.407*height,.085*width,.492*height),
                        'Alien # for Permanent Residence': (.573*width,.45*height,.775*width,.47*height),
                        'Date Expiration of Work Authorization': (.573*width,.472*height,.705*width,.492*height),
                        'Alien # for Work Authorization': (.36*width,.534*height,.61*width,.561*height),
                        'Admission # for Work Authorization': (),
                        'I-94 Admission Number': (.265*width,.56*height,.61*width,.593*height),
                        'ForeignPassport': (.25*width,.592*height,.61*width,.622*height),
                        'Country of Issuance': (.225*width,.622*height,.61*width,.645*height),
                        'TranslatorName': (),
                        'TranslatorAddress': (.06*width,.861*height,.48*width,.886*height),
                        'TranslatorDateOfSignature': (.68*width,.789*height,.93*width,.808*height)}
   
    elif (formNumber == '11/14/2016') & (page_number == 2):
        global image_coords_111416_pg2
        image_coords_111416_pg2 = {'List A - DocumentTitle': (.06*width,.232*height,.335*width,.25*height),
                        'List A - IssuingAuthority': (.06*width,.262*height,.335*width,.278*height),
                        'List A - DocumentNumber': (.06*width,.29*height,.335*width,.306*height),
                        'List A - ExpirationDate': (.06*width,.318*height,.335*width,.334*height),
                        'List A - DocumentTitle - Second Section': (.06*width,.35*height,.335*width,.366*height),
                        'List A - IssuingAuthority - Second Section': (.06*width,.379*height,.335*width,.394*height),
                        'List A - DocumentNumber - Second Section': (.06*width,.405*height,.335*width,.421*height),
                        'List A - Document Expiration Date - Second Section': (.06*width,.434*height,.335*width,.45*height),
                        'List B - DocumentTitle': (.361*width,.232*height,.65*width,.25*height),
                        'List B - IssuingAuthority': (.361*width,.262*height,.65*width,.278*height),
                        'List B - DocumentNumber': (.361*width,.29*height,.65*width,.306*height),
                        'List B - ExpirationDate': (.361*width,.318*height,.65*width,.334*height),
                        'List C - DocumentTitle': (.658*width,.232*height,.94*width,.25*height),
                        'List C - IssuingAuthority': (.658*width,.262*height,.94*width,.278*height),
                        'List C - DocumentNumber': (.658*width,.29*height,.94*width,.306*height),
                        'List C - Expiration Date': (.658*width,.318*height,.94*width,.334*height),
                        'DateOfHire': (.462*width,.61*height,.6*width,.63*height),
                        'Name of Employee Representative': (.06*width,.686*height,.64*width,.706*height),
                        'Title': (.62*width,.652*height,.942*width,.672*height),
                        'EmployerBusinessName': (.662*width,.686*height,.942*width,.706*height),
                        'EmployerStreetAddress': (.06*width,.72*height,.5*width,.741*height),
                        'Date Signed by Employer': (.44*width,.652*height,.62*width,.672*height),
                        'List A - DocumentTitle - Third Section': (.06*width,.465*height,.335*width,.481*height),
                        'List A - IssuingAuthority - Third Section': (.06*width,.494*height,.335*width,.509*height),
                        'List A - DocumentNumber - Third Section': (.06*width,.52*height,.335*width,.535*height),
                        'List A - Document Expiration Date - Third Section': (.06*width,.549*height,.335*width,.565*height),
                        'Employee Info from Section 1 - LastName': (.27*width,.177*height,.51*width,.193*height),
                        'Employee Info from Section 1 - FirstName':(.514*width,.177*height,.705*width,.193*height), 
                        'Employee Info from Section 1 - Middle Initial': (.706*width,.177*height,.746*width,.193*height)
                        }

    elif (formNumber == '07/17/17') & (page_number == 0):
        global image_coords_071717_pg1 
        image_coords_071717_pg1 = {'LastName':(.065*width,.241*height,.347*width,.265*height),
                        'FirstName': (.35*width,.241*height,.592*width,.265*height), 
                        'MiddleInitial': (.596*width,.241*height,.694*width,.265*height),
                        'MaidenName': (.695*width,.241*height,.945*width,.265*height),
                        'StreetAddress': (.065*width,.279*height,.39*width,.302*height),
                        #'AptNo': (.405*width,.279*height,.495*width,.302*height),
                        'City': (.5*width,.279*height,.74*width,.302*height),
                        'State': (.746*width,.279*height,.805*width,.302*height),
                        'Zip': (.808*width,.279*height,.945*width,.302*height),
                        'DateOfBirth': (.066*width,.318*height,.25*width,.346*height),
                        'SocialSecurity': (.252*width,.318*height,.445*width,.346*height),
                        'EmailAddress': (.447*width,.318*height,.725*width,.346*height),
                        'Telephone': (.727*width,.318*height,.945*width,.346*height),
                        'Attestation': (.066*width,.407*height,.094*width,.49*height),
                        'Alien # for Permanent Residence': (.57*width,.449*height,.78*width,.468*height),
                        'Date Expiration of Work Authorization': (.57*width,.47*height,.72*width,.49*height),
                        'Alien # for Work Authorization': (.35*width,.537*height,.62*width,.56*height),
                        'Admission # for Work Authorization': (),
                        'I-94 Admission Number': (.28*width,.56*height,.62*width,.592*height),
                        'ForeignPassport': (.26*width,.593*height,.62*width,.623*height),
                        'Country of Issuance': (.23*width,.622*height,.62*width,.643*height),
                        'TranslatorName': (.53*width,.819*height,.945*width,.84*height),
                        'TranslatorAddress': (.068*width,.859*height,.46*width,.882*height),
                        'TranslatorDateOfSignature': (.688*width,.785*height,.945*width,.805*height)}

    elif (formNumber == '07/17/17') & (page_number == 1):
        global image_coords_071717_pg2 
        image_coords_071717_pg2 = {'List A - DocumentTitle': (.068*width,.23*height,.34*width,.249*height),
                        'List A - IssuingAuthority': (.068*width,.26*height,.34*width,.277*height),
                        'List A - DocumentNumber': (.068*width,.287*height,.34*width,.304*height),
                        'List A - ExpirationDate': (.068*width,.316*height,.34*width,.333*height),
                        'List A - DocumentTitle - Second Section': (.068*width,.347*height,.34*width,.365*height),
                        'List A - IssuingAuthority - Second Section': (.068*width,.376*height,.34*width,.393*height),
                        'List A - DocumentNumber - Second Section': (.068*width,.402*height,.34*width,.419*height),
                        'List A - Document Expiration Date - Second Section': (.068*width,.431*height,.34*width,.448*height),
                        'List B - DocumentTitle': (.365*width,.232*height,.655*width,.25*height),
                        'List B - IssuingAuthority': (.365*width,.26*height,.655*width,.277*height),
                        'List B - DocumentNumber': (.365*width,.287*height,.655*width,.304*height),
                        'List B - ExpirationDate': (.365*width,.316*height,.655*width,.333*height),
                        'List C - DocumentTitle': (.658*width,.232*height,.94*width,.25*height),
                        'List C - IssuingAuthority': (.658*width,.26*height,.94*width,.277*height),
                        'List C - DocumentNumber': (.658*width,.287*height,.94*width,.304*height),
                        'List C - Expiration Date': (.658*width,.316*height,.94*width,.333*height),
                        'DateOfHire': (.464*width,.61*height,.61*width,.63*height),
                        'Name of Employee Representative': (.068*width,.683*height,.64*width,.703*height),
                        'Title': (.625*width,.649*height,.945*width,.669*height),
                        'EmployerBusinessName': (.666*width,.683*height,.945*width,.703*height),
                        'EmployerStreetAddress': (.068*width,.7172*height,.5*width,.737*height),
                        'Date Signed by Employer': (.443*width,.649*height,.623*width,.669*height),
                        'List A - DocumentTitle - Third Section': (.068*width,.462*height,.34*width,.481*height),
                        'List A - IssuingAuthority - Third Section': (.068*width,.492*height,.34*width,.506*height),
                        'List A - DocumentNumber - Third Section': (.068*width,.517*height,.34*width,.532*height),
                        'List A - Document Expiration Date - Third Section': (.068*width,.546*height,.34*width,.562*height),
                        'Employee Info from Section 1 - LastName': (.274*width,.177*height,.514*width,.193*height),
                        'Employee Info from Section 1 - FirstName':(.516*width,.177*height,.708*width,.193*height), 
                        'Employee Info from Section 1 - Middle Initial': (.71*width,.177*height,.748*width,.193*height)
                        }
        
    elif (formNumber == '11-21-91(L)'):
        global image_coords_112191_L
        image_coords_112191_L = {'LastName':(.09*width,.155*height,.36*width,.173*height),
                'FirstName': (.37*width,.155*height,.53*width,.173*height), 
                'MiddleInitial': (.54*width,.155*height,.64*width,.173*height),
                'MaidenName': (.645*width,.155*height,.9*width,.173*height),
                'StreetAddress': (.09*width,.182*height,.52*width,.198*height),
                'City': (.09*width,.208*height,.345*width,.222*height),
                'State': (.346*width,.208*height,.53*width,.222*height),
                'Zip': (.54*width,.208*height,.64*width,.222*height),
                'DateOfBirth': (.645*width,.182*height,.9*width,.198*height),
                'SocialSecurity': (.645*width,.208*height,.9*width,.222*height),
                'Attestation': (.495*width,.233*height,.512*width,.264*height),
                'Alien # for Permanent Residence': (.722*width,.242*height,.89*width,.254*height),
                'Date Expiration of Work Authorization': (.679*width,.254*height,.79*width,.265*height),
                'Alien # for Work Authorization': (.637*width,.264*height,.89*width,.273*height),
                'Admission # for Work Authorization': (),
                'I-94 Admission Number': (),
                'ForeignPassport': (),
                'Country of Issuance': (),
                'TranslatorName': (.501*width,.343*height,.78*width,.355*height),
                'TranslatorAddress': (.15*width,.365*height,.62*width,.379*height),
                'TranslatorDateOfSignature': (.64*width,.365*height,.8*width,.379*height),
                'List A - DocumentTitle': (.171*width,.433*height,.328*width,.448*height),
                'List A - IssuingAuthority': (.181*width,.452*height,.328*width,.468*height),
                'List A - DocumentNumber': (.17*width,.469*height,.328*width,.486*height),
                'List A - Expiration Date': (.24*width,.49*height,.329*width,.507*height),
                'List B - DocumentTitle': (.375*width,.433*height,.595*width,.448*height),
                'List B - IssuingAuthority': (.375*width,.452*height,.595*width,.468*height),
                'List B - DocumentNumber': (.375*width,.469*height,.595*width,.486*height),
                'List B - Expiration Date': (.405*width,.49*height,.49*width,.507*height),
                'List C - DocumentTitle': (.63*width,.433*height,.87*width,.448*height),
                'List C - IssuingAuthority': (.63*width,.452*height,.87*width,.468*height),
                'List C - DocumentNumber': (.63*width,.469*height,.87*width,.486*height),                
                'List C - Expiration Date': (.66*width,.49*height,.765*width,.506*height),
                'List A - DocumentTitle - Second Section': (),
                'List A - IssuingAuthority - Second Section': (),
                'List A - DocumentNumber - Second Section': (.17*width,.507*height,.328*width,.525*height),
                'List A - Document Expiration Date - Second Section': (.24*width,.528*height,.329*width,.545*height),
                'DateOfHire': (.401*width,.574*height,.526*width,.585*height)
                #'ApartmentNo': ()
                }
   
    elif (formNumber == '11-21-91(R)'):
        global image_coords_112191_R
        image_coords_112191_R = {'LastName':(.048*width,.167*height,.36*width,.189*height),
                'FirstName': (.361*width,.167*height,.564*width,.189*height), 
                'MiddleInitial': (.57*width,.167*height,.676*width,.189*height),
                'MaidenName': (.68*width,.167*height,.96*width,.189*height),
                'StreetAddress': (.048*width,.202*height,.565*width,.221*height),
                'City': (.048*width,.23*height,.33*width,.251*height),
                'State': (.33*width,.23*height,.565*width,.251*height),
                'Zip': (.57*width,.23*height,.676*width,.251*height),
                'DateOfBirth': (.68*width,.202*height,.96*width,.221*height),
                'SocialSecurity': (.68*width,.23*height,.96*width,.251*height),
                'Attestation': (.515*width,.262*height,.535*width,.306*height),
                'Alien # for Permanent Residence': (.779*width,.274*height,.9*width,.288*height),
                'Date Expiration of Work Authorization': (.733*width,.289*height,.83*width,.302*height),
                'Alien # for Work Authorization': (.682*width,.302*height,.836*width,.315*height),
                'Admission # for Work Authorization': (),
                'I-94 Admission Number': (),
                'ForeignPassport': (),
                'Country of Issuance': (),
                'TranslatorName': (.515*width,.395*height,.87*width,.41*height),
                'TranslatorAddress': (.1*width,.4213*height,.66*width,.439*height),
                'TranslatorDateOfSignature': (.68*width,.4213*height,.87*width,.439*height),
                'List A - DocumentTitle': (.14*width,.498*height,.32*width,.518*height),
                'List A - IssuingAuthority': (.15*width,.52*height,.32*width,.54*height),
                'List A - DocumentNumber': (.14*width,.547*height,.32*width,.562*height),
                'List A - Expiration Date': (.22*width,.573*height,.32*width,.588*height),
                'List B - DocumentTitle': (.375*width,.498*height,.63*width,.518*height),
                'List B - IssuingAuthority': (.375*width,.52*height,.63*width,.54*height),
                'List B - DocumentNumber': (.375*width,.547*height,.63*width,.562*height),
                'List B - Expiration Date': (.395*width,.573*height,.505*width,.588*height),
                'List C - DocumentTitle': (.67*width,.498*height,.93*width,.518*height),
                'List C - IssuingAuthority': (.67*width,.52*height,.93*width,.54*height),
                'List C - DocumentNumber': (.67*width,.547*height,.93*width,.562*height),                
                'List C - Expiration Date': (.705*width,.573*height,.81*width,.588*height),
                'List A - DocumentTitle - Second Section': (),
                'List A - IssuingAuthority - Second Section': (),
                'List A - DocumentNumber - Second Section': (),
                'List A - Document Expiration Date - Second Section': (.22*width,.618*height,.32*width,.635*height),
                'DateOfHire': (.396*width,.671*height,.492*width,.683*height)
                #'ApartmentNo': (.566*width,.20*height,.676*width,.221*height)
                }
    
    else:
        print("Dimensions not found for form number" + formNumber)
        
def switchCoords(form_number, page_number):
    if form_number == '03/08/13':
        if page_number == 7:
            coords = image_coords_030813_pg7
            return(coords)
        elif page_number == 8:
            coords = image_coords_030813_pg8
            return(coords)
        else:
            print("This page does not contain data")
    elif form_number == '07/17/17':
        if page_number == 1:
            coords = image_coords_071717_pg1
            return(coords)
        elif page_number == 2:
            coords = image_coords_071717_pg2
            return(coords)
        else:
            print("This page does not contain data")        
    elif form_number == '11/14/2016':
        if page_number == 1:
            coords = image_coords_111416_pg1
            return(coords)
        elif page_number == 2:
            coords = image_coords_111416_pg2
            return(coords)
        else:
            print("This page does not contain data")  
    else:
        switcher = {
                '02/02/09': image_coords_020209,
                '05/07/87': image_coords_050787,
                '06/05/07': image_coords_060507,
                '08/07/09': image_coords_080709,
                '05/31/05': image_coords_053105,
                '11-21-91(L)': image_coords_112191_L,
                '11-21-91(R)': image_coords_112191_R
        }
        coords = switcher.get(form_number, "Invalid form number")
        return(coords)

def crop(image, coords):
    """
    @param image_path: The path to the image to edit
    @param coords: A tuple of x/y coordinates (x1, y1, x2, y2)
    @param saved_location: Path to save the cropped image
    """
    image_obj = PIL.Image.open(image)
    cropped_image = image_obj.crop(coords)
    swap = io.BytesIO()
    cropped_image.save(swap, 'png')
    return swap

######################################
########## main thread ###############
######################################

# Put the incoming FlowFile into a dataframe
flowFile = sys.stdin.buffer.read()
flowFile = io.BytesIO(flowFile)

# flowFile = open(r'C:\Users\Andrew Riffle\PycharmProjects\PDF-Data-Extraction\ocr\TestDataFiles\i-9_03-08-13.pdf', 'rb')
# flowFile = open(r'C:\Users\Andrew Riffle\PycharmProjects\PDF-Data-Extraction\ocr\TestDataFiles\i-9_08-07-09.pdf', 'rb')

# Declare the empty list of PNGs
PNGs = []

# convert multipage pdf to a list of images
with Image(file=flowFile, resolution=200) as img:
    # loop through pages of PDF and convert each into a separate PNG
    for i, page in enumerate(img.sequence):
        with Image(page) as im:
            im.alpha_channel = False
            im.format = 'png'

            swapPNG = io.BytesIO()
            im.save(swapPNG)
            PNGs.append(swapPNG)

crops = {}

for i in range(len(PNGs)):
    print('Page ' + str(i))
    page = PNGs[i]
    form_number = findFormNumber(page)

    # check if form_number found. If not, continue to next image.
    if form_number is None:
        continue

    # The pages are in order in the PNGs list, so just grab the index
    page_number = i
    page_number2 = findPageNumber(page)

    # Set the global vars to the correct coordinates
    setImageCoords(page, form_number, page_number2)

    # Get coords for given form and page number
    coords = switchCoords(form_number, page_number2)
    
    #list which forms have the page number on their data page
    has_page_number = ['11-21-91(R)', '05/31/05', '07/17/17', '08/07/09',
                       '11/14/2016', '02/02/09', '03/08/13']
    
    #list which forms do not have the page number on their data page
    no_page_number = ['05/07/87', '11-21-91(L)', '06/05/07']

    page_info = {'05/07/87': 0,
                 '11-21-91(L)': 0,
                 '11-21-91(R)': 2,
                 '05/31/05': 2,
                 '06/05/07': 3,
                 '02/02/09': 4,
                 '08/07/09': 4,
                 '03/08/13': (7,8),
                 '11/14/2016': (1,2),
                 '07/17/17': (1,2)
                 }

    #determine if this file contains data based on page_info lookup table and then
    #crop the image if it does
    if isinstance(page_info[form_number], int):
        if form_number in no_page_number:
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
                        print(key + ' : ' + str(value))
                        swap = crop(page, value)
                        crops[key] = swap
            else:
                    print("Not a data form")
        else:
            if page_info[form_number] == page_number2:
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
                        print(key + ' : ' + str(value))
                        swap = crop(page, value)
                        crops[key] = swap
            else:
                    print("Not a data form")
    else:
        if form_number in no_page_number:
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
                        print(key + ' : ' + str(value))
                        swap = crop(page, value)
                        crops[key] = swap
            else:
                    print("Not a data form")
        else:
            if (page_info[form_number][0] == page_number2) or (page_info[form_number][1] == page_number2):
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
                        print(key + ' : ' + str(value))
                        swap = crop(page, value)
                        crops[key] = swap
            else:
                print("Not a data form")

    ocrs = {}
    for key, value in crops.items():
        ocrs[key] = (pytesseract.image_to_string(PIL.Image.open(crops[key])))

output = json.dumps(ocrs)
sys.stdout.write(output)