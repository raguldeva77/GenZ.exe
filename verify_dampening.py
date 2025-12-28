"""Quick verification of dampening logic"""
import json
from scoring.adaptive_risk import calculate_risk

with open("normalized_output.json") as f:
    data = json.load(f)

context = {
    "org_type": "Finance",
    "data_criticality": "High",
    "internet_exposed": True,
    "days_since_patch": 120
}

scored = calculate_risk(data["findings"], context)
scored = sorted(scored, key=lambda x: x["final_score"], reverse=True)

print("Vuln\t\t\t\tBase\tFinal\tPriority")
print("=" * 70)
for f in scored:
    title = f['title'][:30].ljust(30)
    print(f"{title}\t{f.get('base_score', 0)}\t{f['final_score']}\t{f['priority_rank']}")
