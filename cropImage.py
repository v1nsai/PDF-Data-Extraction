# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 15:19:51 2018

@author: Brandon Croarkin
"""

from PIL import Image
import os
import re

#listing out the (x1, y1, x2, y2) coordinates of information on each of 
#the different forms
image_coords_020209 = {'LastName':(.055*width,.168*height,.37*width,.205*height),
                'FirstName': (.368*width,.169*height,.61*width,.205*height), 
                'DateOfBirth': (.688*width,.205*height,.95*width,.240*height),
                'SocialSecurity': (.688*width,.241*height,.95*width,.275*height),
                'Attestation': (.49*width,.292*height,.515*width,.365*height),
                'Alien/AdmissionNo1': (.515*width,.325*height,.945*width,.350*height),
                'Alien/AdmissionNo2': (.515*width,.346*height,.945*width,.365*height),
                'StreetAddress': (.055*width,.205*height,.58*width,.240*height),
                'City': (.055*width,.241*height,.35*width,.275*height),
                'State': (.345*width,.241*height,.58*width,.275*height),
                'Zip': (.58*width,.241*height,.688*width,.275*height),
                'WorkAuthorization': (.515*width,.362*height,.945*width,.377*height),
                'Translator': (.513*width,.433*height,.94*width,.47*height),
                'DocumentTitle1': (.05*width,.564*height,.363*width,.59*height),
                'DocumentTitle2': (.38*width,.564*height,.65*width,.59*height),
                'DocumentTitle3': (.7*width,.564*height,.95*width,.59*height),
                'DocumentNumber1': (.05*width,.606*height,.363*width,.63*height),
                'DocumentNumber2': (.38*width,.606*height,.65*width,.63*height),
                'DocumentNumber3': (.7*width,.606*height,.95*width,.63*height),
                'DocumentNumber4': (.05*width,.645*height,.363*width,.665*height),
                'DateOfHire': (.053*width,.712*height,.278*width,.728*height),
                'MiddleInitial': (.610*width,.169*height,.686*width,.205*height),
                'ApartmentNo': (.58*width,.205*height,.685*width,.240*height)}

image_coords_030813_pg1 = {'LastName':(),
                'FirstName': (), 
                'DateOfBirth': (),
                'SocialSecurity': (),
                'Attestation': (),
                'Alien/AdmissionNo1': (),
                'Alien/AdmissionNo2': (),
                'StreetAddress': (),
                'City': (),
                'State': (),
                'Zip': (),
                'WorkAuthorization': (),
                'Translator': (),
                'DocumentTitle1': (),
                'DocumentTitle2': (),
                'DocumentTitle3': (),
                'DocumentNumber1': (),
                'DocumentNumber2': (),
                'DocumentNumber3': (),
                'DocumentNumber4': (),
                'DateOfHire': (),
                'MiddleInitial': (),
                'ApartmentNo': ()}

image_coords_030813_pg2 = {'LastName':(),
                'FirstName': (), 
                'DateOfBirth': (),
                'SocialSecurity': (),
                'Attestation': (),
                'Alien/AdmissionNo1': (),
                'Alien/AdmissionNo2': (),
                'StreetAddress': (),
                'City': (),
                'State': (),
                'Zip': (),
                'WorkAuthorization': (),
                'Translator': (),
                'DocumentTitle1': (),
                'DocumentTitle2': (),
                'DocumentTitle3': (),
                'DocumentNumber1': (),
                'DocumentNumber2': (),
                'DocumentNumber3': (),
                'DocumentNumber4': (),
                'DateOfHire': (),
                'MiddleInitial': (),
                'ApartmentNo': ()}

image_coords_050787 = {'LastName':(.069*width,.1215*height,.38*width,.1525*height),
                'FirstName': (.38*width,.1215*height,.56*width,.1525*height), 
                'DateOfBirth': (.07*width,.1819*height,.51*width,.211*height),
                'SocialSecurity': (.51*width,.1819*height,.91*width,.211*height),
                'Attestation': (.085*width,.228*height,.12*width,.275*height),
                'Alien/AdmissionNo1': (.503*width,.24*height,.655*width,.26*height),
                'Alien/AdmissionNo2': (.732*width,.26*height,.911*width,.276*height),
                'Alien/AdmissionNo3': (.235*width,.2735*height,.369*width,.29*height),
                'StreetAddress': (.08*width,.1519*height,.38*width,.182*height),
                'City': (.38*width,.1519*height,.56*width,.182*height),
                'State': (.56*width,.1519*height,.735*width,.182*height),
                'Zip': (.735*width,.1519*height,.92*width,.182*height),
                'WorkAuthorization': (),
                'Translator': (.51*width,.394*height,.833*width,.424*height),
                'DocumentTitle1': (.06*width,.632*height,.09*width,.72*height),
                'DocumentTitle2': (.38*width,.61*height,.4*width,.73*height),
                'DocumentTitle3': (.7*width,.61*height,.72*width,.73*height),
                'DocumentNumber1': .076*width,.782*height,.315*width,.8*height
                'DocumentNumber2': .3913*width,.782*height,.63*width,.8*height
                'DocumentNumber3': (.712*width,.782*height,.95*width,.8*height),
                'DateOfHire': (.785*width,.925*height,.95*width,.953*height),
                'MiddleInitial': (.56*width,.1215*height,.74*width,.1525*height)}

image_coords_053105 = {'LastName':(),
                'FirstName': (), 
                'DateOfBirth': (),
                'SocialSecurity': (),
                'Attestation': (),
                'Alien/AdmissionNo1': (),
                'Alien/AdmissionNo2': (),
                'StreetAddress': (),
                'City': (),
                'State': (),
                'Zip': (),
                'WorkAuthorization': (),
                'Translator': (),
                'DocumentTitle1': (),
                'DocumentTitle2': (),
                'DocumentTitle3': (),
                'DateOfHire': (),
                'MiddleInitial': (),
                'ApartmentNo': ()}

image_coords_060507 = {'LastName':(.055*width,.185*height,.36*width,.221*height),
                'FirstName': (.36*width,.185*height,.58*width,.221*height), 
                'DateOfBirth': (.69*width,.2215*height,.95*width,.25*height),
                'SocialSecurity': (.688*width,.257*height,.94*width,.291*height),
                'Attestation': (.45*width,.306*height,.4752*width,.355*height),
                'Alien/AdmissionNo1': (.71*width,.318*height,.95*width,.332*height),
                'Alien/AdmissionNo2': (.61*width,.351*height,.95*width,.37*height),
                'StreetAddress': (.055*width,.2215*height,.57*width,.2454*height),
                'City': (.055*width,.257*height,.35*width,.291*height),
                'State': (.35*width,.257*height,.57*width,.291*height),
                'Zip': (.58*width,.257*height,.685*width,.291*height),
                'WorkAuthorization': (.652*width,.334*height,.95*width,.351*height),
                'TranslatorName': (.515*width,.433*height,.88*width,.469*height),
                'TranslatorAddress': (.1*width,.47*height,.677*width,.497*height),
                'TranslatorSignDate': (.678*width,.47*height,.9*width,.497*height)
                'DocumentTitle1': (.14*width,.57*height,.36*width,.59*height),
                'DocumentTitle2': (),
                'DocumentTitle3': (),
                'DocumentNumber1': (),
                'DocumentNumber2': (),
                'DocumentNumber3': (),
                'DocumentNumber4': (),
                'DocumentNumber1': (),
                'DocumentNumber2': (),
                'DocumentNumber3': (),
                'DocumentNumber4': (),
                'DateOfHire': (),
                'MiddleInitial': (.58*width,.185*height,.685*width,.221*height),
                'ApartmentNo': (.58*width,.2215*height,.685*width,.2454*height)}

image_coords_080709 = {'LastName':(),
                'FirstName': (), 
                'DateOfBirth': (),
                'SocialSecurity': (),
                'Attestation': (),
                'Alien/AdmissionNo1': (),
                'Alien/AdmissionNo2': (),
                'StreetAddress': (),
                'City': (),
                'State': (),
                'Zip': (),
                'WorkAuthorization': (),
                'Translator': (),
                'DocumentTitle1': (),
                'DocumentTitle2': (),
                'DocumentTitle3': (),
                'DocumentNumber1': (),
                'DocumentNumber2': (),
                'DocumentNumber3': (),
                'DocumentNumber4': (),
                'DateOfHire': (),
                'MiddleInitial': (),
                'ApartmentNo': ()}

image_coords_111416_pg1 = {'LastName':(),
                'FirstName': (), 
                'DateOfBirth': (),
                'SocialSecurity': (),
                'Attestation': (),
                'Alien/AdmissionNo1': (),
                'Alien/AdmissionNo2': (),
                'StreetAddress': (),
                'City': (),
                'State': (),
                'Zip': (),
                'WorkAuthorization': (),
                'Translator': (),
                'DocumentTitle1': (),
                'DocumentTitle2': (),
                'DocumentTitle3': (),
                'DocumentNumber1': (),
                'DocumentNumber2': (),
                'DocumentNumber3': (),
                'DocumentNumber4': (),
                'DateOfHire': (),
                'MiddleInitial': (),
                'ApartmentNo': ()}

image_coords_111416_pg2 = {'LastName':(),
                'FirstName': (), 
                'DateOfBirth': (),
                'SocialSecurity': (),
                'Attestation': (),
                'Alien/AdmissionNo1': (),
                'Alien/AdmissionNo2': (),
                'StreetAddress': (),
                'City': (),
                'State': (),
                'Zip': (),
                'WorkAuthorization': (),
                'Translator': (),
                'DocumentTitle1': (),
                'DocumentTitle2': (),
                'DocumentTitle3': (),
                'DocumentNumber1': (),
                'DocumentNumber2': (),
                'DocumentNumber3': (),
                'DocumentNumber4': (),
                'DateOfHire': (),
                'MiddleInitial': (),
                'ApartmentNo': ()}

image_coords_071717_pg1 = {'LastName':(.077*width,.229*height,.356*width,.271*height),
                'FirstName': (.355*width,.233*height,.597*width,.272*height), 
                'DateOfBirth': (.077*width,.3034*height,.26*width,.3465*height),
                'SocialSecurity': (.26*width,.305*height,.452*width,.349*height),
                'Attestation': (.077*width,.405*height,.108*width,.49*height),
                'Alien/AdmissionNo1': (2800,3210,3850,3350),
                'Alien/AdmissionNo2': (1900,3740,3100,3950),
                'Alien/AdmissionNo3': (1420,3930,3100,4160),
                'Alien/AdmissionNo4': (1350,4110,3100,4320),
                'StreetAddress': (.077*width,.266*height,.41*width,.306*height),
                'City': (.505*width,.271*height,.745*width,.309*height),
                'State': (.746*width,.271*height,.81*width,.309*height),
                'Zip': (.81*width,.271*height,.948*width,.311*height),
                'WorkAuthorization': (2880,3350,3620,3500),
                'TranslatorLN': (420,5440,2650,5680),
                'TranslatorFN': (2660,5430,4600,5680),
                'DocumentTitle': (),
                'DocumentNumber': (),
                'DateOfHire': (),
                'ApartmentNo': (.408*width,.271*height,.505*width,.309*height),
                'MiddleInitial': (.596*width,.234*height,.696*width,.272*height),
                'Email': (.450*width,.308*height,.731*width,.351*height),
                'Telephone': (.729*width,.308*height,.948*width,.352*height)}

image_coords_071717_pg2 = {'LastName':(.077*width,.229*height,.356*width,.271*height),
                'FirstName': (.355*width,.233*height,.597*width,.272*height), 
                'DateOfBirth': (.077*width,.3034*height,.26*width,.3465*height),
                'SocialSecurity': (.26*width,.305*height,.452*width,.349*height),
                'Attestation': (.077*width,.405*height,.108*width,.49*height),
                'Alien/AdmissionNo1': (2800,3210,3850,3350),
                'Alien/AdmissionNo2': (1900,3740,3100,3950),
                'Alien/AdmissionNo3': (1420,3930,3100,4160),
                'Alien/AdmissionNo4': (1350,4110,3100,4320),
                'StreetAddress': (.077*width,.266*height,.41*width,.306*height),
                'City': (.505*width,.271*height,.745*width,.309*height),
                'State': (.746*width,.271*height,.81*width,.309*height),
                'Zip': (.81*width,.271*height,.948*width,.311*height),
                'WorkAuthorization': (2880,3350,3620,3500),
                'TranslatorLN': (420,5440,2650,5680),
                'TranslatorFN': (2660,5430,4600,5680),
                'DocumentTitle': (),
                'DocumentNumber': (),
                'DateOfHire': (),
                'ApartmentNo': (.408*width,.271*height,.505*width,.309*height),
                'MiddleInitial': (.596*width,.234*height,.696*width,.272*height),
                'Email': (.450*width,.308*height,.731*width,.351*height),
                'Telephone': (.729*width,.308*height,.948*width,.352*height)}

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
 
 
if __name__ == '__main__':
    #image = 'Python Crops/Original.png'
    
    #Make a vector of PNG files in a directory so it can repeat 
    #process on all files in directory
    images = []
    folder_location = 'C:\\Users\\Brandon Croarkin\\Documents\\GreenZone\\OCR\\I9 Forms - PNG\\TextCleaned'
    for image in os.listdir(folder_location):
        if image.endswith(".png"):
            images.append(image)
    
    for image in images:
        #image_name removes the Python Crops and .png from the image variable to 
        #give the file a unique file name
        image_names = []
        image_names = image_names.append(re.search(r'(.*?)(?=\.)',image).group())
        
        #loop through the coordinates for each attribute and create a new image
        for key, value in image_coords_071717_pg1.items():
            crop(image, value, 'CroppedImages/' + image_name + '_' + key +'.png')
    
        #delete the original image so NiFi doesn't repeat the process on the image
        #os.remove('Python Crops/' + image)
    
    #croppedImages_Folder_Location = 'C:\\Users\\Brandon Croarkin\\Documents\\GreenZone\\OCR\\PythonCroppedImages'
    #croppedImages = []
    #for image in os.listdir(croppedImages_Folder_Location):
    #    if image.endswith(".png"):
    #        croppedImages.append(image)
    #
    #for image in croppedImages:
    #    originalFile = re.search('r(.*?)(?=\_)',image).group()
        
        #find original file (what comes before the underscore)


##################TESTING
        
##Below is just for testing for the coordinates
if __name__ == '__main__':
   image = 'i-9_06-05-07(Filled)page-2.png'
   im = Image.open('i-9_06-05-07(Filled)page-2.png')
   width, height = im.size
   crop(image, (.39*width,.57*height,.62*width,.585*height), 
        'CroppedImages/Test.png')
        

    
    

        

