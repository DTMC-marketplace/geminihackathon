#!/usr/bin/env python3
"""
Deployer Training Materials Generator

Scans a codebase and generates comprehensive training documentation
for deployers and developers using Gemini AI.

Uses section-by-section generation to avoid truncation issues.

EU AI Act Articles 13 & 14 Compliance Tool.
"""

import argparse
import os
import sys
import re
from pathlib import Path
from typing import List, Set, Dict

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
    ".sh", ".bash", ".zsh", ".ps1", ".bat", ".cmd", ".dart",
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

# Documentation sections to generate
SECTIONS = [
    {
        "name": "Executive Summary",
        "prompt": """Generate ONLY the Executive Summary section for this codebase.
Write 2-3 paragraphs providing a high-level overview of what this product does.
Target audience: CTO or project manager.
Start directly with the content, no section header needed."""
    },
    {
        "name": "System Architecture",
        "prompt": """Generate ONLY the System Architecture section for this codebase.
Include:
### 2.1 Component Diagram
Create a Mermaid diagram showing the main components and their relationships.

### 2.2 Data Flow
Explain how data moves through the system step by step.

### 2.3 Tech Stack
List all technologies, frameworks, and dependencies used.

Start directly with ### 2.1, no main section header needed."""
    },
    {
        "name": "Product Capabilities",
        "prompt": """Generate ONLY the Product Capabilities section for this codebase.
Include:
### 3.1 Core Features
For EACH major feature: What it does, How it works, Key configuration options.

### 3.2 User Journeys
Step-by-step walkthroughs for:
- Journey for "The Deployer" (setting up and running)
- Journey for "The End User" (using the product)

### 3.3 Configuration Options
Create a comprehensive markdown table of all environment variables, flags, settings.

Start directly with ### 3.1, no main section header needed."""
    },
    {
        "name": "Developer Onboarding",
        "prompt": """Generate ONLY the Developer Onboarding section for this codebase.
Include:
### 4.1 Environment Setup
Step-by-step instructions to get a development environment running.

### 4.2 Extension Patterns
Explain how to add new features, modules, or plugins to this codebase.

### 4.3 Testing Guidelines
How to run tests, write new tests, and the testing philosophy.

Start directly with ### 4.1, no main section header needed."""
    },
    {
        "name": "Operational Guide",
        "prompt": """Generate ONLY the Operational Guide section for this codebase.
Include:
### 5.1 Deployment Strategy
How to deploy this product to production.

### 5.2 Troubleshooting & Limitations
Common issues, known bugs, rate limits, and workarounds.

Start directly with ### 5.1, no main section header needed."""
    }
]


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
    
    if path.name in EXCLUDED_FILES:
        return True
    
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
    gitignore_patterns.update({"node_modules", ".git", "__pycache__", ".venv", "venv", "dist", "build"})
    
    for root, dirs, files in os.walk(repo_root):
        root_path = Path(root)
        dirs[:] = [d for d in dirs if not is_ignored(root_path / d, repo_root, gitignore_patterns)]
        
        for file_name in files:
            file_path = root_path / file_name
            if is_ignored(file_path, repo_root, gitignore_patterns):
                continue
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
                pass
    
    return files_data


def build_context(files_data: List[dict]) -> str:
    """Build the context string from scanned files."""
    context_parts = []
    for file_info in files_data:
        context_parts.append(f"--- FILE: {file_info['path']} ---\n{file_info['content']}\n")
    return "\n".join(context_parts)


def generate_section(client, context: str, section: Dict, model_name: str = None) -> str:
    """Generate a single section of the documentation."""
    system_prompt = """You are a Senior Developer Instructor with 20 years of experience.
Your task is to analyze a codebase and generate ONE specific section of training documentation.
Be detailed and specific. Reference actual file paths and code snippets where helpful.
Use Mermaid diagrams where appropriate.
Write in a teaching tone, not a dry technical manual.
If information is missing from the codebase, note it as "Not Found in Codebase"."""

    user_prompt = f"""{section['prompt']}

CODEBASE CONTENTS:
{context}

Generate the section now. Be comprehensive but focused on this section only."""

    generate_config = types.GenerateContentConfig(
        temperature=0.4,
        system_instruction=system_prompt
    )
    
    models_to_try = [model_name] if model_name else [PRIMARY_MODEL, FALLBACK_MODEL]
    
    for model in models_to_try:
        try:
            response = client.models.generate_content(
                model=model,
                contents=user_prompt,
                config=generate_config
            )
            if response.text:
                return response.text.strip()
        except Exception as e:
            print(f"    ⚠️  {model} failed: {e}")
            continue
    
    return f"*[Error: Failed to generate {section['name']} section]*"


def generate_documentation(context: str, product_name: str, model_name: str = None) -> str:
    """Generate complete documentation by calling API for each section."""
    api_key = get_api_key()
    client = genai.Client(api_key=api_key)
    
    sections_content = []
    
    for i, section in enumerate(SECTIONS, 1):
        print(f"  📝 Generating Section {i}/{len(SECTIONS)}: {section['name']}...")
        content = generate_section(client, context, section, model_name)
        sections_content.append((section['name'], content))
    
    # Assemble the final document
    doc = f"# {product_name} - Deployer & Developer Guide\n\n"
    
    section_numbers = ["1", "2", "3", "4", "5"]
    for (name, content), num in zip(sections_content, section_numbers):
        doc += f"## {num}. {name}\n\n{content}\n\n"
    
    return doc


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
        default="Output/Deployer_Guide.md",
        help="Output file path (default: Output/Deployer_Guide.md)"
    )
    parser.add_argument(
        "--name", "-n",
        default=None,
        help="Product name for the guide title (default: inferred from directory name)"
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
    
    product_name = args.name or repo_root.name
    
    print(f"📂 Scanning codebase: {repo_root}")
    files_data = scan_codebase(repo_root)
    print(f"📄 Found {len(files_data)} files to analyze.")
    
    if not files_data:
        print("Error: No files found to analyze.")
        sys.exit(1)
    
    context = build_context(files_data)
    print(f"📊 Total context size: {len(context):,} characters")
    
    print("⏳ Generating documentation (section by section)...")
    documentation = generate_documentation(context, product_name, args.model)
    
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(documentation, encoding="utf-8")
    print(f"✅ Documentation saved to: {output_path}")
    
    print("\n⚠️  AI-generated documentation - Human review recommended.")


if __name__ == "__main__":
    main()
