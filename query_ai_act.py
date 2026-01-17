#!/usr/bin/env python3
"""
EU AI Act - Query Script
========================
Query the AI Act and GDPR File Search Store using Gemini's semantic search.

Requirements:
    pip install google-genai

Usage:
    export GEMINI_API_KEY="your-api-key-here"
    python query_ai_act.py "What are prohibited AI practices?"
"""

import re
import sys
from heapq import nlargest
from pathlib import Path
from typing import List, Optional, Tuple
from google import genai
from google.genai import types, errors
import os

# Configuration
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
BASE_DIR = Path(__file__).resolve().parent
STORE_INFO_PATH = BASE_DIR / "store_info.txt"
ARTICLES_DIR = BASE_DIR / "articles"
FULL_TEXT_PATH = ARTICLES_DIR / "EU_AI_Act_Full_Text.txt"
MODEL_NAME = "gemini-3-pro-preview"
MAX_CONTEXT_ARTICLES = 5
CONTEXT_SNIPPET_CHARS = 4000
STOPWORDS = {
    "what", "are", "the", "and", "for", "with", "that", "this", "from", "into",
    "your", "about", "which", "shall", "will", "does", "can", "may", "must",
    "should", "would", "could", "their", "there", "here", "have", "been",
    "such", "upon", "per", "other", "than", "while", "within", "who", "whom",
    "whose", "why", "how", "when", "where", "any", "each", "some", "many",
}

def get_store_name():
    """Get the store name from the saved info file."""
    if STORE_INFO_PATH.exists():
        with STORE_INFO_PATH.open('r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('store_name='):
                    return line.split('=', 1)[1].strip()
    return None

def load_full_text_sections() -> List[str]:
    """Split the consolidated EU AI Act text into reusable sections."""
    if not FULL_TEXT_PATH.exists():
        return []
    try:
        raw_text = FULL_TEXT_PATH.read_text(encoding='utf-8')
    except OSError:
        return []
    paragraphs = [segment.strip() for segment in raw_text.split("\n\n") if segment.strip()]
    return paragraphs


FULL_TEXT_SECTIONS = load_full_text_sections()


def load_gdpr_sections() -> List[dict]:
    """Read GDPR article files from the local articles directory."""
    if not ARTICLES_DIR.exists():
        return []

    sections: List[dict] = []
    for path in sorted(ARTICLES_DIR.glob("GDPR_Article_*.txt")):
        try:
            text = path.read_text(encoding='utf-8').strip()
        except OSError:
            continue
        if not text:
            continue
        first_line = text.splitlines()[0].strip()
        title = first_line if first_line else path.stem.replace('_', ' ')
        sections.append({'title': title, 'text': text})
    return sections


GDPR_SECTIONS = load_gdpr_sections()


def build_manual_context(question: str) -> List[dict]:
    """Return ranked AI Act or GDPR snippets for fallback answers."""
    tokens: List[Tuple[str, int]] = []
    question_lower = question.lower()
    for tok in re.findall(r"\w+", question_lower):
        if tok in STOPWORDS:
            continue
        if len(tok) <= 2 and tok != "ai":
            continue
        weight = 1
        if tok in {"prohibited", "practices"}:
            weight = 5
        elif tok == "ai":
            weight = 2
        elif tok == "gdpr":
            weight = 4
        tokens.append((tok, weight))
    if not tokens:
        return []

    scored_sections: List[Tuple[int, dict]] = []
    scored_sections.extend(score_ai_act_sections(tokens))
    scored_sections.extend(score_gdpr_sections(tokens, question_lower))

    if not scored_sections:
        return []

    top_matches = nlargest(MAX_CONTEXT_ARTICLES, scored_sections, key=lambda item: item[0])
    return [match[1] for match in top_matches]


def score_ai_act_sections(tokens: List[Tuple[str, int]]) -> List[Tuple[int, dict]]:
    """Score EU AI Act sections for relevance."""
    if not FULL_TEXT_SECTIONS:
        return []

    scored: List[Tuple[int, dict]] = []
    seen_indices = set()
    for idx, section in enumerate(FULL_TEXT_SECTIONS):
        section_lower = section.lower()
        score = sum(section_lower.count(token) * weight for token, weight in tokens)
        if 'prohibited ai practices' in section_lower:
            score += 50
        if 'article 5' in section_lower:
            score += 25
        if score <= 0:
            continue

        if 'prohibited ai practices' in section_lower:
            if idx in seen_indices:
                continue
            end_idx = min(idx + 20, len(FULL_TEXT_SECTIONS))
            combined_sections = "\n".join(FULL_TEXT_SECTIONS[idx:end_idx])
            snippet = combined_sections.strip()
            seen_indices.update(range(idx, end_idx))
            title = "AI Act Article 5"
        else:
            if idx in seen_indices:
                continue
            snippet = section.strip()
            seen_indices.add(idx)
            title_match = re.search(r"Article\s+\d+[a-zA-Z]*", section)
            title = title_match.group(0) if title_match else "EU AI Act Context"

        if len(snippet) > CONTEXT_SNIPPET_CHARS:
            snippet = snippet[:CONTEXT_SNIPPET_CHARS] + "..."
        scored.append((score, {'title': title, 'text': snippet}))
    return scored


def score_gdpr_sections(tokens: List[Tuple[str, int]], question_lower: str) -> List[Tuple[int, dict]]:
    """Score GDPR article files for relevance."""
    if not GDPR_SECTIONS:
        return []

    gdpr_focus_terms = ['gdpr', 'general data protection regulation', 'personal data']
    gdpr_focus = any(term in question_lower for term in gdpr_focus_terms)
    scored: List[Tuple[int, dict]] = []

    for section in GDPR_SECTIONS:
        text_lower = section['text'].lower()
        score = sum(text_lower.count(token) * weight for token, weight in tokens)
        score += text_lower.count('gdpr')
        if gdpr_focus:
            score += 15
        if 'personal data' in question_lower and 'personal data' in text_lower:
            score += 5

        if score <= 0:
            continue

        snippet = section['text']
        if len(snippet) > CONTEXT_SNIPPET_CHARS:
            snippet = snippet[:CONTEXT_SNIPPET_CHARS] + "..."
        scored.append((score, {'title': section['title'], 'text': snippet}))
    return scored


def query_ai_act(question: str, store_name: str = None) -> Tuple[types.GenerateContentResponse, Optional[List[dict]]]:
    """
    Query the AI Act and GDPR using Gemini File Search.
    
    Args:
        question: The question to ask about the AI Act and GDPR
        store_name: Optional store name (will load from file if not provided)
    
    Returns:
        The model's response with citations
    """
    if not GEMINI_API_KEY:
        raise ValueError("Please set the GEMINI_API_KEY environment variable")
    
    if not store_name:
        store_name = get_store_name()
        if not store_name:
            raise ValueError("Store name not found. Please run setup_ai_act_store.py first.")
    
    # Initialize client
    client = genai.Client(api_key=GEMINI_API_KEY)

    base_system_prompt = (
        "You are an expert on the EU AI Act (Regulation 2024/1689) and the GDPR (Regulation 2016/679).\n"
        "Use the File Search tool to find relevant information from those regulations "
        "and provide accurate, well-cited answers. When quoting provisions, mention "
        "the regulation and article number. Be precise and refer to the exact text "
        "of the regulations whenever possible."
    )

    # Configure File Search tool using the typed helper classes
    # Check if FileSearch is available (it may not exist in older versions)
    tools = None
    if hasattr(types, "FileSearch"):
        try:
            tools = [
                types.Tool(
                    file_search=types.FileSearch(
                        file_search_store_names=[store_name]
                    )
                )
            ]
        except (AttributeError, TypeError) as e:
            # FileSearch exists but may not be configured correctly
            print(f"FileSearch configuration error: {e}")
            tools = None
    else:
        # FileSearch not available in this version, will use fallback
        print("FileSearch tool not available in this google-genai version. Using fallback mechanism.")

    # Only try FileSearch if tools were configured
    if tools:
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=question,
                config=types.GenerateContentConfig(
                    system_instruction=base_system_prompt,
                    tools=tools
                )
            )
            return response, None
        except errors.ClientError as err:
            # Fallback for accounts where File Search is unavailable.
            message = str(err)
            if "tool_type" not in message and "File Search" not in message:
                raise

    # Fallback: use local article excerpts as context
    context_sections = build_manual_context(question)
    if not context_sections:
        if tools:
            # If we tried FileSearch and it failed, and we have no fallback context, raise
            raise ValueError("File Search unavailable and no local context available.")
        else:
            # If FileSearch wasn't available from the start, this is expected
            raise ValueError("No local context available and FileSearch not supported in this version.")

    context_block = "\n\n".join(
        f"### {section['title']}\n{section['text']}" for section in context_sections
    )
    fallback_prompt = (
        base_system_prompt
        + "\n\nUse the following excerpts from the EU AI Act and GDPR as context:\n"
        + context_block
        + "\n\nIf the answer is not covered, explain that explicitly."
    )

    print("⚠️  File Search tool unavailable. Using local article excerpts as context.")

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=question,
        config=types.GenerateContentConfig(
            system_instruction=fallback_prompt,
            tools=None
        )
    )
    return response, context_sections

def format_response(response, fallback_sources: Optional[List[dict]] = None):
    """Format the response with citations."""
    output = []
    
    # Main response text
    if response.text:
        output.append("=" * 60)
        output.append("ANSWER:")
        output.append("=" * 60)
        output.append(response.text)
    
    # Check for citations in candidates
    if response.candidates and response.candidates[0].grounding_metadata:
        grounding = response.candidates[0].grounding_metadata
        if grounding.grounding_chunks:
            output.append("\n" + "=" * 60)
            output.append("SOURCES:")
            output.append("=" * 60)
            for i, chunk in enumerate(grounding.grounding_chunks[:5], 1):
                if hasattr(chunk, 'retrieved_context'):
                    ctx = chunk.retrieved_context
                    output.append(f"\n[{i}] {getattr(ctx, 'title', 'Document')}")
                    if hasattr(ctx, 'text'):
                        text_preview = ctx.text[:200] + "..." if len(ctx.text) > 200 else ctx.text
                        output.append(f"    {text_preview}")
    elif fallback_sources:
        output.append("\n" + "=" * 60)
        output.append("SOURCES:")
        output.append("=" * 60)
        for i, section in enumerate(fallback_sources, 1):
            preview = section['text']
            preview = preview[:200] + "..." if len(preview) > 200 else preview
            output.append(f"\n[{i}] {section['title']}")
            output.append(f"    {preview}")

    return "\n".join(output)

def interactive_mode(store_name: str):
    """Run in interactive mode for multiple queries."""
    print("=" * 60)
    print("EU AI Act + GDPR Query System")
    print("=" * 60)
    print("Type your questions about the AI Act and GDPR. Type 'quit' to exit.\n")
    
    while True:
        try:
            question = input("\n📋 Your question: ").strip()
            if question.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            if not question:
                continue
                
            print("\n🔍 Searching the AI Act / GDPR corpus...\n")
            response, fallback_sources = query_ai_act(question, store_name)
            print(format_response(response, fallback_sources))
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

def main():
    """Main function."""
    store_name = get_store_name()
    
    if len(sys.argv) > 1:
        # Single question mode
        question = " ".join(sys.argv[1:])
        print(f"\n🔍 Question: {question}\n")
        response, fallback_sources = query_ai_act(question, store_name)
        print(format_response(response, fallback_sources))
    else:
        # Interactive mode
        interactive_mode(store_name)

if __name__ == "__main__":
    main()
