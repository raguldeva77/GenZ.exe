"""
Integration Test: Module 1 + Module 2
--------------------------------------
Tests the adaptive risk scoring with normalized output from Module 1.
"""

import json
from scoring.adaptive_risk import calculate_risk

# Load normalized output from Module 1
with open("normalized_output.json") as f:
    data = json.load(f)

# Define context for risk scoring
context = {
    "org_type": data["organization"]["type"],
    "data_criticality": "High",
    "internet_exposed": True,
    "days_since_patch": 120
}

# Calculate risk scores
scored = calculate_risk(data["findings"], context)

# Sort by final score (highest risk first - consulting style)
scored = sorted(scored, key=lambda x: x["final_score"], reverse=True)

# Display results
print("=" * 60)
print("ADAPTIVE RISK SCORING RESULTS")
print("=" * 60)
print(f"\nOrganization: {data['organization']['name']} ({data['organization']['type']})")
print(f"Context: {context}")
print(f"\nTotal Findings: {len(scored)}")
print("=" * 60)

for finding in scored:
    print(f"\n[Priority {finding['priority_rank']}] [{finding['risk_level']}] {finding['title']}")
    print(f"  Vuln ID: {finding['vuln_id']}")
    print(f"  Base Score: {finding.get('base_score', 'N/A')}")
    print(f"  Final Score: {finding['final_score']}")
    print(f"  Modifiers: {finding['modifiers']}")
    print(f"  Severity: {finding.get('severity', 'Unknown')}")

print("\n" + "=" * 60)
print("SUMMARY BY RISK LEVEL")
print("=" * 60)

# Count by risk level
risk_counts = {}
for finding in scored:
    level = finding['risk_level']
    risk_counts[level] = risk_counts.get(level, 0) + 1

for level in ["Critical", "High", "Medium", "Low"]:
    count = risk_counts.get(level, 0)
    print(f"{level}: {count}")

print("=" * 60)
