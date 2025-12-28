"""
Module 1: Data Ingestion & Parser
==================================
Enterprise-grade cybersecurity audit pipeline - Data ingestion component

This module handles:
- ZIP file extraction
- XML/JSON vulnerability scan parsing
- Severity filtering (High & Critical only)
- Data normalization to unified JSON structure

Author: Security Audit Pipeline Team
Version: 1.0.0
"""

import zipfile
import json
import xml.etree.ElementTree as ET
import os
import tempfile
from pathlib import Path
from typing import Dict, List, Any, Optional


class ParserError(Exception):
    """Custom exception for parser-related errors"""
    pass


def extract_zip(zip_path: str, extract_to: Optional[str] = None) -> str:
    """
    Extract ZIP file to a temporary or specified directory.
    
    Args:
        zip_path: Path to the ZIP file
        extract_to: Optional directory to extract to (uses temp dir if None)
    
    Returns:
        Path to the extraction directory
    
    Raises:
        ParserError: If ZIP file is invalid or extraction fails
    """
    try:
        if not os.path.exists(zip_path):
            raise ParserError(f"ZIP file not found: {zip_path}")
        
        if not zipfile.is_zipfile(zip_path):
            raise ParserError(f"Invalid ZIP file: {zip_path}")
        
        # Create extraction directory
        if extract_to is None:
            extract_to = tempfile.mkdtemp(prefix="vuln_scan_")
        else:
            os.makedirs(extract_to, exist_ok=True)
        
        # Extract ZIP contents
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        
        print(f"✓ Extracted ZIP to: {extract_to}")
        return extract_to
    
    except zipfile.BadZipFile as e:
        raise ParserError(f"Corrupted ZIP file: {e}")
    except Exception as e:
        raise ParserError(f"ZIP extraction failed: {e}")


def parse_xml(file_path: str) -> List[Dict[str, Any]]:
    """
    Parse XML vulnerability scan file and extract findings.
    
    Expected XML structure (flexible):
    <scan>
      <organization name="..." type="..." />
      <vulnerabilities>
        <vulnerability>
          <id>VULN-001</id>
          <title>...</title>
          <severity>Critical</severity>
          <base_score>9.8</base_score>
          <affected_asset>...</affected_asset>
          <evidence>...</evidence>
        </vulnerability>
      </vulnerabilities>
    </scan>
    
    Args:
        file_path: Path to XML file
    
    Returns:
        List of vulnerability dictionaries
    
    Raises:
        ParserError: If XML parsing fails
    """
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        findings = []
        
        # Extract organization info (if present)
        org_elem = root.find('.//organization')
        org_info = {}
        if org_elem is not None:
            org_info = {
                'name': org_elem.get('name', 'Unknown'),
                'type': org_elem.get('type', 'Unknown')
            }
        
        # Parse vulnerabilities
        # Support multiple common XML structures
        vuln_elements = (
            root.findall('.//vulnerability') or 
            root.findall('.//finding') or 
            root.findall('.//issue')
        )
        
        for vuln in vuln_elements:
            try:
                # Extract fields with fallbacks for different tag names
                vuln_id = (
                    vuln.findtext('id') or 
                    vuln.findtext('vuln_id') or 
                    vuln.findtext('identifier') or 
                    'UNKNOWN'
                )
                
                title = (
                    vuln.findtext('title') or 
                    vuln.findtext('name') or 
                    vuln.findtext('description') or 
                    'No title'
                )
                
                severity = (
                    vuln.findtext('severity') or 
                    vuln.findtext('risk') or 
                    'Unknown'
                )
                
                base_score_text = (
                    vuln.findtext('base_score') or 
                    vuln.findtext('cvss_score') or 
                    vuln.findtext('score') or 
                    '0.0'
                )
                
                affected_asset = (
                    vuln.findtext('affected_asset') or 
                    vuln.findtext('asset') or 
                    vuln.findtext('host') or 
                    'Unknown'
                )
                
                evidence = (
                    vuln.findtext('evidence') or 
                    vuln.findtext('details') or 
                    vuln.findtext('description') or 
                    'No evidence provided'
                )
                
                # Convert base_score to float
                try:
                    base_score = float(base_score_text)
                except ValueError:
                    base_score = 0.0
                
                finding = {
                    'vuln_id': vuln_id,
                    'title': title,
                    'severity': severity.strip(),
                    'base_score': base_score,
                    'affected_asset': affected_asset,
                    'evidence': evidence,
                    'source_file': os.path.basename(file_path),
                    'organization': org_info
                }
                
                findings.append(finding)
            
            except Exception as e:
                print(f"⚠ Warning: Skipped malformed vulnerability entry: {e}")
                continue
        
        print(f"✓ Parsed {len(findings)} findings from XML: {os.path.basename(file_path)}")
        return findings
    
    except ET.ParseError as e:
        raise ParserError(f"XML parsing error in {file_path}: {e}")
    except Exception as e:
        raise ParserError(f"Failed to parse XML file {file_path}: {e}")


def parse_json(file_path: str) -> List[Dict[str, Any]]:
    """
    Parse JSON vulnerability scan file and extract findings.
    
    Expected JSON structure (flexible):
    {
      "organization": {"name": "...", "type": "..."},
      "vulnerabilities": [
        {
          "id": "VULN-001",
          "title": "...",
          "severity": "Critical",
          "base_score": 9.8,
          "affected_asset": "...",
          "evidence": "..."
        }
      ]
    }
    
    Args:
        file_path: Path to JSON file
    
    Returns:
        List of vulnerability dictionaries
    
    Raises:
        ParserError: If JSON parsing fails
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        findings = []
        
        # Extract organization info
        org_info = data.get('organization', {})
        if not org_info:
            org_info = {
                'name': data.get('org_name', 'Unknown'),
                'type': data.get('org_type', 'Unknown')
            }
        
        # Parse vulnerabilities - support multiple field names
        vulnerabilities = (
            data.get('vulnerabilities') or 
            data.get('findings') or 
            data.get('issues') or 
            data.get('results') or 
            []
        )
        
        # Handle case where data itself is a list
        if isinstance(data, list):
            vulnerabilities = data
        
        for vuln in vulnerabilities:
            try:
                # Extract fields with fallbacks
                vuln_id = (
                    vuln.get('id') or 
                    vuln.get('vuln_id') or 
                    vuln.get('identifier') or 
                    'UNKNOWN'
                )
                
                title = (
                    vuln.get('title') or 
                    vuln.get('name') or 
                    vuln.get('description') or 
                    'No title'
                )
                
                severity = (
                    vuln.get('severity') or 
                    vuln.get('risk') or 
                    'Unknown'
                )
                
                base_score = float(
                    vuln.get('base_score') or 
                    vuln.get('cvss_score') or 
                    vuln.get('score') or 
                    0.0
                )
                
                affected_asset = (
                    vuln.get('affected_asset') or 
                    vuln.get('asset') or 
                    vuln.get('host') or 
                    vuln.get('target') or 
                    'Unknown'
                )
                
                evidence = (
                    vuln.get('evidence') or 
                    vuln.get('details') or 
                    vuln.get('description') or 
                    'No evidence provided'
                )
                
                finding = {
                    'vuln_id': str(vuln_id),
                    'title': title,
                    'severity': str(severity).strip(),
                    'base_score': base_score,
                    'affected_asset': affected_asset,
                    'evidence': evidence,
                    'source_file': os.path.basename(file_path),
                    'organization': org_info
                }
                
                findings.append(finding)
            
            except Exception as e:
                print(f"⚠ Warning: Skipped malformed vulnerability entry: {e}")
                continue
        
        print(f"✓ Parsed {len(findings)} findings from JSON: {os.path.basename(file_path)}")
        return findings
    
    except json.JSONDecodeError as e:
        raise ParserError(f"JSON parsing error in {file_path}: {e}")
    except Exception as e:
        raise ParserError(f"Failed to parse JSON file {file_path}: {e}")


def filter_severity(findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Filter findings to include only High and Critical severity.
    
    Args:
        findings: List of vulnerability dictionaries
    
    Returns:
        Filtered list containing only High and Critical findings
    """
    high_critical = ['high', 'critical']
    
    filtered = [
        f for f in findings 
        if f.get('severity', '').lower() in high_critical
    ]
    
    print(f"✓ Filtered {len(filtered)} High/Critical findings from {len(findings)} total")
    return filtered


def normalize_output(all_findings: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Normalize findings into unified JSON structure.
    
    Args:
        all_findings: List of all vulnerability dictionaries
    
    Returns:
        Normalized output dictionary with organization info and findings
    """
    if not all_findings:
        return {
            'organization': {
                'name': 'Unknown',
                'type': 'Unknown'
            },
            'findings': []
        }
    
    # Extract organization info from first finding (or aggregate if different)
    org_info = all_findings[0].get('organization', {})
    
    # Clean up findings - remove organization field from individual findings
    normalized_findings = []
    for finding in all_findings:
        clean_finding = {
            'vuln_id': finding.get('vuln_id'),
            'title': finding.get('title'),
            'severity': finding.get('severity'),
            'base_score': finding.get('base_score'),
            'affected_asset': finding.get('affected_asset'),
            'evidence': finding.get('evidence'),
            'source_file': finding.get('source_file')
        }
        normalized_findings.append(clean_finding)
    
    output = {
        'organization': {
            'name': org_info.get('name', 'Unknown'),
            'type': org_info.get('type', 'Unknown')
        },
        'findings': normalized_findings
    }
    
    print(f"✓ Normalized {len(normalized_findings)} findings")
    return output


def process_scan_files(extract_dir: str) -> List[Dict[str, Any]]:
    """
    Process all XML and JSON files in the extracted directory.
    
    Args:
        extract_dir: Directory containing extracted scan files
    
    Returns:
        List of all parsed findings
    """
    all_findings = []
    
    # Walk through all files in extraction directory
    for root, dirs, files in os.walk(extract_dir):
        for file in files:
            file_path = os.path.join(root, file)
            file_ext = os.path.splitext(file)[1].lower()
            
            try:
                if file_ext == '.xml':
                    findings = parse_xml(file_path)
                    all_findings.extend(findings)
                
                elif file_ext == '.json':
                    findings = parse_json(file_path)
                    all_findings.extend(findings)
                
                else:
                    print(f"⚠ Skipping unsupported file format: {file}")
            
            except ParserError as e:
                print(f"✗ Error processing {file}: {e}")
                continue
    
    return all_findings


def parse_vulnerability_scan(zip_path: str, output_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Main pipeline function: Extract, parse, filter, and normalize vulnerability scan data.
    
    Args:
        zip_path: Path to ZIP file containing scan data
        output_path: Optional path to save normalized JSON output
    
    Returns:
        Normalized vulnerability data dictionary
    
    Raises:
        ParserError: If any step in the pipeline fails
    """
    print(f"\n{'='*60}")
    print("MODULE 1: DATA INGESTION & PARSER")
    print(f"{'='*60}\n")
    
    try:
        # Step 1: Extract ZIP
        print("Step 1: Extracting ZIP file...")
        extract_dir = extract_zip(zip_path)
        
        # Step 2: Process all scan files
        print("\nStep 2: Processing scan files...")
        all_findings = process_scan_files(extract_dir)
        
        if not all_findings:
            print("⚠ Warning: No findings extracted from scan files")
        
        # Step 3: Filter by severity
        print("\nStep 3: Filtering by severity (High & Critical only)...")
        filtered_findings = filter_severity(all_findings)
        
        # Step 4: Normalize output
        print("\nStep 4: Normalizing output structure...")
        normalized_data = normalize_output(filtered_findings)
        
        # Step 5: Save output (optional)
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(normalized_data, f, indent=2)
            print(f"\n✓ Output saved to: {output_path}")
        
        print(f"\n{'='*60}")
        print(f"✓ PARSING COMPLETE")
        print(f"  Total findings: {len(all_findings)}")
        print(f"  High/Critical: {len(filtered_findings)}")
        print(f"{'='*60}\n")
        
        return normalized_data
    
    except Exception as e:
        raise ParserError(f"Pipeline failed: {e}")


def main():
    """
    Test function demonstrating parser usage.
    """
    print("Module 1: Data Ingestion & Parser - Test Mode\n")
    
    # Example usage
    zip_file = "sample_scan.zip"  # Replace with actual ZIP file path
    output_file = "normalized_output.json"
    
    try:
        # Check if sample file exists
        if not os.path.exists(zip_file):
            print(f"⚠ Sample ZIP file not found: {zip_file}")
            print("\nTo test this module:")
            print("1. Create a ZIP file containing XML/JSON vulnerability scan files")
            print("2. Update the 'zip_file' variable in main() with the correct path")
            print("3. Run the script again")
            print("\nExample XML structure:")
            print("""
<scan>
  <organization name="Sample Org" type="Finance" />
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
            """)
            return
        
        # Parse the vulnerability scan
        result = parse_vulnerability_scan(zip_file, output_file)
        
        # Display summary
        print("\nParsed Data Summary:")
        print(json.dumps(result, indent=2))
    
    except ParserError as e:
        print(f"\n✗ Parser Error: {e}")
    except Exception as e:
        print(f"\n✗ Unexpected Error: {e}")


if __name__ == "__main__":
    main()
