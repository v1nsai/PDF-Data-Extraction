import groovy.json.JsonSlurper
import org.apache.pdfbox.pdmodel.PDDocument
import org.apache.pdfbox.util.PDFTextStripperByArea
import java.awt.Rectangle
import org.apache.pdfbox.pdmodel.PDPage
import com.google.gson.Gson
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

def getFormVersion(PDPage page) {
    //Find the form version and load the JSON containing the proper coords
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

def setCoords(version) {
    def jsonSlurper = new JsonSlurper()
    if(version.contains("08/07/09")) {
        coords = jsonSlurper.parseText '''
            {"LastName": [0.055, 0.180, 0.37, 0.204],
               "FirstName": [0.368, 0.180, 0.61, 0.205],
               "MiddleInitial": [0.610, 0.180, 0.686, 0.205],
               "MaidenName": [0.69, 0.18, 0.94, 0.205],
               "StreetAddress": [0.055, 0.217, 0.58, 0.240],
               "City": [0.055, 0.252, 0.35, 0.275],
               "DateOfBirth": [0.688, 0.217, 0.95, 0.240],
               "SocialSecurity": [0.688, 0.253, 0.95, 0.275],
               "State": [0.345, 0.252, 0.58, 0.275],
               "Zip": [0.58, 0.252, 0.688, 0.275],
               "EmailAddress": [],
               "Telephone": [],
               "Attestation": [0.49, 0.292, 0.515, 0.365],
               "Alien # for Permanent Residence": [
               0.722, 0.325, 0.94, 0.345],
               "Date Expiration of Work Authorization": [
               0.805, 0.362, 0.955, 0.377],
               "Alien # for Work Authorization": [
               0.81, 0.346, 0.955, 0.365],
               "I-94 Admission Number": [],
               "Foreign Passport": [],
               "Country of Issuance": [],
               "TranslatorName": [0.513, 0.443, 0.94, 0.469],
               "TranslatorAddress": [0.104, 0.482, 0.67, 0.505],
               "TranslatorDateOfSignature": [0.68, 0.482, 0.94, 0.505],
               "List A - DocumentTitle": [0.145, 0.564, 0.363, 0.586],
               "List A - IssuingAuthority": [0.15, 0.586, 0.363, 0.605],
               "List A - DocumentNumber": [0.126, 0.606, 0.363, 0.625],
               "List A - DocumentExpirationDate": [
               0.215, 0.625, 0.363, 0.644],
               "List A - DocumentTitle - Second Section": [],
               "List A - IssuingAuthority - Second Section": [],
               "List A - DocumentNumber - Second Section": [
               0.13, 0.644, 0.363, 0.662],
               "List A - Document Expiration Date - Second Section": [
               0.215, 0.662, 0.363, 0.682],
               "List B - DocumentTitle": [0.38, 0.561, 0.64, 0.585],
               "List B - IssuingAuthority": [0.38, 0.585, 0.64, 0.605],
               "List B - DocumentNumber": [0.38, 0.6052, 0.64, 0.6245],
               "List B - DocumentExpirationDate": [
               0.38, 0.6245, 0.64, 0.6445],
               "List C - DocumentTitle": [0.7, 0.561, 0.95, 0.585],
               "List C - IssuingAuthority": [0.7, 0.585, 0.95, 0.605],
               "List C - DocumentNumber": [0.7, 0.6052, 0.95, 0.6245],
               "List C - DocumentExpirationDate": [
               0.7, 0.6245, 0.95, 0.6445],
               "DateOfHire": [0.16, 0.711, 0.278, 0.726],
               "Name of Employee Representative": [
               0.394, 0.752, 0.698, 0.777],
               "Title": [0.698, 0.752, 0.95, 0.777],
               "EmployerBusinessName": [0.05, 0.7875, 0.698, 0.808],
               "EmployerStreetAddress": [],
               "Date Signed by Employer": [0.698, 0.7875, 0.95, 0.808],
               "List A - DocumentTitle - Third Section": [],
               "List A - IssuingAuthority - Third Section": [],
               "List A - DocumentNumber - Third Section": [],
               "List A - Document Expiration Date - Third Section": [],
               "Employee Info from Section 1": []}
        '''
        return coords
    }
}

def flowFile = session.get()
if(!flowFile) return

flowFile = session.write(flowFile, { inputStream, outputStream ->
    try {
        //Create objects
//        inputStream = session.read(flowFile)
        PDDocument document = PDDocument.load(inputStream)
        PDFTextStripperByArea stripper = new PDFTextStripperByArea()

        //Get the first page
        List<PDPage> allPages = document.getDocumentCatalog().getAllPages()
        PDPage page = allPages.get(0)

        //Convert to percentages, safer to use on variable sized documents and easier to use
        //height = 841.8901 width = 595.28
        pheight = page.getMediaBox().getHeight()
        pwidth = page.getMediaBox().getWidth()

        //Find the form version and load the JSON containing the proper coords
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
            //                System.out.println('it works')
        }

        //Define the areas to search and add them as search regions
        stripper = new PDFTextStripperByArea()
        //            Rectangle fullname = new Rectangle(widthByPercent(2), heightByPercent(19.5), widthByPercent(58), heightByPercent(1))
        //            stripper.addRegion("fullname", fullname)
        Rectangle LastName = new Rectangle(widthByPercent(2), heightByPercent(19.5), widthByPercent(27), heightByPercent(1))
        stripper.addRegion("LastName", LastName)
        Rectangle FirstName = new Rectangle(widthByPercent(29), heightByPercent(19.5), widthByPercent(23), heightByPercent(1))
        stripper.addRegion("FirstName", FirstName)
        Rectangle MiddleInitial = new Rectangle(widthByPercent(61.5), heightByPercent(19.5), widthByPercent(10), heightByPercent(1))
        stripper.addRegion("MiddleInitial", MiddleInitial)
        Rectangle MaidenName = new Rectangle(widthByPercent(70.5), heightByPercent(19.5), widthByPercent(26), heightByPercent(1))
        stripper.addRegion("MaidenName", MaidenName)
        Rectangle address = new Rectangle(widthByPercent(3), heightByPercent(23), widthByPercent(54), heightByPercent(1))
        stripper.addRegion("StreetAddress", address)
        Rectangle Apt = new Rectangle(widthByPercent(57), heightByPercent(23), widthByPercent(12), heightByPercent(1))
        stripper.addRegion("Apt", Apt)
        Rectangle DateOfBirth = new Rectangle(widthByPercent(70), heightByPercent(23), widthByPercent(21), heightByPercent(1))
        stripper.addRegion("DateOfBirth", DateOfBirth)
        Rectangle City = new Rectangle(widthByPercent(2), heightByPercent(26.5), widthByPercent(26), heightByPercent(1))
        stripper.addRegion("City", City)
        Rectangle State = new Rectangle(widthByPercent(30.5), heightByPercent(26.5), widthByPercent(20), heightByPercent(1))
        stripper.addRegion("State", State)
        Rectangle Zip = new Rectangle(widthByPercent(56), heightByPercent(26.5), widthByPercent(11), heightByPercent(1))
        stripper.addRegion("Zip", Zip)
        Rectangle SocialSecurity = new Rectangle(widthByPercent(70), heightByPercent(26.5), widthByPercent(16.5), heightByPercent(1))
        stripper.addRegion("SocialSecurity", SocialSecurity)
        Rectangle citizen = new Rectangle(widthByPercent(48.5), heightByPercent(29.5), widthByPercent(40), heightByPercent(1))
        stripper.addRegion("citizen", citizen)
        Rectangle national = new Rectangle(widthByPercent(48.5), heightByPercent(31), widthByPercent(40), heightByPercent(1))
        stripper.addRegion("national", national)
        Rectangle resident = new Rectangle(widthByPercent(48.5), heightByPercent(33), widthByPercent(40), heightByPercent(1))
        stripper.addRegion("resident", resident)
        Rectangle alien = new Rectangle(widthByPercent(48.5), heightByPercent(35), widthByPercent(40), heightByPercent(1))
        stripper.addRegion("alien", alien)
        Rectangle TranslatorName = new Rectangle(widthByPercent(52), heightByPercent(44.5), widthByPercent(25), heightByPercent(1))
        stripper.addRegion("TranslatorName", TranslatorName)
        Rectangle TranslatorAddress = new Rectangle(widthByPercent(8), heightByPercent(48), widthByPercent(40), heightByPercent(1))
        stripper.addRegion("TranslatorAddress", TranslatorAddress)
        Rectangle TranslatorDateOfSignature = new Rectangle(widthByPercent(70), heightByPercent(48), widthByPercent(20), heightByPercent(1))
        stripper.addRegion("TranslatorDateOfSignature", TranslatorDateOfSignature)
        Rectangle boxAdoctitle = new Rectangle(widthByPercent(12), heightByPercent(56), widthByPercent(21.5), heightByPercent(1))
        stripper.addRegion("List A - DocumentTitle", boxAdoctitle)
        Rectangle boxAissuer = new Rectangle(widthByPercent(13), heightByPercent(58), widthByPercent(20), heightByPercent(1))
        stripper.addRegion("List A - IssuingAuthority", boxAissuer)
        Rectangle boxAdocnumber1 = new Rectangle(widthByPercent(10.5), heightByPercent(60.5), widthByPercent(20), heightByPercent(1))
        stripper.addRegion("List A - DocumentNumber", boxAdocnumber1)
        Rectangle boxAexpiration1 = new Rectangle(widthByPercent(20.5), heightByPercent(62), widthByPercent(14), heightByPercent(1))
        stripper.addRegion("List A - DocumentExpirationDate", boxAexpiration1)
        Rectangle boxAdocnumber2 = new Rectangle(widthByPercent(10.5), heightByPercent(64), widthByPercent(20), heightByPercent(1))
        stripper.addRegion("List A - DocumentTitle - Second Section", boxAdocnumber2)
        Rectangle boxAexpiration2 = new Rectangle(widthByPercent(20.5), heightByPercent(66), widthByPercent(20), heightByPercent(1))
        stripper.addRegion("List A - Document Expiration Date - Second Section", boxAexpiration2)
        Rectangle boxBline1 = new Rectangle(widthByPercent(38.5), heightByPercent(56.5), widthByPercent(20), heightByPercent(1))
        stripper.addRegion("List B - IssuingAuthority", boxBline1)
        Rectangle boxBline2 = new Rectangle(widthByPercent(38.5), heightByPercent(58.5), widthByPercent(20), heightByPercent(1))
        stripper.addRegion("List B DocumentTitle", boxBline2)
        Rectangle boxBline3 = new Rectangle(widthByPercent(38.5), heightByPercent(60.5), widthByPercent(20), heightByPercent(1))
        stripper.addRegion("List B DocumentNumber", boxBline3)
        Rectangle boxBline4 = new Rectangle(widthByPercent(38.5), heightByPercent(62.5), widthByPercent(20), heightByPercent(1))
        stripper.addRegion("List B DocumentExpirationDate", boxBline4)
        Rectangle boxCline1 = new Rectangle(widthByPercent(72.5), heightByPercent(56.5), widthByPercent(20), heightByPercent(1))
        stripper.addRegion("List C - IssuingAuthority", boxCline1)
        Rectangle boxCline2 = new Rectangle(widthByPercent(72.5), heightByPercent(58.5), widthByPercent(20), heightByPercent(1))
        stripper.addRegion("List C DocumentTitle", boxCline2)
        Rectangle boxCline3 = new Rectangle(widthByPercent(72.5), heightByPercent(60.5), widthByPercent(20), heightByPercent(1))
        stripper.addRegion("List C DocumentNumber", boxCline3)
        Rectangle boxCline4 = new Rectangle(widthByPercent(72.5), heightByPercent(62.5), widthByPercent(20), heightByPercent(1))
        stripper.addRegion("List C DocumentExpirationDate", boxCline4)
        Rectangle examinername = new Rectangle(widthByPercent(39), heightByPercent(75.5), widthByPercent(20), heightByPercent(1))
        stripper.addRegion("examinername", examinername)
        Rectangle examinertitle = new Rectangle(widthByPercent(71), heightByPercent(75.5), widthByPercent(20), heightByPercent(1))
        stripper.addRegion("examinertitle", examinertitle)
        Rectangle examinerbusiness_name = new Rectangle(widthByPercent(2), heightByPercent(78), widthByPercent(67), heightByPercent(1))
        stripper.addRegion("EmployerBusinessName", examinerbusiness_name)
        Rectangle examinerbusiness_address = new Rectangle(widthByPercent(2), heightByPercent(78), widthByPercent(21), heightByPercent(1))
        stripper.addRegion("EmployerBusinessAddress", examinerbusiness_address)
        Rectangle examinerdate = new Rectangle(widthByPercent(23), heightByPercent(78), widthByPercent(45), heightByPercent(1))
        stripper.addRegion("Date Signed by Employer", examinerdate)
        /*
        Rectangle updatename = new Rectangle(widthByPercent(2), heightByPercent(78), widthByPercent(67), heightByPercent(1))
        stripper.addRegion("updatename", updatename)
        Rectangle updaterehiredate = new Rectangle(widthByPercent(2), heightByPercent(78), widthByPercent(67), heightByPercent(1))
        stripper.addRegion("updaterehiredate", updaterehiredate)
        Rectangle updatedoctitle = new Rectangle(widthByPercent(2), heightByPercent(78), widthByPercent(67), heightByPercent(1))
        stripper.addRegion("updatedoctitle", updatedoctitle)
        Rectangle updatedocnum = new Rectangle(widthByPercent(2), heightByPercent(78), widthByPercent(67), heightByPercent(1))
        stripper.addRegion("updatedocnum", updatedocnum)
        Rectangle updateexpiration = new Rectangle(widthByPercent(2), heightByPercent(78), widthByPercent(67), heightByPercent(1))
        stripper.addRegion("updateexpiration", updateexpiration)
        Rectangle updatedate = new Rectangle(widthByPercent(2), heightByPercent(78), widthByPercent(67), heightByPercent(1))
        stripper.addRegion("updatedate", updatedate)
        */

        //Search the area and print the found text
        //            stripper.setSortByPosition(true)
        //            stripper.extractRegions(page)
        //            String text = stripper.getTextForRegion('lname')
        //            System.out.println(text)

        //Load the results into a JSON
        def boxMap = [:]
        stripper.setSortByPosition(true)
        stripper.extractRegions(page)
        regions = stripper.getRegions()
        for (String region : regions) {
            String box = stripper.getTextForRegion(region)
            boxMap.put(region, box)
        }

        // Add the filename as an attribute
        boxMap.put('File', flowFile.getAttribute('filename'))

        Gson gson = new Gson()
        json = gson.toJson(boxMap, LinkedHashMap.class)
        json = json.replace('\\n', '')
        json = json.replace('\\r', '')
        json = json.replace(',"', ',\n"')

        outputStream.write(json.getBytes(StandardCharsets.UTF_8))

    } catch (Exception e){
        System.out.println(e.getMessage())
        session.transfer(flowFile, REL_FAILURE)
    }
} as StreamCallback)
session.transfer(flowFile, REL_SUCCESS)

