# PDF Report Generation Guide

## Quick Start

### Option A: Using Pandoc (Recommended)

**Step 1: Install Pandoc**
- Download from: https://pandoc.org/installing.html
- Windows: Download and run the installer
- Verify installation: `pandoc --version`

**Step 2: Convert Report**
```bash
# Simple conversion
pandoc reporting/output/security_audit_report.md -o reporting/output/security_audit_report.pdf

# Professional formatting
pandoc reporting/output/security_audit_report.md -o reporting/output/security_audit_report.pdf --pdf-engine=xelatex -V geometry:margin=1in -V fontsize=11pt
```

**Step 3: Using the Helper Script**
```bash
python reporting/convert_to_pdf.py
```

---

### Option B: Online Converter (No Installation)

If you can't install Pandoc:
1. Go to: https://www.markdowntopdf.com/
2. Upload `security_audit_report.md`
3. Download the generated PDF

---

### Option C: VS Code Extension

1. Install "Markdown PDF" extension in VS Code
2. Open `security_audit_report.md`
3. Right-click → "Markdown PDF: Export (pdf)"

---

## Troubleshooting

### Pandoc Not Found
```bash
# Check if installed
pandoc --version

# If not found, download from:
https://pandoc.org/installing.html
```

### PDF Engine Error
If you get a LaTeX error, try the simple command:
```bash
pandoc security_audit_report.md -o security_audit_report.pdf
```

### Unicode/Font Issues
Install XeLaTeX for better Unicode support:
```bash
# Windows: Install MiKTeX
https://miktex.org/download
```

---

## For Judges

The generated PDF will include:
- ✅ Professional formatting
- ✅ Executive summary
- ✅ Risk tables
- ✅ Detailed findings with AI explanations
- ✅ Complete methodology
- ✅ Recommendations

Perfect for hackathon submission!
