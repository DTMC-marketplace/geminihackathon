#!/usr/bin/env python3
"""
EU AI Act Article 73 - Incident Management Demo
===============================================
Complete demonstration of the incident management workflow.
Shows detection, classification, timeline tracking, and remediation.
"""

from incident_management import IncidentManager
#from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import time
import json

console = Console()

def demo():
    """Run complete incident management demo"""
    console.print(Panel.fit(
        "[bold cyan]EU AI Act Article 73 - Incident Management Demo[/bold cyan]\n\n"
        "This demo shows:\n"
        "1. Incident creation\n"
        "2. AI-assisted severity classification\n"
        "3. Causal link establishment\n"
        "4. Reporting timeline tracking\n"
        "5. AI-suggested remediation\n"
        "6. Complete incident display",
        title="🇪🇺 Demo",
        border_style="cyan"
    ))
    
    console.print("\n[dim]Initializing Incident Manager...[/dim]")
    manager = IncidentManager(use_ai=True)
    
    if not manager.use_ai:
        console.print("[yellow]⚠️  AI features disabled (GEMINI_API_KEY not set)[/yellow]")
        console.print("[yellow]   Demo will work but without AI classification/suggestions[/yellow]\n")
    
    # Step 1: Create incident
    console.print("\n[bold cyan]Step 1: Creating Incident[/bold cyan]")
    console.print("[dim]Creating a test incident for demonstration...[/dim]")
    
    incident = manager.create_incident(
        title="AI System Produced Harmful Medical Advice",
        description=(
            "The AI system provided incorrect dosage recommendations that could lead to patient harm. "
            "The system suggested 10x the recommended dose for a pediatric medication. "
            "This was detected through automated monitoring of prescription patterns."
        ),
        ai_system_id="MED-AI-001",
        ai_system_name="Medical Diagnosis Assistant v2.0",
        member_state="Germany",
        detected_by="automated",
        metadata={"test": True, "demo": True}
    )
    
    console.print(f"[green]✓[/green] Created incident: [bold]{incident.id}[/bold]")
    console.print(f"Title: {incident.title}")
    console.print(f"Detected: {incident.detected_at.strftime('%Y-%m-%d %H:%M:%S')}")
    time.sleep(1)
    
    # Step 2: Classify severity
    console.print("\n[bold cyan]Step 2: Classifying Severity (AI-Assisted)[/bold cyan]")
    console.print("[dim]Analyzing incident against EU AI Act Article 3(49) definitions...[/dim]")
    
    if manager.use_ai:
        severity, incident_type, reporting_days = manager.classify_severity(incident)
        
        if severity:
            console.print(f"[green]✓[/green] Severity: [bold]{severity.value.upper()}[/bold]")
            if incident_type:
                type_names = {
                    "a": "Death or Serious Harm to Health",
                    "b": "Critical Infrastructure Disruption",
                    "c": "Fundamental Rights Infringement",
                    "d": "Property or Environment Harm"
                }
                console.print(f"[green]✓[/green] Type: [bold]{incident_type.value}[/bold] - {type_names.get(incident_type.value, 'Unknown')}")
            console.print(f"[green]✓[/green] Reporting Deadline: [bold]{reporting_days} days[/bold]")
            console.print(f"[green]✓[/green] Serious Incident: [bold]{'Yes' if incident.is_serious else 'No'}[/bold]")
        else:
            console.print("[yellow]⚠️  Classification requires manual review[/yellow]")
    else:
        console.print("[yellow]⚠️  AI classification skipped (API key not available)[/yellow]")
        console.print("[dim]   In production, this would require manual classification[/dim]")
    
    time.sleep(1)
    
    # Step 3: Establish causal link
    console.print("\n[bold cyan]Step 3: Establishing Causal Link[/bold cyan]")
    console.print("[dim]Determining relationship between AI system and incident...[/dim]")
    
    manager.establish_causal_link(
        incident,
        established=True,
        notes="Root cause analysis confirms AI model error in dosage calculation algorithm. "
              "The model incorrectly interpreted pediatric weight-based dosing guidelines."
    )
    
    console.print("[green]✓[/green] Causal link established")
    console.print(f"   Established at: {incident.causal_link_established_at.strftime('%Y-%m-%d %H:%M:%S')}")
    time.sleep(1)
    
    # Step 4: Check timeline
    console.print("\n[bold cyan]Step 4: Checking Reporting Timeline[/bold cyan]")
    console.print("[dim]Calculating deadline and remaining time...[/dim]")
    
    timeline = manager.track_reporting_timeline(incident)
    
    # Color code the status
    status_colors = {
        "reported": "green",
        "on_track": "green",
        "warning": "yellow",
        "urgent": "red",
        "overdue": "bold red",
        "partial": "yellow"
    }
    color = status_colors.get(timeline['status'], "white")
    
    console.print(f"[{color}]{timeline['message']}[/{color}]")
    
    if timeline.get('days_remaining') is not None:
        table = Table(title="Timeline Details", show_header=False, box=None)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="white")
        
        table.add_row("Days Remaining", str(timeline['days_remaining']))
        table.add_row("Hours Remaining", f"{timeline['hours_remaining']:.1f}")
        if timeline.get('deadline'):
            table.add_row("Deadline", timeline['deadline'])
        if timeline.get('timeline_days'):
            table.add_row("Reporting Timeline", f"{timeline['timeline_days']} days (Article 73)")
        
        console.print(table)
    
    time.sleep(1)
    
    # Step 5: Get remediation suggestions
    console.print("\n[bold cyan]Step 5: Getting Remediation Suggestions (AI-Assisted)[/bold cyan]")
    console.print("[dim]Generating AI-suggested remediation actions...[/dim]")
    
    if manager.use_ai:
        suggestions = manager.suggest_remediation(incident)
        
        if suggestions:
            console.print(f"[green]✓[/green] Generated {len(suggestions)} suggestions")
            
            table = Table(title="AI-Suggested Remediation Actions", show_header=True)
            table.add_column("#", style="cyan", width=3)
            table.add_column("Action", style="white")
            table.add_column("Source", style="dim")
            
            for i, suggestion in enumerate(suggestions[:5], 1):  # Show first 5
                table.add_row(str(i), suggestion, "AI")
                manager.add_remediation_action(incident, suggestion, ai_suggested=True)
            
            console.print(table)
            console.print(f"[dim]Added {min(5, len(suggestions))} actions to incident[/dim]")
        else:
            console.print("[yellow]⚠️  No suggestions generated[/yellow]")
    else:
        console.print("[yellow]⚠️  AI suggestions skipped (API key not available)[/yellow]")
        # Add manual action
        manager.add_remediation_action(
            incident,
            "Conduct root cause analysis of dosage calculation algorithm",
            ai_suggested=False
        )
        console.print("[green]✓[/green] Added manual remediation action")
    
    time.sleep(1)
    
    # Step 6: Display full incident
    console.print("\n[bold cyan]Step 6: Complete Incident Summary[/bold cyan]")
    console.print("[dim]Displaying full incident details...[/dim]\n")
    
    manager.display_incident(incident)
    
    # Additional summary
    console.print("\n[bold]Incident Workflow Status:[/bold]")
    workflow_table = Table(show_header=False, box=None)
    workflow_table.add_column("Step", style="cyan")
    workflow_table.add_column("Status", style="white")
    
    workflow_table.add_row("Detection", "✓ Complete")
    workflow_table.add_row("Classification", "✓ Complete" if incident.severity else "⚠️ Pending")
    workflow_table.add_row("Causal Link", "✓ Complete" if incident.causal_link_established else "⚠️ Pending")
    workflow_table.add_row("Remediation Planning", "✓ Complete" if incident.remediation_actions else "⚠️ Pending")
    workflow_table.add_row("Report Submission", "⚠️ Pending" if not incident.complete_report_submitted else "✓ Complete")
    workflow_table.add_row("Authority Notification", "⚠️ Pending" if not incident.authority_notified else "✓ Complete")
    
    console.print(workflow_table)
    
    # Final summary
    # #region agent log
    with open('/Users/jiangyuqing/geminihackathon/.cursor/debug.log', 'a') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"pre-fix","hypothesisId":"A","location":"demo_incident.py:196","message":"Before Panel.fit call","data":{"incident_id":incident.id},"timestamp":int(__import__('time').time()*1000)}) + '\n')
    # #endregion
    panel_obj = Panel.fit(
        f"[bold green]✓ Demo Complete![/bold green]\n\n"
        f"Incident ID: [bold]{incident.id}[/bold]\n"
        f"Status: [bold]{incident.status.value}[/bold]\n"
        f"Serious: [bold]{'Yes' if incident.is_serious else 'No'}[/bold]\n\n"
        f"[dim]View details:[/dim] [cyan]python incident_cli.py show {incident.id}[/cyan]\n"
        f"[dim]Check timeline:[/dim] [cyan]python incident_cli.py timeline {incident.id}[/cyan]\n"
        f"[dim]List all:[/dim] [cyan]python incident_cli.py list[/cyan]",
        title="Next Steps",
        border_style="green"
    )
    # #region agent log
    with open('/Users/jiangyuqing/geminihackathon/.cursor/debug.log', 'a') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"pre-fix","hypothesisId":"A","location":"demo_incident.py:210","message":"After Panel.fit call","data":{"panel_type":str(type(panel_obj))},"timestamp":int(__import__('time').time()*1000)}) + '\n')
    # #endregion
    console.print()  # Print newline separately
    console.print(panel_obj)  # Print panel separately
    
    console.print("\n[dim]Incident data saved to: incidents/{}.json[/dim]".format(incident.id))

if __name__ == "__main__":
    try:
        demo()
    except KeyboardInterrupt:
        console.print("\n[yellow]Demo interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {e}")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")
