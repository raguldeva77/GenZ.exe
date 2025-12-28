# Module 5: Security Audit Report Generator

## Overview
Professional Markdown report generator that combines outputs from all pipeline modules into a judge-ready security audit document.

## Purpose
Creates comprehensive, human-readable audit reports suitable for:
- Security auditors
- Compliance officers  
- Executive stakeholders
- Hackathon judges

## Features

✅ **Professional Template** - Industry-standard audit report format  
✅ **Executive Summary** - High-level overview for decision-makers  
✅ **Risk Tables** - Priority-sorted vulnerability summary  
✅ **Detailed Findings** - Complete vulnerability analysis with AI explanations  
✅ **Methodology Section** - Documents the audit process  
✅ **Recommendations** - Actionable remediation guidance  
✅ **Markdown Output** - Easily convertible to PDF/HTML

## Architecture

```
reporting/
├── report_generator.py    # Main generator module
├── templates/
│   └── report.md         # Report template with placeholders
└── output/
    └── security_audit_report.md  # Generated reports
```

## Input Requirements

### From Module 1
- Organization info (name, type)

### From Module 3
- Trace matrix with complete reasoning trails

### From Module 4
- AI-generated explanations

## Output Structure

```markdown
# Security Audit Report

## Organization Overview
- Name, Industry, Date

## Executive Summary
- Total findings
- Key highlights

## Risk Summary Table
| Priority | Vulnerability | Score | Level |

## Detailed Findings
### Priority 1: Vulnerability Name
- IDs, scores, evidence
- Context modifiers
- AI explanation

## Methodology
- Module 1-4 process description

## Recommendations
- Immediate, short-term, long-term actions
```

## Usage

### Standalone Test
```bash
python reporting/report_generator.py
```

### Full Pipeline
```bash
python test_full_pipeline.py
```

## Template System

The report uses a simple placeholder replacement system:
- `{{org_name}}` - Organization name
- `{{org_type}}` - Industry/sector
- `{{date}}` - Report generation date
- `{{total_findings}}` - Number of vulnerabilities
- `{{risk_table}}` - Auto-generated risk summary table
- `{{detailed_findings}}` - Auto-generated detailed sections

## PDF Conversion

Convert Markdown to PDF using standard tools:
```bash
# Using pandoc
pandoc security_audit_report.md -o security_audit_report.pdf

# Using markdown-pdf (npm)
markdown-pdf security_audit_report.md
```

## Judge-Ready Features

1. **Professional Formatting** - Industry-standard structure
2. **Complete Transparency** - Full methodology documented
3. **Explainability** - Every decision traceable
4. **Actionable** - Clear recommendations
5. **Data Sovereignty** - Offline generation noted

## Example Output

See `reporting/output/security_audit_report.md` for a complete example generated from sample data.

## Judge-Ready Statement

> "Our report generator produces professional, audit-grade security assessments that combine deterministic risk scoring with AI-powered explanations, all while maintaining complete offline operation and full transparency into the assessment methodology."
