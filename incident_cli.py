#!/usr/bin/env python3
"""
EU AI Act Article 73 - Incident Management CLI
===============================================
Interactive command-line interface for managing serious incidents
according to EU AI Act Article 73 requirements.

Usage:
    python incident_cli.py
    python incident_cli.py list
    python incident_cli.py show INC-20250107-120000-0
    python incident_cli.py create "Title" "Description" "AI-SYS-001" "System Name" "Germany"
"""

import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.markdown import Markdown
from datetime import datetime

from incident_management import (
    IncidentManager, Incident, IncidentSeverity, 
    SeriousIncidentType, IncidentStatus
)

console = Console()

def print_header():
    """Print CLI header"""
    console.print(Panel.fit(
        "[bold cyan]EU AI Act Article 73[/bold cyan]\n"
        "[bold]Serious Incident Management System[/bold]\n\n"
        "Compliance: Article 73 - Reporting of serious incidents\n"
        "Timeline Tracking: 2/10/15 days reporting deadlines\n"
        "AI-Assisted: Detection, classification, remediation suggestions",
        title="🇪🇺 Incident Management",
        border_style="cyan"
    ))

def cmd_list(manager: IncidentManager, status: str = None, severity: str = None):
    """List all incidents"""
    status_enum = None
    if status:
        try:
            status_enum = IncidentStatus(status.lower())
        except ValueError:
            console.print(f"[red]Invalid status: {status}[/red]")
            return
    
    severity_enum = None
    if severity:
        try:
            severity_enum = IncidentSeverity(severity.lower())
        except ValueError:
            console.print(f"[red]Invalid severity: {severity}[/red]")
            return
    
    incidents = manager.list_incidents(status=status_enum, severity=severity_enum)
    
    if not incidents:
        console.print("[yellow]No incidents found.[/yellow]")
        return
    
    table = Table(title=f"Incidents ({len(incidents)})")
    table.add_column("ID", style="cyan")
    table.add_column("Title", style="white")
    table.add_column("Severity", style="yellow")
    table.add_column("Status", style="green")
    table.add_column("Timeline", style="magenta")
    table.add_column("Detected", style="dim")
    
    for incident in incidents:
        timeline = manager.track_reporting_timeline(incident)
        severity_str = incident.severity.value if incident.severity else "Unclassified"
        status_str = incident.status.value
        
        # Color code timeline status
        timeline_color = {
            "reported": "green",
            "on_track": "green",
            "warning": "yellow",
            "urgent": "red",
            "overdue": "bold red",
            "partial": "yellow"
        }.get(timeline['status'], "white")
        
        timeline_str = f"[{timeline_color}]{timeline['message']}[/{timeline_color}]"
        
        table.add_row(
            incident.id,
            incident.title[:40] + "..." if len(incident.title) > 40 else incident.title,
            severity_str,
            status_str,
            timeline_str,
            incident.detected_at.strftime('%Y-%m-%d %H:%M')
        )
    
    console.print(table)

def cmd_show(manager: IncidentManager, incident_id: str):
    """Show detailed incident information"""
    incident = manager.load_incident(incident_id)
    if not incident:
        console.print(f"[red]Incident not found: {incident_id}[/red]")
        return
    
    manager.display_incident(incident)
    
    # Additional details
    if incident.investigation_notes:
        console.print(Panel(
            "\n".join(f"• {note}" for note in incident.investigation_notes),
            title="Investigation Notes",
            border_style="blue"
        ))
    
    if incident.corrective_actions:
        console.print(Panel(
            "\n".join(f"• {action}" for action in incident.corrective_actions),
            title="Corrective Actions",
            border_style="green"
        ))
    
    if incident.risk_assessment:
        console.print(Panel(
            incident.risk_assessment,
            title="Risk Assessment",
            border_style="red"
        ))

def cmd_create(manager: IncidentManager):
    """Create a new incident interactively"""
    console.print("\n[bold cyan]Create New Incident[/bold cyan]\n")
    
    title = Prompt.ask("Incident Title")
    description = Prompt.ask("Description", multiline=True)
    ai_system_id = Prompt.ask("AI System ID")
    ai_system_name = Prompt.ask("AI System Name")
    member_state = Prompt.ask("Member State (EU)", default="Germany")
    detected_by = Prompt.ask("Detected By", choices=["automated", "human"], default="automated")
    
    incident = manager.create_incident(
        title=title,
        description=description,
        ai_system_id=ai_system_id,
        ai_system_name=ai_system_name,
        member_state=member_state,
        detected_by=detected_by
    )
    
    console.print(f"\n[green]✓ Incident created: {incident.id}[/green]")
    
    # Auto-classify if AI available
    if manager.use_ai:
        console.print("[dim]Classifying severity...[/dim]")
        severity, incident_type, reporting_days = manager.classify_severity(incident)
        if severity:
            console.print(f"[green]✓ Classified as {severity.value}[/green]")
            if incident.is_serious:
                console.print(f"[yellow]⚠️ Serious incident - {reporting_days} days reporting deadline[/yellow]")
    
    manager.display_incident(incident)
    
    # Ask about causal link
    if Confirm.ask("\nEstablish causal link now?"):
        established = Confirm.ask("Causal link established between AI system and incident?")
        notes = Prompt.ask("Notes (optional)", default="")
        manager.establish_causal_link(incident, established=established, notes=notes)
        console.print("[green]✓ Causal link recorded[/green]")

def cmd_classify(manager: IncidentManager, incident_id: str):
    """Re-classify an incident"""
    incident = manager.load_incident(incident_id)
    if not incident:
        console.print(f"[red]Incident not found: {incident_id}[/red]")
        return
    
    console.print(f"[dim]Classifying incident {incident_id}...[/dim]")
    severity, incident_type, reporting_days = manager.classify_severity(incident)
    
    if severity:
        console.print(f"[green]✓ Classified as {severity.value}[/green]")
        if incident_type:
            console.print(f"[green]✓ Type: {incident_type.value}[/green]")
        console.print(f"[green]✓ Reporting deadline: {reporting_days} days[/green]")
        manager.display_incident(incident)
    else:
        console.print("[yellow]Classification requires manual review[/yellow]")

def cmd_remediate(manager: IncidentManager, incident_id: str):
    """Get remediation suggestions and add actions"""
    incident = manager.load_incident(incident_id)
    if not incident:
        console.print(f"[red]Incident not found: {incident_id}[/red]")
        return
    
    console.print(f"\n[bold cyan]Remediation for {incident.id}[/bold cyan]\n")
    
    if manager.use_ai:
        console.print("[dim]Generating AI suggestions...[/dim]")
        suggestions = manager.suggest_remediation(incident)
        
        console.print(Panel(
            "\n".join(f"{i+1}. {suggestion}" for i, suggestion in enumerate(suggestions)),
            title="AI-Suggested Remediation Actions",
            border_style="yellow"
        ))
        
        if Confirm.ask("\nAdd suggested actions?"):
            for suggestion in suggestions:
                manager.add_remediation_action(incident, suggestion, ai_suggested=True)
            console.print("[green]✓ Remediation actions added[/green]")
    
    # Manual action
    if Confirm.ask("\nAdd manual remediation action?"):
        action = Prompt.ask("Action description")
        manager.add_remediation_action(incident, action, ai_suggested=False)
        console.print("[green]✓ Action added[/green]")

def cmd_timeline(manager: IncidentManager, incident_id: str):
    """Show reporting timeline status"""
    incident = manager.load_incident(incident_id)
    if not incident:
        console.print(f"[red]Incident not found: {incident_id}[/red]")
        return
    
    timeline = manager.track_reporting_timeline(incident)
    
    table = Table(title="Reporting Timeline")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="white")
    
    table.add_row("Status", timeline['status'])
    table.add_row("Message", timeline['message'])
    if timeline.get('days_remaining') is not None:
        table.add_row("Days Remaining", str(timeline['days_remaining']))
        table.add_row("Hours Remaining", f"{timeline['hours_remaining']:.1f}")
    if timeline.get('deadline'):
        table.add_row("Deadline", timeline['deadline'])
    if timeline.get('timeline_days'):
        table.add_row("Reporting Timeline", f"{timeline['timeline_days']} days")
    
    console.print(table)
    
    # Show key dates
    console.print("\n[bold]Key Dates:[/bold]")
    console.print(f"  Detected: {incident.detected_at.strftime('%Y-%m-%d %H:%M')}")
    if incident.causal_link_established_at:
        console.print(f"  Causal Link: {incident.causal_link_established_at.strftime('%Y-%m-%d %H:%M')}")
    if incident.reporting_deadline:
        console.print(f"  Deadline: {incident.reporting_deadline.strftime('%Y-%m-%d %H:%M')}")
    if incident.complete_report_submitted_at:
        console.print(f"  Report Submitted: {incident.complete_report_submitted_at.strftime('%Y-%m-%d %H:%M')}")

def cmd_report(manager: IncidentManager, incident_id: str):
    """Submit incident report"""
    incident = manager.load_incident(incident_id)
    if not incident:
        console.print(f"[red]Incident not found: {incident_id}[/red]")
        return
    
    if not incident.is_serious:
        console.print("[yellow]This incident is not classified as serious. Reporting not required.[/yellow]")
        if not Confirm.ask("Submit report anyway?"):
            return
    
    console.print(f"\n[bold cyan]Submit Report for {incident.id}[/bold cyan]\n")
    
    report_type = Prompt.ask("Report Type", choices=["initial", "complete"], default="complete")
    report_content = Prompt.ask("Report Content", multiline=True)
    
    if report_type == "initial":
        manager.submit_initial_report(incident, report_content)
        console.print("[green]✓ Initial report submitted[/green]")
    else:
        manager.submit_complete_report(incident, report_content)
        console.print("[green]✓ Complete report submitted[/green]")
    
    # Ask about authority notification
    if Confirm.ask("\nNotify market surveillance authority?"):
        authority_contact = Prompt.ask("Authority Contact (email/phone)")
        notification_content = Prompt.ask("Notification Content", multiline=True)
        manager.notify_authority(incident, authority_contact, notification_content)
        console.print("[green]✓ Authority notified[/green]")

def interactive_mode(manager: IncidentManager):
    """Run interactive mode"""
    print_header()
    
    while True:
        console.print("\n[bold cyan]Commands:[/bold cyan]")
        console.print("  [dim]list[/dim]          - List all incidents")
        console.print("  [dim]show <id>[/dim]     - Show incident details")
        console.print("  [dim]create[/dim]         - Create new incident")
        console.print("  [dim]classify <id>[/dim] - Classify incident severity")
        console.print("  [dim]remediate <id>[/dim] - Get remediation suggestions")
        console.print("  [dim]timeline <id>[/dim] - Show reporting timeline")
        console.print("  [dim]report <id>[/dim]   - Submit incident report")
        console.print("  [dim]exit[/dim]          - Exit\n")
        
        try:
            cmd_input = Prompt.ask("[bold green]Command[/bold green]").strip().split()
            if not cmd_input:
                continue
            
            cmd = cmd_input[0].lower()
            
            if cmd == "exit" or cmd == "quit" or cmd == "q":
                break
            elif cmd == "list":
                cmd_list(manager)
            elif cmd == "show" and len(cmd_input) > 1:
                cmd_show(manager, cmd_input[1])
            elif cmd == "create":
                cmd_create(manager)
            elif cmd == "classify" and len(cmd_input) > 1:
                cmd_classify(manager, cmd_input[1])
            elif cmd == "remediate" and len(cmd_input) > 1:
                cmd_remediate(manager, cmd_input[1])
            elif cmd == "timeline" and len(cmd_input) > 1:
                cmd_timeline(manager, cmd_input[1])
            elif cmd == "report" and len(cmd_input) > 1:
                cmd_report(manager, cmd_input[1])
            else:
                console.print("[red]Invalid command. Type 'exit' to quit.[/red]")
        except KeyboardInterrupt:
            console.print("\n[yellow]Exiting...[/yellow]")
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        # Command-line mode
        manager = IncidentManager()
        cmd = sys.argv[1].lower()
        
        if cmd == "list":
            status = sys.argv[2] if len(sys.argv) > 2 else None
            severity = sys.argv[3] if len(sys.argv) > 3 else None
            cmd_list(manager, status, severity)
        elif cmd == "show" and len(sys.argv) > 2:
            cmd_show(manager, sys.argv[2])
        elif cmd == "create":
            if len(sys.argv) < 7:
                console.print("[red]Usage: python incident_cli.py create \"Title\" \"Description\" \"AI-SYS-001\" \"System Name\" \"Germany\"[/red]")
                return
            incident = manager.create_incident(
                title=sys.argv[2],
                description=sys.argv[3],
                ai_system_id=sys.argv[4],
                ai_system_name=sys.argv[5],
                member_state=sys.argv[6]
            )
            console.print(f"[green]Created: {incident.id}[/green]")
            manager.display_incident(incident)
        elif cmd == "classify" and len(sys.argv) > 2:
            cmd_classify(manager, sys.argv[2])
        elif cmd == "timeline" and len(sys.argv) > 2:
            cmd_timeline(manager, sys.argv[2])
        else:
            console.print("[red]Invalid command. Use 'python incident_cli.py' for interactive mode.[/red]")
    else:
        # Interactive mode
        manager = IncidentManager()
        interactive_mode(manager)

if __name__ == "__main__":
    main()
