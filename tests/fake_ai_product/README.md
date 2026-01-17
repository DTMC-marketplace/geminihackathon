# Fake AI Product

This is a **fake AI product** created to test the Deployer Training Generator.

## Overview

FakeAI is a sentiment analysis API that:

1. Takes text input from users.
2. Uses a pre-trained model to classify sentiment (positive, negative, neutral).
3. Returns a JSON response with the classification and confidence score.

## Architecture

- **API Layer**: Flask-based REST API (`src/api.py`)
- **Model Layer**: Simple Naive Bayes classifier (`src/model.py`)
- **Utils**: Helper functions for text preprocessing (`src/utils.py`)

## Getting Started

```bash
pip install -r requirements.txt
python src/api.py
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 5000 | API listening port |
| `MODEL_PATH` | `models/nb_model.pkl` | Path to trained model |
