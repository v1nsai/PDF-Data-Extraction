import java.nio.charset.StandardCharsets
import org.apache.pdfbox.io.IOUtils
import org.apache.pdfbox.pdmodel.PDDocument
import org.apache.pdfbox.util.PDFTextStripperByArea
import java.awt.Rectangle
import org.apache.pdfbox.pdmodel.PDPage
import com.google.gson.Gson
import java.nio.charset.StandardCharsets
def flowFile = session.get()
flowFile = session.write(flowFile, { inputStream, outputStream ->
    try {
        //Load Flowfile contents
        PDDocument document = PDDocument.load(inputStream)
        PDFTextStripperByArea stripper = new PDFTextStripperByArea()
        //Get the first page
        List<PDPage> allPages = document.getDocumentCatalog().getAllPages()
        PDPage page = allPages.get(0)

    //Define the areas to search and add them as search regions
    stripper = new PDFTextStripperByArea()
    Rectangle lname = new Rectangle(25, 226, 240, 15)
    stripper.addRegion("lname", lname)
    Rectangle fname = new Rectangle(276, 226, 240, 15)
    stripper.addRegion("fname", fname)
    //Load the results into a JSON
    def boxMap = [:]
    stripper.setSortByPosition(true)
    stripper.extractRegions(page)
    regions = stripper.getRegions()
    for (String region : regions) {
        String box = stripper.getTextForRegion(region)
        boxMap.put(region, box)
    }
    Gson gson = new Gson()
    //Remove random noise from the output
    json = gson.toJson(boxMap, LinkedHashMap.class)
    json = json.replace('\\n', '')
    json = json.replace('\\r', '')
    json = json.replace(',"', ',\n"')
    //Overwrite flowfile contents with JSON
    outputStream.write(json.getBytes(StandardCharsets.UTF_8))
    } catch (Exception e){
        System.out.println(e.getMessage())
        session.transfer(flowFile, REL_FAILURE)
    }
} as StreamCallback)
session.transfer(flowFile, REL_SUCCESS)

//OVERWRITE
flowFile = session.get()
if(!flowFile) return
//def text = 'Hello world!' // Cast a closure with an inputStream and outputStream parameter to StreamCallback
flowFile = session.write(flowFile, {inputStream, outputStream ->
    text = IOUtils.toString(inputStream, StandardCharsets.UTF_8)
    outputStream.write(text.reverse().getBytes(StandardCharsets.UTF_8))
} as StreamCallback)
session.transfer(flowFile, REL_SUCCESS)

//WRITE
flowFile = session.get()
if(!flowFile) return
//def text = 'Hello world!'
// Cast a closure with an outputStream parameter to OutputStreamCallback
flowFile = session.write(flowFile, {outputStream ->
    outputStream.write(text.getBytes(StandardCharsets.UTF_8))
} as OutputStreamCallback)