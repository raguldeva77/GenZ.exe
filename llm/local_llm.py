"""
Module 4: Local LLM Interface (Ollama Wrapper)
---------------------------------------------
Base wrapper for running local LLM queries via Ollama.
"""

import subprocess


def run_llm(prompt, model="llama3.1:8b"):
    """
    Run a prompt through local Ollama LLM.
    
    Args:
        prompt (str): The prompt to send to the LLM
        model (str): Ollama model name (default: llama3.1:8b)
    
    Returns:
        str: LLM response text
    
    Raises:
        RuntimeError: If Ollama execution fails
    """
    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",      # Force UTF-8 encoding
        errors="ignore"        # Ignore encoding errors
    )

    if result.returncode != 0:
        raise RuntimeError(f"Ollama error: {result.stderr}")

    return result.stdout.strip()


# Simple test
if __name__ == "__main__":
    print("Testing Ollama connection...")
    try:
        response = run_llm("Explain SQL Injection in simple terms.")
        print("✓ Ollama is working!")
        print("Response:", response)
    except RuntimeError as e:
        print(f"✗ Ollama error: {e}")
        print("\nMake sure Ollama is installed and running:")
        print("  1. Install: https://ollama.ai")
        print("  2. Run: ollama pull llama3.1:8b")
