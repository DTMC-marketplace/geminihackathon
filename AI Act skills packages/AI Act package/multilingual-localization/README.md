# Multilingual Localization Service

## Overview

This feature provides an automated translation service leveraging Google's Gemini models. It is designed to act as a resilient "Plugin" within the system, capable of falling back to alternative models if the primary high-performance model is unavailable or restricted.

**Primary Model**: `gemini-3-pro-preview` (Higher quality, better context)
**Fallback Model**: `gemini-2.0-flash-exp` (Faster, fallback for permissions/quota issues)

## How It Works

### Frontend Integration

The frontend (e.g., CLI or Web UI) invokes this service by calling the `localize_document.py` script.

- **Input**: User provides a file path and a target language.
- **Feedback**: The script prints progress (e.g., "Attempting translation with...", "Model failed...", "Success").
- **Output**: The frontend should look for the result in the `Output/` directory at the project root.

### Backend Workflow

1. **Load Configuration**: The system loads the `GEMINI_API_KEY` from the environment or `.env` file.
2. **Attempt Primary**: It first attempts to use `gemini-3-pro-preview`.
3. **Fallback**: If `gemini-3` fails (e.g., 403 Permission Denied, Rate Limit), it automatically retries with `gemini-2.0-flash-exp`.
4. **Result Storage**: The translated file is saved to the `Output/` folder (e.g., `Output/mysfile_French.md`).

## Usage

```bash
python scripts/localize_document.py --file documents/policy.md --lang "German"
```

## Architecture

- **Script**: `scripts/localize_document.py` (Core logic)
- **Output**: `Output/` (Centralized artifact storage)
- **Skill Definition**: `SKILL.md` (Agent instructions)
