#!/usr/bin/env python3
"""
EU AI Act GDPR - Interactive Agent (CLI)
===================================
A robust terminal-based agent for querying the EU AI Act and GDPR.
Uses Gemini's Long Context window to analyze the full regulation text.

EU AI Act Compliance: LIMITED RISK - Article 50 (Chatbot Transparency)
Classification Date: 2025-01-07
Risk Level: Limited Risk (Chatbot/Conversational AI)
Applicable Requirements: Article 50(1) - Transparency obligations

Usage:
    python ai_act_cli.py
"""

import sys
from pathlib import Path
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from datetime import datetime

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Error: 'google-genai' package not found. Run: pip install google-genai")
    sys.exit(1)

import setup_ai_act_store

# Configuration
VERSION = "1.0.0"
SYSTEM_NAME = "EU AI Act Query Assistant"
EU_AI_ACT_RISK_LEVEL = "Limited Risk"
EU_AI_ACT_CLASSIFICATION_DATE = "2025-01-07"

# Load API key from environment variable
import os
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    # Clean API key: strip whitespace and take only first line
    GEMINI_API_KEY = GEMINI_API_KEY.strip().split('\n')[0].split('\r')[0]
if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY environment variable not set.")
    print("Please set it with: export GEMINI_API_KEY='your-api-key-here'")
    print("Or create a .env file (see .env.example)")
    sys.exit(1)
BASE_DIR = Path(__file__).resolve().parent
ARTICLES_DIR = BASE_DIR / "articles"
AI_ACT_TEXT_PATH = ARTICLES_DIR / "EU_AI_Act_Full_Text.txt"
GDPR_TEXT_PATH = ARTICLES_DIR / "GDPR_Full_Text.txt"

MODEL_NAME = "gemini-3-pro-preview"

class AIActAgent:
    def __init__(self):
        self.console = Console()
        self.client = None
        self.full_text = ""
        self.history = []
        
        self.initialize_agent()
        
    def initialize_agent(self):
        """Initialize API client and load content."""
        self.console.print("[dim]Initializing agent...[/dim]")
        
        # 0. Setup AI Act Store
        try:
            setup_ai_act_store.main()
        except Exception as e:
            self.console.print(f"[bold red]Error running setup script:[/bold red] {e}")
            

        # 1. Setup Client
        try:
            self.client = genai.Client(api_key=GEMINI_API_KEY)
        except Exception as e:
            self.console.print(f"[bold red]Error initializing client:[/bold red] {e}")
            sys.exit(1)
            
        # 2. Load AI Act Text
        if not AI_ACT_TEXT_PATH.exists():
            self.console.print(f"[bold red]Error:[/bold red] File not found: {AI_ACT_TEXT_PATH}")
            sys.exit(1)
            
        try:
            self.full_text = AI_ACT_TEXT_PATH.read_text(encoding='utf-8')
            self.console.print(f"[green]✓[/green] Loaded EU AI Act text ({len(self.full_text)} characters)")
        except Exception as e:
            self.console.print(f"[bold red]Error reading file:[/bold red] {e}")
            sys.exit(1)

    def chat_loop(self):
        """Main interactive chat loop."""
        self.console.clear()
        self.console.print(Panel.fit(
            "[bold cyan]EU AI Act and GDPR Regulatory Agent[/bold cyan]\n"
            "Ask questions about the regulation. I have read the full text.\n"
            "[dim]Type 'exit', 'quit', or 'q' to end session.[/dim]",
            title=f"🇪🇺 EU AI Act and GDPR Agent v{VERSION}",
            border_style="cyan"
        ))

        # EU AI Act Article 50 Compliance: Chatbot Disclosure
        self.console.print()
        self.console.print(Panel.fit(
            "🤖 [bold yellow]AI Assistant Disclosure (EU AI Act Article 50)[/bold yellow]\n\n"
            f"You are interacting with an AI-powered system using [bold]Google {MODEL_NAME}[/bold].\n"
            "This system analyzes the EU AI Act and GDPR regulation text to provide information.\n\n"
            "[bold]Important Notices:[/bold]\n"
            "[dim]• Responses are AI-generated and should be verified with official sources\n"
            "• This is NOT legal advice - consult qualified legal counsel for compliance decisions\n"
            "• Information is based on Regulation (EU) 2024/1689 (EU AI Act) and GDPR\n"
            f"• System Classification: {EU_AI_ACT_RISK_LEVEL} AI System\n"
            f"• Model: {MODEL_NAME} | Version: {VERSION} | Classified: {EU_AI_ACT_CLASSIFICATION_DATE}[/dim]",
            title="⚠️  Transparency Notice",
            border_style="yellow"
        ))
        self.console.print()

        while True:
            try:
                # Get User Input
                question = Prompt.ask("\n[bold green]You[/bold green]")
                question = question.strip()
                
                if not question:
                    continue
                    
                if question.lower() in ['exit', 'quit', 'q']:
                    self.console.print("\n[yellow]Goodbye![/yellow]")
                    break
                    
                if question.lower() == 'clear':
                    self.console.clear()
                    self.history = []
                    self.console.print("[dim]Conversation history cleared.[/dim]")
                    continue

                # Process Query
                self.process_query(question)
                
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Goodbye![/yellow]")
                break
            except Exception as e:
                self.console.print(f"\n[bold red]An error occurred:[/bold red] {e}")

    def process_query(self, question: str):
        """Send query to Gemini and display response."""

        # We inject the full text into the system prompt (simulating RAG via Long Context)
        # This is more robust than Tool calls for this specific setup
        system_prompt = f"""You are an expert legal assistant on the EU AI Act (Regulation 2024/1689) and GDPR.

        IMPORTANT - EU AI Act Article 50 Compliance:
        You are an AI assistant. Users have been informed they are interacting with an AI system.
        Your responses must be helpful but include appropriate disclaimers about verification and legal counsel.

        CONTEXT DOCUMENT (Full Text of the Regulation):
        ================================================================================
        {self.full_text}
        ================================================================================

        Your goal is to provide accurate, comprehensive answers based ONLY on the provided context document above.

        Guidelines:
        1. ALWAYS cite specific Articles and paragraphs (e.g., "Article 5(1)").
        2. If the answer is not in the document, state that clearly.
        3. Be precise with legal definitions.
        4. Use structured formatting (bullet points, bold text).
        5. Remind users when appropriate that AI-generated responses should be verified with legal counsel.
        6. For compliance-critical questions, emphasize the importance of professional legal advice.
        """

        generate_config = types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.3, 
        )

        with self.console.status("[bold cyan]Analyzing...[/bold cyan]", spinner="dots"):
            try:
                # Use Chat to maintain history
                if not self.history: # Initialize chat if new
                     self.chat_session = self.client.chats.create(
                        model=MODEL_NAME,
                        config=generate_config,
                        history=[]
                    )
                
                response = self.chat_session.send_message(question)
                self.display_response(response)
                
            except Exception as e:
                self.console.print(f"[bold red]API Error:[/bold red] {e}")

    def display_response(self, response):
        """Render the response using Rich."""
        if response.text:
            self.console.print("\n[bold cyan]Agent:[/bold cyan]")
            md = Markdown(response.text)
            self.console.print(md)

            # EU AI Act Article 50 Compliance: AI-generated content notice
            self.console.print("\n[dim italic]⚠️  AI-generated response - Verify with official sources and legal counsel for compliance decisions[/dim italic]")
        else:
            self.console.print("\n[dim]No text response generated.[/dim]")

if __name__ == "__main__":
    # Handle command-line arguments
    if len(sys.argv) > 1 and sys.argv[1] in ['--version', '-v']:
        console = Console()
        console.print(f"\n[bold cyan]{SYSTEM_NAME}[/bold cyan]")
        console.print(f"Version: {VERSION}")
        console.print(f"Model: {MODEL_NAME}")
        console.print(f"EU AI Act Classification: {EU_AI_ACT_RISK_LEVEL}")
        console.print(f"Classification Date: {EU_AI_ACT_CLASSIFICATION_DATE}")
        console.print(f"Compliance: Article 50 (Chatbot Transparency)")
        sys.exit(0)

    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h']:
        console = Console()
        console.print(f"\n[bold cyan]{SYSTEM_NAME} v{VERSION}[/bold cyan]")
        console.print("\nAI-powered query tool for EU AI Act and GDPR regulations")
        console.print("\n[bold]Usage:[/bold]")
        console.print("  python ai_act_cli.py                    # Interactive mode")
        console.print("  python ai_act_cli.py [question]         # Single query mode")
        console.print("  python ai_act_cli.py --version          # Show version info")
        console.print("  python ai_act_cli.py --help             # Show this help")
        console.print("\n[bold]EU AI Act Compliance:[/bold]")
        console.print(f"  Risk Level: {EU_AI_ACT_RISK_LEVEL}")
        console.print("  Requirements: Article 50 (Transparency obligations for chatbots)")
        console.print("  Users are informed they are interacting with AI")
        console.print("\n[bold]Commands in Interactive Mode:[/bold]")
        console.print("  exit, quit, q    # Exit the program")
        console.print("  clear            # Clear conversation history")
        sys.exit(0)

    agent = AIActAgent()

    if len(sys.argv) > 1:
        # Single shot mode
        question = " ".join(sys.argv[1:])
        agent.console.print(f"\n[bold green]Query:[/bold green] {question}")
        agent.process_query(question)
    else:
        # Interactive mode
        agent.chat_loop()
