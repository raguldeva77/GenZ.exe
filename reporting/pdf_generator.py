"""
PDF Generator Module
Converts HTML reports to PDF using xhtml2pdf (Windows-compatible)
"""

from xhtml2pdf import pisa
from pathlib import Path
import re


def clean_html_for_pdf(html_content):
    """
    Clean HTML content to be compatible with xhtml2pdf
    Removes all CSS and adds basic inline styling
    """
    # Remove all <style> blocks
    html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove style attributes
    html_content = re.sub(r'\s+style="[^"]*"', '', html_content)
    
    # Add basic inline CSS for readability
    basic_css = """
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        h1 { color: #333; border-bottom: 2px solid #333; padding-bottom: 10px; }
        h2 { color: #555; margin-top: 30px; }
        h3 { color: #777; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f0f0f0; font-weight: bold; }
        code, pre { background-color: #f5f5f5; padding: 2px 4px; font-family: monospace; }
        pre { padding: 10px; }
    </style>
    """
    
    # Insert basic CSS before </head> or at the start of <body>
    if '</head>' in html_content:
        html_content = html_content.replace('</head>', basic_css + '</head>')
    elif '<body' in html_content:
        html_content = html_content.replace('<body', basic_css + '<body', 1)
    
    return html_content


def html_to_pdf(html_path, pdf_path):
    """
    Convert HTML file to PDF
    
    Args:
        html_path (str): Path to input HTML file
        pdf_path (str): Path to output PDF file
    """
    try:
        # Ensure paths exist
        html_file = Path(html_path)
        if not html_file.exists():
            raise FileNotFoundError(f"HTML file not found: {html_path}")
        
        # Read and clean HTML content
        html_content = html_file.read_text(encoding='utf-8')
        html_content = clean_html_for_pdf(html_content)
        
        # Convert HTML to PDF
        with open(pdf_path, 'wb') as pdf_file:
            pisa_status = pisa.CreatePDF(
                html_content,
                dest=pdf_file,
                encoding='utf-8'
            )
        
        if pisa_status.err:
            print(f"⚠️  PDF generated with {pisa_status.err} warnings")
        
        print(f"✅ PDF generated: {pdf_path}")
        
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        raise
