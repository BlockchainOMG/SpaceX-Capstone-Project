# How to Convert HTML Presentation to PDF

## Method 1: Using Web Browser (Easiest - Recommended)

### For Chrome/Chromium/Edge:

1. **Open the HTML file:**
   ```bash
   # Navigate to the project directory
   cd /home/tolga/Documents/SpaceX_Capstone_Project
   
   # Open in default browser
   xdg-open SpaceX_Capstone_Presentation.html
   ```
   
   Or double-click `SpaceX_Capstone_Presentation.html` in your file manager.

2. **Print to PDF:**
   - Press `Ctrl + P` (or `Cmd + P` on Mac)
   - In the print dialog:
     - Destination: Select "Save as PDF"
     - Layout: Portrait
     - Paper size: A4 or Letter
     - Margins: Default
     - Scale: Fit to page (if needed)
     - Options: ✓ Background graphics
   - Click "Save"
   - Save as: `SpaceX_Capstone_Presentation.pdf`

### For Firefox:

1. Open the HTML file
2. Press `Ctrl + P` (or `Cmd + P` on Mac)
3. Select "Print to File" or "Microsoft Print to PDF"
4. Choose PDF format
5. Click "Print" and save

---

## Method 2: Using Command Line Tools

### Option A: Install wkhtmltopdf

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install wkhtmltopdf

# Then convert
cd /home/tolga/Documents/SpaceX_Capstone_Project
wkhtmltopdf SpaceX_Capstone_Presentation.html SpaceX_Capstone_Presentation.pdf
```

### Option B: Install Chromium and use headless mode

```bash
# Install chromium
sudo apt-get install chromium-browser

# Convert to PDF
chromium-browser --headless --disable-gpu --print-to-pdf=SpaceX_Capstone_Presentation.pdf file:///home/tolga/Documents/SpaceX_Capstone_Project/SpaceX_Capstone_Presentation.html
```

### Option C: Using Python weasyprint

```bash
# Install weasyprint
pip install weasyprint

# Create a simple conversion script
python3 << 'EOF'
from weasyprint import HTML

HTML('SpaceX_Capstone_Presentation.html').write_pdf(
    'SpaceX_Capstone_Presentation.pdf'
)
print("PDF created successfully!")
EOF
```

---

## Method 3: Online Conversion Tools (No Installation Required)

### Recommended Online Tools:

1. **HTML to PDF Converter**
   - Website: https://www.html2pdf.app/
   - Upload `SpaceX_Capstone_Presentation.html`
   - Click "Convert"
   - Download PDF

2. **PDF.io**
   - Website: https://pdf.io/html2pdf/
   - Upload HTML file
   - Convert and download

3. **CloudConvert**
   - Website: https://cloudconvert.com/html-to-pdf
   - Upload HTML file
   - Convert and download

**Note:** These services are free but require internet connection and uploading your file.

---

## Method 4: Using LibreOffice Writer

1. Open LibreOffice Writer
2. File → Open
3. Select `SpaceX_Capstone_Presentation.html`
4. File → Export as PDF
5. Choose settings and export

---

## Troubleshooting

### Issue: Slides appear on single page

**Solution:** The HTML is designed for print with page breaks. Use Method 1 (Browser print) which respects page breaks.

### Issue: CSS not rendered correctly

**Solution:** Ensure you're opening the HTML file directly (not copying content). The CSS is embedded in the HTML file.

### Issue: Images not showing

**Solution:** Make sure you're in the correct directory and all image paths are correct.

---

## Quality Settings for Best Results

When converting to PDF, use these settings:

- **Page Size:** A4 or Letter (1024x768 slide dimensions)
- **Orientation:** Landscape (for slide format) or Portrait (for document format)
- **Margins:** Minimal or None
- **Scale:** 100% or "Fit to page"
- **Background Graphics:** Enabled/On
- **Color Mode:** Color (not grayscale)
- **Quality:** High or Maximum

---

## Verification

After creating the PDF, verify:

- ✓ All 21 slides are present
- ✓ Colors and formatting are correct
- ✓ Tables and charts are readable
- ✓ Text is not cut off
- ✓ File size is reasonable (typically 1-5 MB)

---

## Alternative: Use the Markdown Version

If PDF conversion is problematic, you can:

1. Use `PRESENTATION_CONTENT.md` directly
2. Import into PowerPoint/Google Slides
3. Or use Markdown presentation tools like:
   - Marp: https://marp.app/
   - reveal.js: https://revealjs.com/
   - Slidev: https://sli.dev/

---

## Quick Command (Recommended)

If you have a web browser available:

```bash
cd /home/tolga/Documents/SpaceX_Capstone_Project
xdg-open SpaceX_Capstone_Presentation.html
# Then press Ctrl+P and save as PDF
```

---

## Need Help?

If you encounter issues:

1. Check that all dependencies are installed
2. Verify the HTML file opens correctly in a browser
3. Try a different conversion method
4. Contact support or check the README.md for more information

**The HTML presentation is fully functional and can be used as-is for presentations. PDF conversion is optional for submission purposes.**

