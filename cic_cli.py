"""
CIC - Cybersecurity Intelligence & Compliance
Unified CLI for Complete Audit Pipeline
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """
    Run a command and handle errors
    
    Args:
        cmd (list): Command to run
        description (str): Description of the step
    """
    print(f"\n{'='*70}")
    print(f"🔹 {description}")
    print(f"{'='*70}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        return False
    except FileNotFoundError:
        print(f"❌ Command not found: {cmd[0]}")
        return False


def main():
    """
    Run the complete audit pipeline
    """
    print("\n" + "="*70)
    print("🚀 CIC - OFFLINE AI SECURITY AUDIT PIPELINE")
    print("="*70)
    print("Running Modules 1-5 in sequence...")
    print("="*70)
    
    # Module 1: Data Ingestion & Parser
    if not run_command(
        ["python", "parser.py"],
        "MODULE 1: Data Ingestion & Parser"
    ):
        sys.exit(1)
    
    # Module 2: Risk Scoring (Integration Test)
    if not run_command(
        ["python", "test_integration.py"],
        "MODULE 2: Adaptive Risk Scoring"
    ):
        sys.exit(1)
    
    # Module 3: Traceability Matrix
    if not run_command(
        ["python", "test_trace_matrix.py"],
        "MODULE 3: Traceability Matrix"
    ):
        sys.exit(1)
    
    # Module 4: LLM Explanations
    if not run_command(
        ["python", "llm/explain_from_trace.py"],
        "MODULE 4: LLM Explainability"
    ):
        sys.exit(1)
    
    # Module 5: Report Generation (Markdown + HTML + PDF)
    if not run_command(
        ["python", "reporting/report_generator.py"],
        "MODULE 5: Report Generation"
    ):
        sys.exit(1)
    
    # Final summary
    print("\n" + "="*70)
    print("🎉 AUDIT PIPELINE COMPLETED SUCCESSFULLY!")
    print("="*70)
    
    # Check for generated files
    output_dir = Path("reporting/output")
    pdf_file = output_dir / "security_audit_report.pdf"
    html_file = output_dir / "security_audit_report.html"
    md_file = output_dir / "security_audit_report.md"
    
    print("\n📄 Generated Reports:")
    if md_file.exists():
        print(f"   ✅ Markdown: {md_file}")
    if html_file.exists():
        print(f"   ✅ HTML:     {html_file}")
    if pdf_file.exists():
        print(f"   ✅ PDF:      {pdf_file}")
    else:
        print(f"   ⚠️  PDF:      Not generated (check WeasyPrint installation)")
    
    print("\n" + "="*70)
    print("🏆 Your security audit report is ready for presentation!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
