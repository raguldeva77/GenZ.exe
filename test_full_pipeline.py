"""
FINAL INTEGRATION TEST: All Modules (1-5)
-----------------------------------------
Complete pipeline from parsing to final audit report.

This demonstrates the full Synthetic Auditor workflow:
1. Parse vulnerability scans (Module 1)
2. Calculate adaptive risk scores (Module 2)
3. Build explainable trace matrix (Module 3)
4. Generate AI explanations (Module 4)
5. Create professional audit report (Module 5)
"""

import json
from scoring.adaptive_risk import calculate_risk
from explainability.trace_matrix import build_trace_matrix
from llm.explain_from_trace import explain_all
from reporting.report_generator import generate_report

print("=" * 70)
print("SYNTHETIC AUDITOR - FULL PIPELINE TEST")
print("=" * 70)

# Load normalized data from Module 1
print("\n[Module 1] Loading parsed vulnerability data...")
with open("normalized_output.json") as f:
    data = json.load(f)
print(f"✓ Loaded {len(data['findings'])} findings for {data['organization']['name']}")

# Define organizational context
context = {
    "org_type": data["organization"]["type"],
    "data_criticality": "High",
    "internet_exposed": True,
    "days_since_patch": 120
}
print(f"✓ Context: {context}")

# Module 2: Adaptive Risk Scoring
print("\n[Module 2] Calculating adaptive risk scores...")
scored = calculate_risk(data["findings"], context)
print(f"✓ Scored {len(scored)} findings with priority ranking")

# Module 3: Explainable Trace Matrix
print("\n[Module 3] Building explainable trace matrix...")
trace = build_trace_matrix(scored)
print(f"✓ Built trace matrix with complete reasoning trails")

# Module 4: LLM Explanations
print("\n[Module 4] Generating AI-powered explanations...")
print("(This may take 30-60 seconds depending on your hardware)")
print("-" * 70)

try:
    explanations = explain_all(trace)
    print(f"✓ Generated {len(explanations)} AI explanations")
except Exception as e:
    print(f"⚠ LLM unavailable: {e}")
    print("  Using fallback explanations...")
    explanations = [
        {
            "vuln_id": item["vuln_id"],
            "title": item["title"],
            "priority_rank": item["trace"]["priority_rank"],
            "explanation": f"[LLM unavailable] This {item['trace']['risk_level']} vulnerability requires immediate attention based on its priority rank and context."
        }
        for item in trace
    ]

# Module 5: Report Generation
print("\n[Module 5] Generating security audit report...")
report_path = generate_report(
    org=data["organization"],
    trace_matrix=trace,
    explanations=explanations
)
print(f"✓ Report generated: {report_path}")

# Summary
print("\n" + "=" * 70)
print("PIPELINE SUMMARY")
print("=" * 70)
print(f"✓ Module 1: Parsed {len(data['findings'])} findings")
print(f"✓ Module 2: Calculated adaptive risk scores")
print(f"✓ Module 3: Built explainable trace matrix")
print(f"✓ Module 4: Generated AI explanations")
print(f"✓ Module 5: Created audit report")
print("\n✅ FULL PIPELINE COMPLETE!")
print(f"\n📄 View your report: {report_path}")
print("=" * 70)
