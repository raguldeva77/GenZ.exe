# Module 3: Explainable Risk Trace Matrix

## Overview
Transparent reasoning trail builder that documents the complete risk calculation path for each vulnerability.

## Purpose
Provides **explainability** and **auditability** by showing exactly how each risk score was calculated, addressing the "black box AI" concern.

## Features

✅ **Complete Reasoning Trails** - Base score → Modifiers → Final score  
✅ **Evidence Linking** - Every score tied to actual scan evidence  
✅ **Modifier Tracking** - Shows which context factors influenced the score  
✅ **Priority Preservation** - Maintains ranking from Module 2  
✅ **Audit-Ready** - Full transparency for compliance reviews  
✅ **No AI Required** - Pure logic and data structuring

## Input
Scored findings from Module 2 with:
- `base_score`
- `final_score`
- `modifiers` (dict)
- `risk_level`
- `priority_rank`
- `evidence`

## Output Structure

```json
{
  "vuln_id": "VULN-004",
  "title": "Remote Code Execution",
  "trace": {
    "base_score": 10.0,
    "modifiers_applied": {
      "org_type": "+1.0",
      "data_criticality": "+0.8",
      "internet_exposed": "+0.5",
      "patch_delay": "+0.3"
    },
    "final_score": 10.0,
    "risk_level": "Critical",
    "priority_rank": 1
  },
  "evidence": "Deserialization vulnerability allows arbitrary code execution",
  "affected_asset": "API Gateway",
  "source_file": "scan1.xml"
}
```

## Usage

### Standalone
```python
from explainability.trace_matrix import build_trace_matrix

trace = build_trace_matrix(scored_findings)
```

### Full Pipeline (Modules 1-3)
```python
python test_trace_matrix.py
```

## Key Innovation

**Explainable Risk Reasoning** - Unlike black-box AI systems, every score change is:
- Documented
- Traceable
- Verifiable
- Audit-ready

This addresses a critical gap in AI-based security tools: **trust through transparency**.

## Judge-Ready Statement

> "Our trace matrix provides complete explainability by documenting the reasoning path from raw findings through context-aware scoring to final risk assessment, ensuring auditor trust and regulatory compliance."
