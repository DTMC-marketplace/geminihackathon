#!/usr/bin/env python3
"""
Deployer Training Materials Generator

Scans a codebase and generates comprehensive training documentation
for deployers and developers using Gemini AI.

EU AI Act Articles 13 & 14 Compliance Tool.
"""

import argparse
import os
import sys
import re
from pathlib import Path
from typing import List, Set

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Error: google-genai package not found.")
    print("Install with: pip install google-genai")
    sys.exit(1)

# Configuration
PRIMARY_MODEL = "gemini-3-pro-preview"
FALLBACK_MODEL = "gemini-2.0-flash-exp"

# File extensions to ingest (all common programming languages and text files)
TEXT_EXTENSIONS = {
    # Programming Languages
    ".py", ".js", ".ts", ".jsx", ".tsx", ".go", ".rs", ".java", ".kt", ".scala",
    ".c", ".cpp", ".h", ".hpp", ".cs", ".swift", ".rb", ".php", ".pl", ".lua",
    ".sh", ".bash", ".zsh", ".ps1", ".bat", ".cmd",
    # Web & Config
    ".html", ".htm", ".css", ".scss", ".sass", ".less",
    ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf",
    ".xml", ".xsl", ".xslt",
    # Documentation
    ".md", ".markdown", ".rst", ".txt", ".adoc",
    # Data & Query
    ".sql", ".graphql", ".gql",
    # Other
    ".dockerfile", ".makefile", ".cmake",
}

# Files to always exclude (security)
EXCLUDED_FILES = {".env", ".env.local", ".env.production", ".env.development"}
EXCLUDED_PATTERNS = {"*.key", "*.pem", "*.secret", "*_key.txt"}


def load_env_file():
    """Manually load .env file from current or parent directories."""
    current_dir = Path(__file__).resolve().parent
    for _ in range(6):
        env_path = current_dir / ".env"
        if env_path.exists():
            try:
                content = env_path.read_text(encoding="utf-8")
                for line in content.splitlines():
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    match = re.match(r'^GEMINI_API_KEY\s*=\s*(?:["\'])(.*?)(?:["\'])$|^GEMINI_API_KEY\s*=\s*(.*?)$', line)
                    if match:
                        key = match.group(1) or match.group(2)
                        os.environ["GEMINI_API_KEY"] = key
                        return
            except Exception:
                pass
        if current_dir.parent == current_dir:
            break
        current_dir = current_dir.parent


def get_api_key() -> str:
    """Get GEMINI_API_KEY from environment or .env file."""
    if not os.environ.get("GEMINI_API_KEY"):
        load_env_file()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        sys.exit(1)
    return api_key


def load_gitignore_patterns(repo_root: Path) -> Set[str]:
    """Load patterns from .gitignore file."""
    patterns = set()
    gitignore_path = repo_root / ".gitignore"
    if gitignore_path.exists():
        try:
            for line in gitignore_path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    patterns.add(line)
        except Exception:
            pass
    return patterns


def is_ignored(path: Path, repo_root: Path, gitignore_patterns: Set[str]) -> bool:
    """Check if a path should be ignored based on .gitignore and security rules."""
    relative_path = path.relative_to(repo_root)
    path_str = str(relative_path).replace("\\", "/")
    
    # Always exclude security-sensitive files
    if path.name in EXCLUDED_FILES:
        return True
    
    # Check gitignore patterns (simplified matching)
    for pattern in gitignore_patterns:
        pattern_clean = pattern.strip("/")
        if pattern_clean in path_str or path.name == pattern_clean:
            return True
        if pattern_clean.endswith("/") and path_str.startswith(pattern_clean):
            return True
    
    return False


def scan_codebase(repo_root: Path) -> List[dict]:
    """Scan the codebase and collect file contents."""
    files_data = []
    gitignore_patterns = load_gitignore_patterns(repo_root)
    
    # Add common ignored directories
    gitignore_patterns.update({"node_modules", ".git", "__pycache__", ".venv", "venv", "dist", "build"})
    
    for root, dirs, files in os.walk(repo_root):
        root_path = Path(root)
        
        # Filter out ignored directories
        dirs[:] = [d for d in dirs if not is_ignored(root_path / d, repo_root, gitignore_patterns)]
        
        for file_name in files:
            file_path = root_path / file_name
            
            if is_ignored(file_path, repo_root, gitignore_patterns):
                continue
            
            # Check if file extension is in our list
            if file_path.suffix.lower() not in TEXT_EXTENSIONS and file_path.name.lower() not in {"dockerfile", "makefile"}:
                continue
            
            try:
                content = file_path.read_text(encoding="utf-8")
                relative_path = file_path.relative_to(repo_root)
                files_data.append({
                    "path": str(relative_path).replace("\\", "/"),
                    "content": content
                })
            except Exception:
                pass  # Skip files we can't read
    
    return files_data


def build_context(files_data: List[dict]) -> str:
    """Build the context string from scanned files."""
    context_parts = []
    for file_info in files_data:
        context_parts.append(f"--- FILE: {file_info['path']} ---\n{file_info['content']}\n")
    return "\n".join(context_parts)


def build_system_prompt() -> str:
    """Build the system prompt for the instructor persona."""
    return """You are a Senior Developer Instructor with 20 years of experience.
Your task is to analyze a codebase and generate comprehensive, production-quality training documentation.

Your documentation MUST follow this exact structure:

# [Product Name] - Deployer & Developer Guide

## 1. Executive Summary
A high-level overview of what this product does. 2-3 paragraphs written for a CTO or project manager.

## 2. System Architecture

### 2.1 Component Diagram
Create a Mermaid diagram showing the main components and their relationships.

### 2.2 Data Flow
Explain how data moves through the system.

### 2.3 Tech Stack
List all technologies, frameworks, and dependencies used.

## 3. Product Capabilities

### 3.1 Core Features
For EACH major feature in the codebase:
- Feature Name
- What it does
- How it works (brief technical summary)
- Key configuration options

### 3.2 User Journeys
Write step-by-step walkthroughs for common tasks:
- Journey for "The Deployer" (setting up and running the system)
- Journey for "The End User" (using the product)

### 3.3 Configuration Options
Create a comprehensive table of all environment variables, flags, and settings.

## 4. Developer Onboarding

### 4.1 Environment Setup
Step-by-step instructions to get a development environment running.

### 4.2 Extension Patterns
Explain how to add new features, modules, or plugins to this codebase.

### 4.3 Testing Guidelines
How to run tests, write new tests, and the testing philosophy.

## 5. Operational Guide

### 5.1 Deployment Strategy
How to deploy this product to production.

### 5.2 Troubleshooting & Limitations
Common issues, known bugs, rate limits, and workarounds.

---

IMPORTANT:
- Be detailed and specific. Reference actual file paths and code snippets.
- Use Mermaid diagrams where helpful.
- Write in a teaching tone, not a dry technical manual.
- If information is missing from the codebase, note it as "Not Found in Codebase".
"""


def generate_documentation(context: str, model_name: str = None) -> str:
    """Call Gemini API to generate the documentation."""
    api_key = get_api_key()
    client = genai.Client(api_key=api_key)
    
    system_prompt = build_system_prompt()
    user_prompt = f"""Analyze the following codebase and generate the Deployer & Developer Guide.

CODEBASE CONTENTS:
{context}

Generate the complete documentation now."""

    generate_config = types.GenerateContentConfig(
        temperature=0.4,
        system_instruction=system_prompt
    )
    
    models_to_try = [model_name] if model_name else [PRIMARY_MODEL, FALLBACK_MODEL]
    last_exception = None
    
    for model in models_to_try:
        print(f"🤖 Attempting generation with model: {model}...")
        try:
            response = client.models.generate_content(
                model=model,
                contents=user_prompt,
                config=generate_config
            )
            if response.text:
                return response.text.strip()
            print(f"⚠️  Model {model} returned no text.")
        except Exception as e:
            print(f"❌ Model {model} failed: {e}")
            last_exception = e
    
    print("Error: Documentation generation failed with all attempted models.")
    if last_exception:
        print(f"Last error: {last_exception}")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Generate Deployer Training Documentation from a codebase."
    )
    parser.add_argument(
        "--path", "-p",
        default=".",
        help="Path to the repository root (default: current directory)"
    )
    parser.add_argument(
        "--output", "-o",
        default="Deployer_Guide.md",
        help="Output file path (default: Deployer_Guide.md)"
    )
    parser.add_argument(
        "--model", "-m",
        default=None,
        help=f"Specific model to use. If omitted, tries {PRIMARY_MODEL} then {FALLBACK_MODEL}."
    )
    
    args = parser.parse_args()
    
    repo_root = Path(args.path).resolve()
    if not repo_root.exists():
        print(f"Error: Path not found: {repo_root}")
        sys.exit(1)
    
    print(f"📂 Scanning codebase: {repo_root}")
    files_data = scan_codebase(repo_root)
    print(f"📄 Found {len(files_data)} files to analyze.")
    
    if not files_data:
        print("Error: No files found to analyze.")
        sys.exit(1)
    
    context = build_context(files_data)
    print(f"📊 Total context size: {len(context):,} characters")
    
    print("⏳ Generating documentation...")
    documentation = generate_documentation(context, args.model)
    
    output_path = Path(args.output)
    output_path.write_text(documentation, encoding="utf-8")
    print(f"✅ Documentation saved to: {output_path}")
    
    print("\n⚠️  AI-generated documentation - Human review recommended.")


if __name__ == "__main__":
    main()
