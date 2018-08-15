import java.io.File;
        import java.io.IOException;
        import org.apache.pdfbox.pdmodel.PDDocument;
        import org.apache.pdfbox.util.PDFTextStripper;
        import org.apache.pdfbox.util.PDFTextStripperByArea;
        import java.awt.Rectangle;
        import java.util.List;
        import org.apache.pdfbox.pdmodel.PDPage;

public class backup {
    public static void main(String[] args) {

        try {
            File file = new File("/Users/doctor_ew/IdeaProjects/I9PDFExtractor/nocr/2011_i9_test_noPIV.pdf");
            PDDocument document = PDDocument.load(file);
            PDFTextStripperByArea stripper = new PDFTextStripperByArea();
            stripper.setSortByPosition(true);
            Rectangle rect1 = new Rectangle(38, 275, 15, 100);
            Rectangle rect2 = new Rectangle(54, 275, 40, 100);
            stripper.addRegion("row1column1", rect1);
            stripper.addRegion("row1column2", rect2);
            List allPages = document.getDocumentCatalog().getAllPages();
            List<PDPage> pages = document.getDocumentCatalog().getAllPages();

            int j = 0;

            for (PDPage page : pages) {
                stripper.extractRegions(page);
                stripper.setSortByPosition(true);
                List<String> regions = stripper.getRegions();
                for (String region : regions) {
                    String text = stripper.getTextForRegion(region);
                    System.out.println("Region: " + region + " on Page " + j);
                    System.out.println("\tText: \n" + text);
                }
            }
        } catch (Exception e){
            System.out.println(e.getMessage());
        }
    }
}