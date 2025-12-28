"""
PDF Report Generator
-------------------
Converts Markdown audit report to PDF using Pandoc.

Requirements:
- Pandoc installed: https://pandoc.org/installing.html
"""

import subprocess
from pathlib import Path


def convert_to_pdf(markdown_path, pdf_path=None):
    """
    Convert Markdown report to PDF using Pandoc.
    
    Args:
        markdown_path (str): Path to Markdown file
        pdf_path (str): Output PDF path (optional)
    
    Returns:
        str: Path to generated PDF
    """
    markdown_file = Path(markdown_path)
    
    if not markdown_file.exists():
        raise FileNotFoundError(f"Markdown file not found: {markdown_path}")
    
    # Default PDF path
    if pdf_path is None:
        pdf_path = markdown_file.with_suffix('.pdf')
    
    # Check if Pandoc is installed
    try:
        subprocess.run(
            ["pandoc", "--version"],
            capture_output=True,
            check=True
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise RuntimeError(
            "Pandoc not found. Please install from: https://pandoc.org/installing.html"
        )
    
    # Convert to PDF
    print(f"Converting {markdown_file.name} to PDF...")
    result = subprocess.run(
        [
            "pandoc",
            str(markdown_file),
            "-o", str(pdf_path),
            "--pdf-engine=xelatex",  # Better Unicode support
            "-V", "geometry:margin=1in",  # Professional margins
            "-V", "fontsize=11pt"  # Readable font size
        ],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        # Try without xelatex if it fails
        print("Trying alternative PDF engine...")
        result = subprocess.run(
            [
                "pandoc",
                str(markdown_file),
                "-o", str(pdf_path)
            ],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            raise RuntimeError(f"PDF conversion failed: {result.stderr}")
    
    print(f"✓ PDF generated: {pdf_path}")
    return str(pdf_path)


if __name__ == "__main__":
    # Convert the security audit report
    try:
        pdf_path = convert_to_pdf(
            "reporting/output/security_audit_report.md"
        )
        print("\n" + "=" * 70)
        print("PDF CONVERSION SUCCESSFUL")
        print("=" * 70)
        print(f"PDF Location: {pdf_path}")
        print("\nYou can now submit this PDF to judges!")
        print("=" * 70)
        
    except FileNotFoundError as e:
        print(f"\n✗ Error: {e}")
        print("\nGenerate the Markdown report first:")
        print("  python test_full_pipeline.py")
        
    except RuntimeError as e:
        print(f"\n✗ Error: {e}")
        print("\nInstall Pandoc:")
        print("  Windows: https://pandoc.org/installing.html")
        print("  Or use online converter: https://www.markdowntopdf.com/")
