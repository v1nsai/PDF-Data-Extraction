import com.google.gson.JsonObject;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.util.PDFTextStripperByArea;
import org.apache.pdfbox.pdmodel.PDPage;
import java.awt.Rectangle;
import java.io.File;
import java.io.FileOutputStream;
import java.io.PrintStream;
import java.util.List;

class nocr_java {

    private static float pwidth;
    private static float pheight;

    //Using percentages of page width and height is better at handling size variation than pixels
    //These functions handle the conversion
    private static int widthByPercent(double percent) {
        return (int)Math.round(percent * pwidth);
    }

    private static int heightByPercent(double percent) {
        return (int)Math.round(percent * pheight);
    }

    public static void main(String[] args) {

        try {
            //Create objects
            File file = new File("C:\\Users\\Andrew Riffle\\IdeaProjects\\I9PDFExtractor\\nocr\\2011_i9_test_noPIV.pdf");
            PDDocument document = PDDocument.load(file);
            PDFTextStripperByArea stripper = new PDFTextStripperByArea();

            //Get the first page
            List<PDPage> allPages = document.getDocumentCatalog().getAllPages();
            PDPage page = allPages.get(0);

            //Convert to percentages, safer to use on variable sized documents and easier to use
            //height = 841.8901 width = 595.28
            pheight = page.getMediaBox().getHeight() / 100;
            pwidth = page.getMediaBox().getWidth() / 100;

            //Find the form version and load the JSON containing the proper coords
            Rectangle formvertop = new Rectangle(widthByPercent(0), heightByPercent(0), widthByPercent(100), heightByPercent(8));
            stripper.addRegion("formvertop", formvertop);
            Rectangle formverbottom = new Rectangle(widthByPercent(0), heightByPercent(92), widthByPercent(100), heightByPercent(8));
            stripper.addRegion("formverbottom", formverbottom);
            stripper.setSortByPosition(true);
            stripper.extractRegions(page);
            List<String> regions = stripper.getRegions();
            String ver = "";
            for (String region : regions) {
                String swap = stripper.getTextForRegion(region);
                ver = ver + swap;
            }
            if(ver.contains("(Rev. 08/07/09)")){
//                System.out.println("it works");
            }

            //Define the areas to search and add them as search regions
            stripper = new PDFTextStripperByArea();
//            Rectangle fullname = new Rectangle(widthByPercent(2), heightByPercent(19.5), widthByPercent(58), heightByPercent(1))
//            stripper.addRegion("fullname", fullname)
            Rectangle lname = new Rectangle(widthByPercent(2), heightByPercent(19.5), widthByPercent(27), heightByPercent(1));
            stripper.addRegion("lname", lname);
            Rectangle fname = new Rectangle(widthByPercent(29), heightByPercent(19.5), widthByPercent(23), heightByPercent(1));
            stripper.addRegion("fname", fname);
            Rectangle middleinit = new Rectangle(widthByPercent(61.5), heightByPercent(19.5), widthByPercent(10), heightByPercent(1));
            stripper.addRegion("middleinit", middleinit);
            Rectangle maiden = new Rectangle(widthByPercent(70.5), heightByPercent(19.5), widthByPercent(26), heightByPercent(1));
            stripper.addRegion("maiden", maiden);
            Rectangle address = new Rectangle(widthByPercent(3), heightByPercent(23), widthByPercent(54), heightByPercent(1));
            stripper.addRegion("address", address);
            Rectangle apt = new Rectangle(widthByPercent(57), heightByPercent(23), widthByPercent(12), heightByPercent(1));
            stripper.addRegion("apt", apt);
            Rectangle dob = new Rectangle(widthByPercent(70), heightByPercent(23), widthByPercent(21), heightByPercent(1));
            stripper.addRegion("dob", dob);
            Rectangle city = new Rectangle(widthByPercent(2), heightByPercent(26.5), widthByPercent(26), heightByPercent(1));
            stripper.addRegion("city", city);
            Rectangle state = new Rectangle(widthByPercent(30.5), heightByPercent(26.5), widthByPercent(20), heightByPercent(1));
            stripper.addRegion("state", state);
            Rectangle zip = new Rectangle(widthByPercent(56), heightByPercent(26.5), widthByPercent(11), heightByPercent(1));
            stripper.addRegion("zip", zip);
            Rectangle ssn = new Rectangle(widthByPercent(70), heightByPercent(26.5), widthByPercent(16.5), heightByPercent(1));
            stripper.addRegion("ssn", ssn);
            Rectangle citizen = new Rectangle(widthByPercent(48.5), heightByPercent(29.5), widthByPercent(40), heightByPercent(1));
            stripper.addRegion("citizen", citizen);
            Rectangle national = new Rectangle(widthByPercent(48.5), heightByPercent(31), widthByPercent(40), heightByPercent(1));
            stripper.addRegion("national", national);
            Rectangle resident = new Rectangle(widthByPercent(48.5), heightByPercent(33), widthByPercent(40), heightByPercent(1));
            stripper.addRegion("resident", resident);
            Rectangle alien = new Rectangle(widthByPercent(48.5), heightByPercent(35), widthByPercent(40), heightByPercent(1));
            stripper.addRegion("alien", alien);
            Rectangle translatorname = new Rectangle(widthByPercent(52), heightByPercent(44.5), widthByPercent(25), heightByPercent(1));
            stripper.addRegion("translatorname", translatorname);
            Rectangle translatoraddress = new Rectangle(widthByPercent(8), heightByPercent(48), widthByPercent(40), heightByPercent(1));
            stripper.addRegion("translatoraddress", translatoraddress);
            Rectangle translatordate = new Rectangle(widthByPercent(70), heightByPercent(48), widthByPercent(20), heightByPercent(1));
            stripper.addRegion("translatordate", translatordate);
            Rectangle boxAdoctitle = new Rectangle(widthByPercent(12), heightByPercent(56), widthByPercent(21.5), heightByPercent(1));
            stripper.addRegion("boxAdoctitle", boxAdoctitle);
            Rectangle boxAissuer = new Rectangle(widthByPercent(13), heightByPercent(58), widthByPercent(20), heightByPercent(1));
            stripper.addRegion("boxAIssuer", boxAissuer);
            Rectangle boxAdocnumber1 = new Rectangle(widthByPercent(10.5), heightByPercent(60.5), widthByPercent(20), heightByPercent(1));
            stripper.addRegion("boxAdocnumber1", boxAdocnumber1);
            Rectangle boxAexpiration1 = new Rectangle(widthByPercent(20.5), heightByPercent(62), widthByPercent(20), heightByPercent(1));
            stripper.addRegion("boxAexpiration1", boxAexpiration1);
            Rectangle boxAdocnumber2 = new Rectangle(widthByPercent(10.5), heightByPercent(64), widthByPercent(20), heightByPercent(1));
            stripper.addRegion("boxAdocnumber2", boxAdocnumber2);
            Rectangle boxAexpiration2 = new Rectangle(widthByPercent(20.5), heightByPercent(66), widthByPercent(20), heightByPercent(1));
            stripper.addRegion("boxAexpiration2", boxAexpiration2);
            Rectangle boxBline1 = new Rectangle(widthByPercent(38.5), heightByPercent(56.5), widthByPercent(20), heightByPercent(1));
            stripper.addRegion("boxBline1", boxBline1);
            Rectangle boxBline2 = new Rectangle(widthByPercent(38.5), heightByPercent(58.5), widthByPercent(20), heightByPercent(1));
            stripper.addRegion("boxBline2", boxBline2);
            Rectangle boxBline3 = new Rectangle(widthByPercent(38.5), heightByPercent(60.5), widthByPercent(20), heightByPercent(1));
            stripper.addRegion("boxBline3", boxBline3);
            Rectangle boxBline4 = new Rectangle(widthByPercent(38.5), heightByPercent(62.5), widthByPercent(20), heightByPercent(1));
            stripper.addRegion("boxBline4", boxBline4);
            Rectangle boxCline1 = new Rectangle(widthByPercent(72.5), heightByPercent(56.5), widthByPercent(20), heightByPercent(1));
            stripper.addRegion("boxCline1", boxCline1);
            Rectangle boxCline2 = new Rectangle(widthByPercent(72.5), heightByPercent(58.5), widthByPercent(20), heightByPercent(1));
            stripper.addRegion("boxCline2", boxCline2);
            Rectangle boxCline3 = new Rectangle(widthByPercent(72.5), heightByPercent(60.5), widthByPercent(20), heightByPercent(1));
            stripper.addRegion("boxCline3", boxCline3);
            Rectangle boxCline4 = new Rectangle(widthByPercent(72.5), heightByPercent(62.5), widthByPercent(20), heightByPercent(1));
            stripper.addRegion("boxCline4", boxCline4);
            Rectangle examinername = new Rectangle(widthByPercent(39), heightByPercent(75.5), widthByPercent(20), heightByPercent(1));
            stripper.addRegion("examinername", examinername);
            Rectangle examinertitle = new Rectangle(widthByPercent(71), heightByPercent(75.5), widthByPercent(20), heightByPercent(1));
            stripper.addRegion("examinertitle", examinertitle);
            Rectangle examinerbusiness_address = new Rectangle(widthByPercent(2), heightByPercent(78), widthByPercent(67), heightByPercent(1));
            stripper.addRegion("examinerbusiness_address", examinerbusiness_address);
            Rectangle examinerdate = new Rectangle(widthByPercent(2), heightByPercent(78), widthByPercent(67), heightByPercent(1));
            stripper.addRegion("examinerdate", examinerdate);
            Rectangle updatename = new Rectangle(widthByPercent(2), heightByPercent(78), widthByPercent(67), heightByPercent(1));
            stripper.addRegion("updatename", updatename);
            Rectangle updaterehiredate = new Rectangle(widthByPercent(2), heightByPercent(78), widthByPercent(67), heightByPercent(1));
            stripper.addRegion("updaterehiredate", updaterehiredate);
            Rectangle updatedoctitle = new Rectangle(widthByPercent(2), heightByPercent(78), widthByPercent(67), heightByPercent(1));
            stripper.addRegion("updatedoctitle", updatedoctitle);
            Rectangle updatedocnum = new Rectangle(widthByPercent(2), heightByPercent(78), widthByPercent(67), heightByPercent(1));
            stripper.addRegion("updatedocnum", updatedocnum);
            Rectangle updateexpiration = new Rectangle(widthByPercent(2), heightByPercent(78), widthByPercent(67), heightByPercent(1));
            stripper.addRegion("updateexpiration", updateexpiration);
            Rectangle updatedate = new Rectangle(widthByPercent(2), heightByPercent(78), widthByPercent(67), heightByPercent(1));
            stripper.addRegion("updatedate", updatedate);

            //Search the area and print the found text
//            stripper.setSortByPosition(true)
//            stripper.extractRegions(page)
//            String text = stripper.getTextForRegion('lname')
//            System.out.println(text)

            //Load the results into a JSON
            JsonObject boxMap = new JsonObject();
            stripper.setSortByPosition(true);
            stripper.extractRegions(page);
            regions = stripper.getRegions();
            for (String region : regions) {
                String box = stripper.getTextForRegion(region);
                boxMap.addProperty(region, box);
            }
            String json = boxMap.toString();
            json = json.replace("\\n", "");
            json = json.replace("\\r", "");
            json = json.replace(",\"", ",\n\"");

            //Write JSON to file
            try (PrintStream out = new PrintStream(new FileOutputStream("C:\\Users\\Andrew Riffle\\IdeaProjects\\I9PDFExtractor\\nocr\\results.json"))) {
                out.print(json);
            } catch (Exception e) {
                System.out.println(e.getMessage());
            }
        } catch (Exception e){
            System.out.println(e.getMessage());
        }
    }
}