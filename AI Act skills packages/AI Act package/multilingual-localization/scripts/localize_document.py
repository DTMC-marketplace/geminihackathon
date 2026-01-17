#!/usr/bin/env python3
"""
Multilingual Document Localization Tool
=======================================
Translates documents (Markdown, plain text, etc.) to a target language
while preserving formatting.

EU AI Act Compliance: LIMITED RISK - Article 50 (Transparency)
Classification: This tool uses AI for translation.

Usage:
    python localize_document.py --file document.md --lang "French"
    python localize_document.py --file document.md --lang "German" --model "gemini-3-pro-preview"
"""

import argparse
import os
import sys
from pathlib import Path

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Error: 'google-genai' package not found. Run: pip install google-genai")
    sys.exit(1)

# Configuration
PRIMARY_MODEL = "gemini-3-pro-preview"
FALLBACK_MODEL = "gemini-2.0-flash-exp"

# Supported languages for EU market coverage (Article 13 compliance)
EU_LANGUAGES = [
    "Bulgarian", "Croatian", "Czech", "Danish", "Dutch", "English", "Estonian",
    "Finnish", "French", "German", "Greek", "Hungarian", "Irish", "Italian",
    "Latvian", "Lithuanian", "Maltese", "Polish", "Portuguese", "Romanian",
    "Slovak", "Slovenian", "Spanish", "Swedish"
]


def load_env_file():
    """Manually load .env file from current or parent directories."""
    import re
    
    # Start from current file's directory and go up
    current_dir = Path(__file__).resolve().parent
    
    # Search up to 5 levels (scripts -> skill -> package -> skills -> repo root)
    for _ in range(6):
        env_path = current_dir / ".env"
        if env_path.exists():
            try:
                content = env_path.read_text(encoding="utf-8")
                for line in content.splitlines():
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    
                    # Match KEY=VALUE or KEY="VALUE"
                    match = re.match(r'^GEMINI_API_KEY\s*=\s*(?:["\'])(.*?)(?:["\'])$|^GEMINI_API_KEY\s*=\s*(.*?)$', line)
                    if match:
                        key = match.group(1) or match.group(2)
                        os.environ["GEMINI_API_KEY"] = key
                        return
            except Exception:
                pass # Ignore errors reading .env
        
        if current_dir.parent == current_dir:
            break # Root reached
        current_dir = current_dir.parent


def get_api_key() -> str:
    """Get GEMINI_API_KEY from environment or .env file."""
    # Try loading from .env if not in environment
    if not os.environ.get("GEMINI_API_KEY"):
        load_env_file()
        
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        print("Set it with: export GEMINI_API_KEY='your-api-key-here'")
        print("Or ensure a .env file exists in the project root.")
        sys.exit(1)
    return api_key


def detect_format(file_path: Path) -> str:
    """Detect file format based on extension."""
    extension = file_path.suffix.lower()
    format_map = {
        ".md": "markdown",
        ".markdown": "markdown",
        ".txt": "plain text",
        ".rst": "reStructuredText",
        ".html": "HTML",
        ".htm": "HTML",
        ".xml": "XML",
        ".json": "JSON",
        ".yaml": "YAML",
        ".yml": "YAML",
    }
    return format_map.get(extension, "plain text")


def build_translation_prompt(content: str, target_lang: str, file_format: str) -> str:
    """Build a prompt that instructs the model to translate while preserving format."""
    return f"""You are a professional translator specializing in EU regulatory and technical documentation.

TASK: Translate the following {file_format} document to {target_lang}.

RULES:
1. PRESERVE all formatting exactly (headers, lists, bold, italics, code blocks, links).
2. DO NOT translate:
   - Code snippets inside code blocks (```...```)
   - Variable names, file paths, URLs
   - Special directives or frontmatter (e.g., YAML between ---)
3. Translate naturally and appropriately for the target culture.
4. Maintain consistency with EU regulatory terminology.
5. For technical terms without direct translation, keep the English term with a brief parenthetical explanation if needed.

DOCUMENT TO TRANSLATE:
================================================================================
{content}
================================================================================

OUTPUT: Return ONLY the translated document, preserving all original formatting. Do not add any explanation or commentary."""


def translate_document(content: str, target_lang: str, file_format: str, model_name: str = None) -> str:
    """Call Gemini API to translate the document with fallback logic."""
    api_key = get_api_key()
    client = genai.Client(api_key=api_key)
    
    prompt = build_translation_prompt(content, target_lang, file_format)
    generate_config = types.GenerateContentConfig(temperature=0.3)
    
    # Determined primary and fallback models
    models_to_try = []
    if model_name:
        models_to_try.append(model_name)
    else:
        models_to_try = [PRIMARY_MODEL, FALLBACK_MODEL]
    
    last_exception = None
    
    for model in models_to_try:
        print(f"🤖 Attempting translation with model: {model}...")
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=generate_config
            )
            
            if response.text:
                return response.text.strip()
            # If no text but no exception, it might be safety filter or empty response
            print(f"⚠️  Model {model} returned no text.")
            
        except Exception as e:
            print(f"❌ Model {model} failed: {e}")
            last_exception = e
            
    # If we get here, all attempts failed
    print("Error: content generation failed with all attempted models.")
    if last_exception:
        print(f"Last error: {last_exception}")
    sys.exit(1)


def generate_output_path(input_path: Path, target_lang: str) -> Path:
    """Generate output file path in the project root Output directory."""
    # Find project root (where .env is usually located, or go up 5 levels)
    # Current script is in: AI Act skills packages/AI Act package/multilingual-localization/scripts/
    # Root is up 4 levels.
    
    # Use explicit absolute path from user request context if possible, otherwise relative
    # User specified @[Output] which mapped to c:\Users\Nzettodess\Downloads\Gemini-Hackathon\Output
    
    # Try to find root dynamically
    current_dir = Path(__file__).resolve().parent
    repo_root = current_dir.parent.parent.parent.parent # script -> skill -> package -> skills -> repo
    output_dir = repo_root / "Output"
    
    if not output_dir.exists():
        # Fallback to local Output if root doesn't exist (unlikely in this env)
        output_dir = current_dir.parent / "Output"
        output_dir.mkdir(exist_ok=True)
        
    # Sanitize language name for filename
    lang_safe = target_lang.replace(" ", "_").replace("/", "_")
    stem = input_path.stem
    suffix = input_path.suffix
    return output_dir / f"{stem}_{lang_safe}{suffix}"


def main():
    parser = argparse.ArgumentParser(
        description="Translate documents with AI Act compliance and model fallback."
    )
    parser.add_argument(
        "--file", "-f",
        required=True,
        help="Path to the input document"
    )
    parser.add_argument(
        "--lang", "-l",
        required=True,
        help=f"Target language (e.g., 'French'). EU languages: {', '.join(EU_LANGUAGES[:5])}..."
    )
    parser.add_argument(
        "--model", "-m",
        default=None,
        help=f"Specific model to use. If omitted, tries {PRIMARY_MODEL} then {FALLBACK_MODEL}."
    )
    parser.add_argument(
        "--output", "-o",
        help="Custom output file path. Defaults to 'Output' folder in project root."
    )
    
    args = parser.parse_args()
    
    # Validate input file
    input_path = Path(args.file)
    if not input_path.exists():
        print(f"Error: File not found: {input_path}")
        sys.exit(1)
    
    # Read input
    try:
        content = input_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    # Detect format
    file_format = detect_format(input_path)
    print(f"📄 Input: {input_path} ({file_format})")
    print(f"🌍 Target Language: {args.lang}")
    
    # Translate
    print("⏳ Translating...")
    translated_content = translate_document(content, args.lang, file_format, args.model)
    
    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = generate_output_path(input_path, args.lang)
    
    # Write output
    try:
        output_path.write_text(translated_content, encoding="utf-8")
        print(f"✅ Output: {output_path}")
    except Exception as e:
        print(f"Error writing output: {e}")
        sys.exit(1)
    
    # EU AI Act Article 50 Compliance Notice
    print("\n⚠️  AI-generated translation - Human review recommended.")


if __name__ == "__main__":
    main()
