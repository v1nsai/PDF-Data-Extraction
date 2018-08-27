import org.apache.pdfbox.pdmodel.PDDocument
import org.apache.pdfbox.util.PDFTextStripperByArea
import java.awt.Rectangle
import org.apache.pdfbox.pdmodel.PDPage
import java.nio.charset.StandardCharsets

pwidth = 0.00
pheight = 0.00

//Using percentages of page width and height is better at handling size variation than pixels
//These functions handle the conversion
def widthByPercent(double percent) {
    return (int)Math.round(percent * pwidth)
}

def heightByPercent(double percent) {
    return (int)Math.round(percent * pheight)
}

//Find the form version and load the JSON containing the proper coords
def getFormVersion(PDPage page, PDFTextStripperByArea stripper) {
    //Grab the top and bottom of the page, concatenate them and look for the Rev. date
    Rectangle formvertop = new Rectangle(widthByPercent(0), heightByPercent(0), widthByPercent(100), heightByPercent(8))
    stripper.addRegion("formvertop", formvertop)
    Rectangle formverbottom = new Rectangle(widthByPercent(0), heightByPercent(92), widthByPercent(100), heightByPercent(8))
    stripper.addRegion("formverbottom", formverbottom)
    stripper.setSortByPosition(true)
    stripper.extractRegions(page)
    List<String> regions = stripper.getRegions()
    String ver = ''
    for (String region : regions) {
        String swap = stripper.getTextForRegion(region)
        ver = ver + swap
    }

    if(ver.contains('(Rev. 08/07/09)')){
        return '08/07/09'
    }
}

def getCoords(String version) {
    def swapcoords = [:]
    if(version.contains("08/07/09")) {
        swapcoords = [
                'pages': [0],
                'LastName': [0.02, 0.195, 0.27, 0.01],
                'FirstName': [0.29, 0.195, 0.23, 0.01],
                'MiddleInitial': [0.615, 0.195, 0.09, 0.01],
                'MaidenName': [0.69, 0.195, 0.26, 0.01],
                'StreetAddress': [0.03, 0.23, 0.54, 0.01],
                'ApartmentNo': [0.57, 0.23, 0.12, 0.01],
                'City': [0.02, 0.265, 0.26, 0.01],
                'State': [0.305, 0.265, 0.2, 0.01],
                'Zip': [0.56, 0.265, 0.11, 0.01],
                'DateOfBirth': [0.7, 0.23, 0.21, 0.01],
                'SocialSecurity': [0.70, 0.265, 0.165, 0.01],
                'citizen': [0.485, 0.295, 0.40, 0.01],
                'national': [0.485, 0.31, 0.40, 0.01],
                'resident': [0.485, 0.33, 0.40, 0.01],
                'alien': [0.485, 0.35, 0.40, 0.01],
                'Alien # for Permanent Residence': [0.747, 0.33, 0.216, 0.01],
                'Date Expiration of Work Authorization': [],
                'I-94 Admission Number': [],
                'ForeignPassport': [],
                'Country of Issuance': [],
                'Alien # for Work Authorization': [0.833, 0.349, 0.13, 0.01],
                'TranslatorAddress': [0.8, 0.48, 0.4, 0.01],
                'TranslatorName': [0.52, 0.445, 0.25, 0.01],
                'TranslatorDateOfSignature': [0.7, 0.48, 0.2, 0.01],
                'List A - DocumentTitle': [0.12, 0.561, 0.215, 0.01],
                'List A - IssuingAuthority': [0.13, 0.58, 0.2, 0.01],
                'List A - DocumentNumber': [0.105, 0.605, 0.2, 0.01],
                'List A - Expiration Date': [0.205, 0.62, 0.14, 0.01],
                'List B - DocumentTitle': [0.385, 0.565, 0.2, 0.01],
                'List B - IssuingAuthority': [0.385, 0.585, 0.2, 0.01],
                'List B - DocumentNumber': [0.385, 0.605, 0.2, 0.01],
                'List B - Expiration Date': [0.385, 0.625, 0.2, 0.01],
                'List C - DocumentTitle': [0.725, 0.565, 0.2, 0.01],
                'List C - IssuingAuthority': [0.725, 0.585, 0.2, 0.01],
                'List C - DocumentNumber': [0.725, 0.605, 0.2, 0.01],
                'List C - Expiration Date': [0.725, 0.625, 0.2, 0.01],
                'List A - DocumentNumber - Second Section': [0.105, 0.64, 0.2, 0.01],
                'List A - Expiration Date -  Second Section': [0.205, 0.66, 0.2, 0.01],
                'DateOfHire': []
        ]
    }
    return swapcoords
}

def flowFile = session.get()
if(!flowFile) return

flowFile = session.write(flowFile, { inputStream, outputStream ->
    try {
        //Create objects
//        inputStream = session.read(flowFile)
//        File inputStream = new File("/Users/doctor_ew/IdeaProjects/PDF-Data-Extraction/nocr/2011_test_i9.pdf");
        PDDocument document = PDDocument.load(inputStream)
        PDFTextStripperByArea stripper = new PDFTextStripperByArea()

        //Get the first page
        List<PDPage> allPages = document.getDocumentCatalog().getAllPages()
//        PDPage page = allPages.get(0)

        def boxMap = [:]
        def version = getFormVersion(page, stripper)
        def coords = getCoords(version) //coords is a java.util.LinkedHashMap

        for(int page_num : coords['pages']) {
            // Get the page
            PDPage page = allpages.get(page_num)

            //Convert to percentages, safer to use on variable sized documents and easier to use
            //height = 841.8901 width = 595.28
            pheight = page.getMediaBox().getHeight()
            pwidth = page.getMediaBox().getWidth()

            // Reinitialize stripper to flush out the old coords for finding form version
            stripper = new PDFTextStripperByArea()

            // A better way to loop through the elements
            def keys = coords.keySet()
            for(String key : keys) {
                if(key == 'pages' || coords[key] == null || coords[key].size() < 4)
                    continue
                def swapRectangle = new Rectangle(
                        widthByPercent(coords[key][0]),
                        heightByPercent(coords[key][1]),
                        widthByPercent(coords[key][2]),
                        heightByPercent(coords[key][3])
                )
                stripper.addRegion(key, swapRectangle)
            }

            //Load the results into a JSON
            stripper.setSortByPosition(true)
            stripper.extractRegions(page)
            regions = stripper.getRegions()
            for (String region : regions) {
                String box = stripper.getTextForRegion(region)
                boxMap.put(region, box)
            }
        }

        //Loop through all the elements of coords
//        coords.each { element ->
//            //If the element has coords assigned to it, fill in the coords and region name with the key and values
//            if (element.value.size() == 4) {
//                def swap = new Rectangle(
//                        widthByPercent(element.value[0]),
//                        heightByPercent(element.value[1]),
//                        widthByPercent(element.value[2]),
//                        heightByPercent(element.value[3])
//                )
//                stripper.addRegion(element.key, swap)
//            }
//        }

        // Add the filename as an attribute
        boxMap.put('File', flowFile.getAttribute('filename'))

        json = boxMap.inspect()
        json = json.replace('\\n', '')
        json = json.replace('\\r', '')
        json = json.replace(',"', ',\n"')

        outputStream.write(json.getBytes(StandardCharsets.UTF_8))
//        print(json)

    } catch (Exception e){
        System.out.println(e.getMessage())
        session.transfer(flowFile, REL_FAILURE)
    }
} as StreamCallback)
session.transfer(flowFile, REL_SUCCESS)
