"""
Module 5: Security Audit Report Generator
-----------------------------------------
Generates professional Markdown audit reports from pipeline output.
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Add project root to Python path for imports
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))


def generate_report(org, trace_matrix, explanations, output_path="reporting/output/security_audit_report.md"):
    """
    Generate a professional security audit report.
    
    Args:
        org (dict): Organization info from Module 1
        trace_matrix (list): Trace matrix from Module 3
        explanations (list): LLM explanations from Module 4
        output_path (str): Output file path
    
    Returns:
        str: Path to generated report
    """
    template_path = Path("reporting/templates/report.md")
    template = template_path.read_text(encoding="utf-8")

    # Build risk table
    risk_rows = []
    for item in trace_matrix:
        risk_rows.append(
            f"| {item['trace']['priority_rank']} | {item['title']} | "
            f"{item['trace']['final_score']} | {item['trace']['risk_level']} |"
        )
    risk_table = "\n".join(risk_rows)

    # Build detailed findings
    details = []
    for item, exp in zip(trace_matrix, explanations):
        details.append(f"""
### 🔴 Priority {item['trace']['priority_rank']}: {item['title']}

- **Vulnerability ID:** {item['vuln_id']}
- **Affected Asset:** {item['affected_asset']}
- **Base Score:** {item['trace']['base_score']}
- **Final Score:** {item['trace']['final_score']}
- **Risk Level:** {item['trace']['risk_level']}

**Context Modifiers Applied:**
```json
{json.dumps(item['trace']['modifiers_applied'], indent=2)}
```

**Evidence:**  
{item['evidence']}

**AI Analyst Explanation:**  
{exp['explanation']}

**Source:** {item['source_file']}

---
""")

    detailed_findings = "\n".join(details)

    # Replace template placeholders
    report = template \
        .replace("{{org_name}}", org["name"]) \
        .replace("{{org_type}}", org["type"]) \
        .replace("{{date}}", datetime.now().strftime("%Y-%m-%d")) \
        .replace("{{total_findings}}", str(len(trace_matrix))) \
        .replace("{{risk_table}}", risk_table) \
        .replace("{{detailed_findings}}", detailed_findings)

    # Ensure output directory exists
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Write Markdown report
    output_file.write_text(report, encoding="utf-8")
    print(f"✅ Markdown report generated: {output_file}")
    
    # Convert Markdown to HTML using Pandoc
    html_path = output_file.with_suffix('.html')
    try:
        subprocess.run(
            ["pandoc", str(output_file), "-o", str(html_path), "--standalone"],
            check=True,
            capture_output=True
        )
        print(f"✅ HTML report generated: {html_path}")
        
        # Convert HTML to PDF using WeasyPrint
        try:
            from reporting.pdf_generator import html_to_pdf
            pdf_path = output_file.with_suffix('.pdf')
            html_to_pdf(str(html_path), str(pdf_path))
        except Exception as e:
            print(f"⚠️  PDF generation skipped: {e}")
            
    except subprocess.CalledProcessError as e:
        print(f"⚠️  HTML generation skipped (Pandoc not available): {e}")
    except FileNotFoundError:
        print(f"⚠️  HTML generation skipped (Pandoc not installed)")
    
    return str(output_file)


# Simple standalone test
if __name__ == "__main__":
    print("=" * 70)
    print("MODULE 5: REPORT GENERATOR - STANDALONE TEST")
    print("=" * 70)
    
    # Sample data for testing
    sample_org = {
        "name": "Sample Organization",
        "type": "Finance"
    }
    
    sample_trace = [
        {
            "vuln_id": "VULN-001",
            "title": "Unencrypted Database Connection",
            "affected_asset": "User DB Server",
            "source_file": "scan1.xml",
            "trace": {
                "base_score": 9.8,
                "final_score": 10.0,
                "risk_level": "Critical",
                "priority_rank": 1,
                "modifiers_applied": {
                    "org_type": "+1.0",
                    "data_criticality": "+0.8",
                    "internet_exposed": "+0.5",
                    "patch_delay": "+0.3"
                }
            },
            "evidence": "Port 3306 open without TLS encryption. Database credentials transmitted in plaintext."
        }
    ]
    
    sample_explanations = [
        {
            "vuln_id": "VULN-001",
            "title": "Unencrypted Database Connection",
            "priority_rank": 1,
            "explanation": "This vulnerability is critical for a financial organization because unencrypted database connections expose sensitive customer data to interception. The Priority 1 ranking reflects the combination of a high base severity (9.8) and organizational context factors including financial sector requirements, high data criticality, and internet exposure."
        }
    ]
    
    try:
        report_path = generate_report(
            org=sample_org,
            trace_matrix=sample_trace,
            explanations=sample_explanations
        )
        
        print(f"\n✓ Report generated successfully!")
        print(f"  Location: {report_path}")
        print("\n" + "=" * 70)
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
