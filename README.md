# Geminihackathon: EU AI Act Compliance Project

Comprehensive tools and systems for EU AI Act (Regulation 2024/1689) compliance, including incident management, risk assessment, and regulatory query capabilities.

## Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 2. Set Up API Key

```bash
export GEMINI_API_KEY="your-api-key-here"
```

### 3. Run Main AI Act Query Tool

```bash
# Interactive mode
python ai_act_cli.py

# Single query
python ai_act_cli.py "What are the requirements for serious incident reporting?"
```
### AI Act Query Tool

**Files:**
- `ai_act_cli.py` - Main query interface
- `query_ai_act.py` - Single-shot queries
- `setup_ai_act_store.py` - Knowledge base setup

**Usage:**
```bash
python ai_act_cli.py
```

## Requirements

- Python 3.11+
- Gemini API key (for AI features)
- See `requirements.txt` for Python packages

