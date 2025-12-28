"""
Module 3: Explainable Risk Trace Matrix
--------------------------------------
Builds a transparent reasoning trail for each vulnerability.
"""

def build_trace_matrix(scored_findings):
    trace_results = []

    for finding in scored_findings:
        trace = {
            "vuln_id": finding.get("vuln_id"),
            "title": finding.get("title"),
            "trace": {
                "base_score": finding.get("base_score"),
                "modifiers_applied": finding.get("modifiers", {}),
                "final_score": finding.get("final_score"),
                "risk_level": finding.get("risk_level"),
                "priority_rank": finding.get("priority_rank")
            },
            "evidence": finding.get("evidence"),
            "affected_asset": finding.get("affected_asset"),
            "source_file": finding.get("source_file")
        }

        trace_results.append(trace)

    return trace_results


# Simple standalone test
if __name__ == "__main__":
    sample = [
        {
            "vuln_id": "VULN-001",
            "title": "Unencrypted Database",
            "base_score": 9.8,
            "final_score": 10.0,
            "risk_level": "Critical",
            "priority_rank": 1,
            "modifiers": {
                "org_type": "+1.0",
                "data_criticality": "+0.8",
                "internet_exposed": "+0.5",
                "patch_delay": "+0.3"
            },
            "evidence": "Port 3306 open without TLS",
            "affected_asset": "User DB Server",
            "source_file": "scan1.xml"
        }
    ]

    trace = build_trace_matrix(sample)
    from pprint import pprint
    pprint(trace)
