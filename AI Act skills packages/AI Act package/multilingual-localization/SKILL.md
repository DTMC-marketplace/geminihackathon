---
name: multilingual-localization
description: Translate documentation and instructions to EU languages while preserving formatting. Use when the user wants to translate, localize, or convert documents to another language, especially for EU AI Act Article 13 compliance (multilingual support documentation).
---

# Multilingual Localization

Translate documents (Markdown, plain text, HTML, etc.) to EU languages while preserving formatting. Supports EU AI Act Article 13 compliance for multilingual documentation requirements.

## Quick Start

```bash
python scripts/localize_document.py --file examples/sample_policy.md --lang "French"
```

## Instructions

1. **Identify the document** to translate and the target language.
2. **Run the translation script**:

   ```bash
   python "AI Act skills packages/AI Act package/multilingual-localization/scripts/localize_document.py" \
     --file <path-to-document> \
     --lang "<target-language>"
   ```

3. **Verify the output**: Check the project root `Output/` directory for the translated file.
4. **Human review**: Always recommend human review for technical accuracy and cultural appropriateness.

## Documentation

See [README.md](README.md) for architecture details and fallback logic configuration.

## Supported Formats

- Markdown (`.md`, `.markdown`)
- Plain text (`.txt`)
- reStructuredText (`.rst`)
- HTML (`.html`, `.htm`)
- YAML (`.yaml`, `.yml`)
- JSON (`.json`)
- XML (`.xml`)

## EU Languages Supported

Bulgarian, Croatian, Czech, Danish, Dutch, English, Estonian, Finnish, French, German, Greek, Hungarian, Irish, Italian, Latvian, Lithuanian, Maltese, Polish, Portuguese, Romanian, Slovak, Slovenian, Spanish, Swedish.

## Examples

**Translate README to German:**

```bash
python scripts/localize_document.py --file examples/sample_policy.md --lang "German"
# Output: examples/sample_policy_German.md
```

**Translate to French with custom output path:**

```bash
python scripts/localize_document.py --file docs/guide.md --lang "French" --output docs/fr/guide.md
```

**Translate multiple languages (batch):**

```bash
for lang in French German Spanish Italian; do
  python scripts/localize_document.py --file examples/sample_policy.md --lang "$lang"
done
```

## Requirements

- Python 3.8+
- `google-genai` package: `pip install google-genai`
- `GEMINI_API_KEY` environment variable set

## Best Practices

- Always perform human review on translated documents, especially for regulatory content.
- For legal or compliance documents, consult with native speakers or professional translators.
- Keep original documents as source of truth; regenerate translations when source changes.

## EU AI Act Compliance

This tool addresses:

- **Article 13**: Transparency and provision of information to users
- **Accessibility**: Making documentation available in EU languages
- **User Understanding**: Ensuring users can understand AI system documentation in their language
