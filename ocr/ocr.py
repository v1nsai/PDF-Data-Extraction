from wand.image import Image
import sys
import io
import PIL

def findFormNumber(png):
    """
    @@file - the file to find the form number of
    This function takes in a file and spits out the form number associated with it
    """

    # crop bottom of image
    im = PIL.Image.open(png)
    width, height = im.size
    while True:
        try:
            cropped_img = crop(image, (.04 * width, .955 * height, .95 * width, .98 * height))
            # run tesseract on crop
            text = pytesseract.image_to_string(PIL.Image.open(cropped_img))
            # clean output to just pull revision date with either dd/mm/yy or dd-mm-yy format
            matches = re.findall(
                '(\d{2}[\/ ](\d{2}|January|Jan|February|Feb|March|Mar|April|Apr|May|May|June|Jun|July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec)[\/ ]\d{2,4})'
                , text)
            # return output
            if matches:
                for match in matches:
                    return (match[0])
                    break
            elif not matches:
                print('nothing found in first crop')
                cropped_img = crop(image, (.04 * width, .925 * height, .95 * width, .955 * height))

                # run tesseract on crop
                text = pytesseract.image_to_string(PIL.Image.open(cropped_img))

                # clean output to just pull revision date with either dd/mm/yy or dd-mm-yy format
                matches = re.findall(
                    '(\d{2}[\/ ](\d{2}|January|Jan|February|Feb|March|Mar|April|Apr|May|May|June|Jun|July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec)[\/ ]\d{2,4})'
                    , text)

                # output answer
                for match in matches:
                    return (match[0])

# Put the incoming FlowFile into a dataframe
flowFile = sys.stdin.buffer.read()
flowFile = io.BytesIO(flowFile)

# Declare the empty list of PNGs
PNGs = []

# convert multipage pdf to a list of images
with Image(file=flowFile, resolution=200) as img:
    # loop through pages of PDF and convert each into a separate PNG
    for i, page in enumerate(img.sequence):
        with Image(page) as im:
            img.alpha_channel = False
            img.format = 'png'

            swapPNG = io.BytesIO()
            img.save(swapPNG)
            PNGs = PNGs.append(swapPNG)

form_num = findFormNumber(PNGs[0])