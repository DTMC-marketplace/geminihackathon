---
name: deployer-training
description: Generate comprehensive deployer and developer training documentation by scanning a codebase. Use when user asks for onboarding guides, developer documentation, system overviews, or needs to understand a new codebase. Triggers on phrases like "create training materials", "generate developer guide", "explain this codebase", "onboarding documentation", or "deployer manual".
---

# Deployer Training Materials Generator

Generate comprehensive, production-quality training documentation by scanning and analyzing a codebase using Gemini AI.

## When to Use

- Creating onboarding documentation for new developers
- Generating deployer guides for operations teams
- Understanding a new or unfamiliar codebase
- Documenting a product before release
- EU AI Act Articles 13 & 14 compliance (Transparency & Human Oversight)

## Quick Start

```bash
python scripts/generate_training.py --path /path/to/repo
```

## Instructions

1. **Identify the target codebase**: Determine the repository root to scan.
2. **Run the generator**:

   ```bash
   python "AI Act skills packages/AI Act package/deployer-training/scripts/generate_training.py" \
     --path <path-to-repository> \
     --name "Your Product Name"
   ```

3. **Review the output**: Check project root `Output/Deployer_Guide.md` for the generated documentation.
4. **Human review**: Always recommend human review for accuracy and completeness.

## What You Get

A comprehensive `Deployer_Guide.md` with:

1. **Executive Summary**: High-level product overview.
2. **System Architecture**: Component diagrams (Mermaid), data flow, tech stack.
3. **Product Capabilities**: Core features, user journeys, configuration options.
4. **Developer Onboarding**: Environment setup, extension patterns, testing guidelines.
5. **Operational Guide**: Deployment strategy, troubleshooting & limitations.

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--path` | string | `.` | Path to the repository root |
| `--output` | string | `Deployer_Guide.md` | Output file path |
| `--model` | string | Auto | Specific model (uses `gemini-3-pro-preview` then `gemini-2.0-flash-exp` as fallback) |

## Requirements

- Python 3.8+
- `google-genai` package: `pip install google-genai`
- `GEMINI_API_KEY` environment variable set

## Best Practices

- Run on a clean checkout of the repository.
- The generator respects `.gitignore` and excludes `.env` files for security.
- For large codebases, review the "Total context size" output to ensure it fits in the model's context window.
- Always perform human review on generated documentation.

## EU AI Act Compliance

This tool addresses:

- **Article 13**: Transparency and provision of information to users
- **Article 14**: Human oversight requirements (documentation for deployers)
