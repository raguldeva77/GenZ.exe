"""
Module 2: Adaptive Risk Scoring Engine
-------------------------------------
Calculates context-aware risk scores for vulnerabilities.
No AI, no external libraries.
"""

def calculate_risk(findings, context):
    scored_findings = []

    for finding in findings:
        base_score = float(finding.get("base_score", 0))
        final_score = base_score
        modifiers = {}

        # Organization type modifier
        org_type = context.get("org_type", "").lower()
        if org_type in ["finance", "healthcare"]:
            final_score += 1.0
            modifiers["org_type"] = "+1.0"
        elif org_type == "education":
            final_score += 0.5
            modifiers["org_type"] = "+0.5"

        # Data criticality modifier
        data_crit = context.get("data_criticality", "").lower()
        if data_crit == "high":
            final_score += 0.8
            modifiers["data_criticality"] = "+0.8"
        elif data_crit == "medium":
            final_score += 0.4
            modifiers["data_criticality"] = "+0.4"

        # Internet exposure
        if context.get("internet_exposed", False):
            final_score += 0.5
            modifiers["internet_exposed"] = "+0.5"

        # Patch age
        if context.get("days_since_patch", 0) > 90:
            final_score += 0.3
            modifiers["patch_delay"] = "+0.3"

        # Dampening to preserve prioritization
        # Prevents lower base scores from hitting the cap too easily
        if base_score < 8 and final_score >= 9:
            final_score -= 0.5

        # Cap score at 10
        final_score = min(final_score, 10.0)

        # Risk level
        if final_score >= 8:
            risk_level = "Critical"
        elif final_score >= 6:
            risk_level = "High"
        elif final_score >= 3:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        scored_findings.append({
            **finding,
            "final_score": round(final_score, 2),
            "risk_level": risk_level,
            "modifiers": modifiers
        })

    # Priority ranking (lower number = higher priority)
    # Sort by final score descending, then assign ranks
    sorted_findings = sorted(
        scored_findings,
        key=lambda x: x["final_score"],
        reverse=True
    )

    for idx, finding in enumerate(sorted_findings, start=1):
        finding["priority_rank"] = idx

    return sorted_findings


# Simple test
if __name__ == "__main__":
    sample_findings = [
        {
            "vuln_id": "VULN-001",
            "title": "Unencrypted DB",
            "base_score": 7.5
        }
    ]

    context = {
        "org_type": "Finance",
        "data_criticality": "High",
        "internet_exposed": True,
        "days_since_patch": 120
    }

    result = calculate_risk(sample_findings, context)
    print(result)
