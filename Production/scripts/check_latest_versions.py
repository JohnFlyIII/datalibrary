#!/usr/bin/env python3
"""
Check latest available versions of key packages
Run this to see what versions are current as of your date
"""

import subprocess
import json
from datetime import datetime

def get_latest_version(package):
    """Get latest version of a package from PyPI"""
    try:
        result = subprocess.run(
            ["pip", "index", "versions", package],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if "Available versions:" in line:
                    versions = line.split(": ")[1].split(", ")
                    return versions[0]  # First one is usually latest stable
        return "Check failed"
    except:
        return "Error checking"

print(f"Checking latest package versions as of {datetime.now().strftime('%Y-%m-%d')}")
print("=" * 60)

# Key packages to check
packages = {
    "anthropic": "Claude API client",
    "sentence-transformers": "For embeddings", 
    "transformers": "Hugging Face transformers",
    "huggingface-hub": "HF Hub client",
    "numpy": "Numerical computing",
    "pandas": "Data manipulation",
    "scikit-learn": "Machine learning",
    "pdfplumber": "PDF processing",
    "pypdf2": "PDF processing",
    "torch": "PyTorch (if needed)",
    "python-dotenv": "Environment management",
    "click": "CLI framework",
    "nltk": "Natural language toolkit",
    "tiktoken": "OpenAI tokenizer"
}

print(f"{'Package':<25} {'Latest Version':<15} {'Description':<30}")
print("-" * 70)

for package, description in packages.items():
    version = get_latest_version(package)
    print(f"{package:<25} {version:<15} {description:<30}")

print("\nNote: Always test compatibility when using latest versions!")
print("Some packages may have breaking changes between major versions.")