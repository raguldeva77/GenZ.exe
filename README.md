# CIC - Cybersecurity Intelligence & Compliance

## 🚀 Quick Start (Recommended)

Run the complete audit pipeline with a single command:

```powershell
python cic_cli.py
```

This will automatically:
1. Parse vulnerability scan data (Module 1)
2. Calculate adaptive risk scores (Module 2)
3. Generate traceability matrix (Module 3)
4. Create LLM explanations (Module 4)
5. Generate Markdown, HTML, and **PDF** reports (Module 5)

**Output**: `reporting/output/security_audit_report.pdf`

---

# Module 1: Data Ingestion & Parser

## Overview

Enterprise-grade Python module for parsing cybersecurity vulnerability scan data from ZIP archives containing XML and JSON files. This module extracts, filters, and normalizes vulnerability findings into a unified JSON structure.

## Features

✅ **ZIP File Extraction** - Safely extracts and processes ZIP archives  
✅ **Multi-Format Support** - Parses both XML and JSON vulnerability scan files  
✅ **Severity Filtering** - Automatically filters for High and Critical findings only  
✅ **Data Normalization** - Converts all findings to a unified JSON structure  
✅ **Robust Error Handling** - Gracefully handles malformed files and missing fields  
✅ **Offline Operation** - No external APIs or cloud services required  
✅ **Clean Architecture** - Separation of concerns with modular functions

## Requirements

- Python 3.6+
- Standard library only (no external dependencies)

## Installation

No installation required. Simply ensure you have Python 3.6 or higher installed:

```bash
python --version
```

## Usage

### Basic Usage

```python
from parser import parse_vulnerability_scan

# Parse a ZIP file containing vulnerability scans
result = parse_vulnerability_scan(
    zip_path="sample_scan.zip",
    output_path="normalized_output.json"
)

# Access the normalized data
print(f"Organization: {result['organization']['name']}")
print(f"Total High/Critical findings: {len(result['findings'])}")
```

### Command Line Usage

```bash
python parser.py
```

**Note:** Update the `zip_file` variable in the `main()` function to point to your actual ZIP file.

### Programmatic Usage

```python
from parser import (
    extract_zip,
    parse_xml,
    parse_json,
    filter_severity,
    normalize_output
)

# Step-by-step processing
extract_dir = extract_zip("scans.zip")
xml_findings = parse_xml("scan1.xml")
json_findings = parse_json("scan2.json")

all_findings = xml_findings + json_findings
filtered = filter_severity(all_findings)
normalized = normalize_output(filtered)
```

## Input Format

### Expected ZIP Structure

```
sample_scan.zip
├── scan1.xml
├── scan2.json
└── subfolder/
    └── scan3.xml
```

### XML Format

```xml
<?xml version="1.0" encoding="UTF-8"?>
<scan>
  <organization name="Sample Organization" type="Finance" />
  <vulnerabilities>
    <vulnerability>
      <id>VULN-001</id>
      <title>Unencrypted Database</title>
      <severity>Critical</severity>
      <base_score>9.8</base_score>
      <affected_asset>User DB Server</affected_asset>
      <evidence>Port 3306 open without TLS</evidence>
    </vulnerability>
  </vulnerabilities>
</scan>
```

### JSON Format

```json
{
  "organization": {
    "name": "Sample Organization",
    "type": "Finance"
  },
  "vulnerabilities": [
    {
      "id": "VULN-001",
      "title": "Unencrypted Database",
      "severity": "Critical",
      "base_score": 9.8,
      "affected_asset": "User DB Server",
      "evidence": "Port 3306 open without TLS"
    }
  ]
}
```

## Output Format

```json
{
  "organization": {
    "name": "Sample Organization",
    "type": "Finance"
  },
  "findings": [
    {
      "vuln_id": "VULN-001",
      "title": "Unencrypted Database",
      "severity": "Critical",
      "base_score": 9.8,
      "affected_asset": "User DB Server",
      "evidence": "Port 3306 open without TLS",
      "source_file": "scan1.xml"
    }
  ]
}
```

## Module Functions

### Core Functions

| Function | Description |
|----------|-------------|
| `extract_zip(zip_path, extract_to)` | Extracts ZIP file to temporary directory |
| `parse_xml(file_path)` | Parses XML vulnerability scan file |
| `parse_json(file_path)` | Parses JSON vulnerability scan file |
| `filter_severity(findings)` | Filters for High and Critical findings only |
| `normalize_output(findings)` | Normalizes findings to unified JSON structure |
| `parse_vulnerability_scan(zip_path, output_path)` | Main pipeline function |

### Error Handling

The module includes custom `ParserError` exception for:
- Invalid or corrupted ZIP files
- Malformed XML/JSON files
- Missing required fields
- Unsupported file formats

## Testing

Sample test files are included:

- `sample_scan1.xml` - XML format with 5 vulnerabilities (mixed severity)
- `sample_scan2.json` - JSON format with 4 vulnerabilities (mixed severity)
- `sample_scan.zip` - ZIP archive containing both files

Run the test:

```bash
python parser.py
```

Expected output:
- Total findings: 9
- High/Critical findings: 6
- Output file: `normalized_output.json`

## Architecture

```
parser.py
│
├── extract_zip()           # ZIP extraction
├── parse_xml()             # XML parsing
├── parse_json()            # JSON parsing
├── filter_severity()       # Severity filtering
├── normalize_output()      # Data normalization
├── process_scan_files()    # File processing orchestration
└── parse_vulnerability_scan()  # Main pipeline
```

## Design Principles

1. **Separation of Concerns** - Each function has a single responsibility
2. **Defensive Programming** - Extensive error handling and validation
3. **Flexibility** - Supports multiple XML/JSON field name variations
4. **Offline First** - No external dependencies or network calls
5. **Clean Code** - Well-commented, readable, maintainable

## Limitations

- Only processes XML and JSON files (other formats are skipped)
- Only filters for "High" and "Critical" severity (case-insensitive)
- Organization info is taken from the first finding if multiple sources exist

## Future Enhancements (Not in Scope)

- ❌ AI-based risk scoring
- ❌ Automated report generation
- ❌ Cloud integration
- ❌ Database storage

## License

Enterprise internal use only.

## Support

For issues or questions, contact the Security Audit Pipeline Team.
