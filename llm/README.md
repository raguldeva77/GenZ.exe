# Module 4: Local LLM Analyst Co-Pilot

## Overview
AI-powered explanation generator that converts technical trace matrix data into human-readable vulnerability assessments using a local LLM (Ollama).

## Critical Design Principle

**The LLM is a NARRATOR, not a DECISION MAKER.**

### What Module 4 Does ✅
- Explains why a vulnerability has a certain priority
- Converts trace matrix data into human language
- Helps auditors and stakeholders understand technical findings

### What Module 4 Does NOT Do ❌
- Calculate risk scores (Module 2's job)
- Change priorities (Module 2's job)
- Make security decisions (Modules 1-3's job)
- Invent new findings (hallucination prevention)

## Architecture

```
llm/
├── local_llm.py           # Ollama subprocess wrapper
└── explain_from_trace.py  # Trace → Explanation converter
```

## Requirements

### Software
- **Ollama** installed and running
- **Model**: llama3.1:8b (or compatible)

### Installation
```bash
# Install Ollama
# Visit: https://ollama.ai

# Pull model
ollama pull llama3.1:8b

# Verify
ollama run llama3.1:8b
```

## Usage

### Standalone Test
```bash
# Test Ollama connection
python llm/local_llm.py

# Test explanation generation
python llm/explain_from_trace.py
```

### Full Pipeline (Modules 1-4)
```bash
python test_full_pipeline.py
```

## Hallucination Prevention

### Prompt Engineering
The prompts are carefully designed to:
1. **Constrain scope**: "DO NOT change scores or priorities"
2. **Require evidence**: "Use only the provided evidence"
3. **Prevent invention**: "DO NOT invent new findings"
4. **Focus on explanation**: "ONLY explain why..."

### Example Prompt Structure
```
You are a cybersecurity auditor assisting a security team.

Explain the vulnerability below in clear, professional language.
DO NOT change scores or priorities.
DO NOT invent new findings.
ONLY explain why this vulnerability is high priority based on the evidence provided.

[Structured data from trace matrix]

Explain in 3-4 sentences:
1. Why this vulnerability is risky for this organization
2. Why the priority rank reflects urgency
3. What makes this particularly concerning given the context
```

## Error Handling

### Graceful Degradation
If Ollama fails:
- Error is caught and logged
- Explanation shows: `[LLM Error: ...] Manual review required.`
- Pipeline continues without crashing

### Offline Guarantee
- All LLM calls are local (subprocess to Ollama)
- No internet required
- No external API calls
- Complete data sovereignty maintained

## Input Format

From Module 3 (trace matrix):
```json
{
  "vuln_id": "VULN-001",
  "title": "Unencrypted Database Connection",
  "trace": {
    "base_score": 9.8,
    "final_score": 10.0,
    "risk_level": "Critical",
    "priority_rank": 2,
    "modifiers_applied": {...}
  },
  "evidence": "Port 3306 open without TLS...",
  "affected_asset": "User DB Server"
}
```

## Output Format

```json
{
  "vuln_id": "VULN-001",
  "title": "Unencrypted Database Connection",
  "priority_rank": 2,
  "explanation": "This vulnerability is critical for a financial organization because unencrypted database connections expose sensitive customer data to interception. The Priority 2 ranking reflects the combination of a high base severity (9.8) and organizational context factors including financial sector requirements, high data criticality, and internet exposure. The 120-day patch delay further elevates urgency, making this a top remediation priority after only the most severe code execution vulnerabilities."
}
```

## Judge-Ready Statement

> "Our local LLM analyst co-pilot generates human-readable explanations from structured trace data, maintaining complete offline operation while preventing hallucinations through constrained prompting. The AI explains decisions made by deterministic logic, never making security decisions itself."

## Testing Without Ollama

The module is designed to fail gracefully:
- Modules 1-3 work independently
- Module 4 can be skipped if Ollama unavailable
- Error messages guide setup

## Performance

- **Per-finding**: ~2-5 seconds (depends on hardware)
- **6 findings**: ~30-60 seconds total
- **Model size**: 4.7GB (llama3.1:8b)

## Future Enhancements

- Multi-language explanations
- Executive vs technical tone selection
- Batch processing optimization
- Model fine-tuning on security terminology
