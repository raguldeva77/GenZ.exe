"""
Module 4: Analyst Co-Pilot (Local LLM)
-------------------------------------
Generates human-readable explanations from explainable risk traces.

IMPORTANT: This module does NOT:
- Calculate risk scores
- Change priorities
- Make decisions

It ONLY explains existing decisions made by Modules 1-3.
"""

import json
import sys
import os

# Add parent directory to path for standalone execution
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm.local_llm import run_llm


def build_prompt(trace_item):
    """
    Build a structured prompt for the LLM to explain a vulnerability.
    
    The prompt constrains the LLM to:
    - Only explain, not decide
    - Use provided evidence only
    - Not invent new findings
    """
    modifiers_str = json.dumps(trace_item['trace']['modifiers_applied'], indent=2)
    
    return f"""You are a cybersecurity auditor assisting a security team.

Explain the vulnerability below in clear, professional language.
DO NOT change scores or priorities.
DO NOT invent new findings.
ONLY explain why this vulnerability is high priority based on the evidence provided.

Vulnerability ID: {trace_item['vuln_id']}
Title: {trace_item['title']}
Affected Asset: {trace_item['affected_asset']}

Base Score: {trace_item['trace']['base_score']}
Final Score: {trace_item['trace']['final_score']}
Risk Level: {trace_item['trace']['risk_level']}
Priority Rank: {trace_item['trace']['priority_rank']}

Context Modifiers Applied:
{modifiers_str}

Evidence:
{trace_item['evidence']}

Explain in 3-4 sentences:
1. Why this vulnerability is risky for this organization
2. Why the priority rank reflects urgency
3. What makes this particularly concerning given the context
"""


def explain_trace_item(trace_item):
    """
    Generate human-readable explanation for a single trace item.
    
    Args:
        trace_item (dict): Trace matrix item from Module 3
    
    Returns:
        str: LLM-generated explanation
    """
    prompt = build_prompt(trace_item)
    return run_llm(prompt)


def explain_all(trace_matrix):
    """
    Generate explanations for all items in trace matrix.
    
    Args:
        trace_matrix (list): List of trace items from Module 3
    
    Returns:
        list: List of dicts with vuln_id, priority_rank, and explanation
    """
    results = []

    for item in trace_matrix:
        try:
            explanation = explain_trace_item(item)
            results.append({
                "vuln_id": item["vuln_id"],
                "title": item["title"],
                "priority_rank": item["trace"]["priority_rank"],
                "explanation": explanation
            })
        except Exception as e:
            # Graceful degradation if LLM fails
            results.append({
                "vuln_id": item["vuln_id"],
                "title": item["title"],
                "priority_rank": item["trace"]["priority_rank"],
                "explanation": f"[LLM Error: {str(e)}] Manual review required."
            })

    return results


# Simple standalone test
if __name__ == "__main__":
    # Sample trace item for testing
    sample_trace = {
        "vuln_id": "VULN-001",
        "title": "Unencrypted Database Connection",
        "affected_asset": "User DB Server",
        "trace": {
            "base_score": 9.8,
            "final_score": 10.0,
            "risk_level": "Critical",
            "priority_rank": 2,
            "modifiers_applied": {
                "org_type": "+1.0",
                "data_criticality": "+0.8",
                "internet_exposed": "+0.5",
                "patch_delay": "+0.3"
            }
        },
        "evidence": "Port 3306 open without TLS encryption. Database credentials transmitted in plaintext.",
        "source_file": "scan1.xml"
    }

    print("=" * 70)
    print("Testing LLM Explanation Generation")
    print("=" * 70)
    
    try:
        explanation = explain_trace_item(sample_trace)
        print(f"\n[Priority {sample_trace['trace']['priority_rank']}] {sample_trace['title']}")
        print(f"\n{explanation}")
        print("\n" + "=" * 70)
        print("✓ LLM explanation generated successfully")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nMake sure Ollama is installed and running:")
        print("  1. Install: https://ollama.ai")
        print("  2. Run: ollama pull llama3.1:8b")
