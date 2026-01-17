#!/usr/bin/env python3
"""
EU AI Act Article 73 - Serious Incident Management System
==========================================================
Comprehensive incident detection, classification, timeline tracking, 
remediation workflow, and regulatory notification system for EU AI Act compliance.

EU AI Act Article 73 Requirements:
- Incident detection and classification
- 15-day reporting timeline tracking (with exceptions: 2 days for critical infrastructure, 10 days for death)
- Remediation workflow
- Regulatory notification to market surveillance authorities
- AI-assisted automation with human judgment for serious incidents

Usage:
    from incident_management import IncidentManager
    manager = IncidentManager()
    incident = manager.create_incident(...)
    manager.classify_severity(incident)
    manager.track_reporting_timeline(incident)
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass, asdict, field
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Warning: 'google-genai' package not found. AI features will be limited.")
    genai = None

# Configuration
BASE_DIR = Path(__file__).resolve().parent
INCIDENTS_DIR = BASE_DIR / "incidents"
INCIDENTS_DIR.mkdir(exist_ok=True)

# EU AI Act Article 3, point (49) - Serious Incident Definition
class SeriousIncidentType(Enum):
    """Serious incident types as defined in EU AI Act Article 3(49)"""
    DEATH_OR_SERIOUS_HARM = "a"  # Article 3(49)(a)
    CRITICAL_INFRASTRUCTURE_DISRUPTION = "b"  # Article 3(49)(b)
    FUNDAMENTAL_RIGHTS_INFRINGEMENT = "c"  # Article 3(49)(c)
    PROPERTY_ENVIRONMENT_HARM = "d"  # Article 3(49)(d)

class IncidentSeverity(Enum):
    """Incident severity classification"""
    CRITICAL = "critical"  # Death or critical infrastructure - 2-10 days reporting
    HIGH = "high"  # Serious harm or fundamental rights - 15 days reporting
    MEDIUM = "medium"  # Property/environment harm - 15 days reporting
    LOW = "low"  # Non-serious incidents - monitoring only

class IncidentStatus(Enum):
    """Incident workflow status"""
    DETECTED = "detected"
    CLASSIFIED = "classified"
    INVESTIGATING = "investigating"
    REMEDIATING = "remediating"
    REPORTED = "reported"
    RESOLVED = "resolved"
    CLOSED = "closed"

@dataclass
class Incident:
    """Incident data structure for EU AI Act Article 73 compliance"""
    id: str
    title: str
    description: str
    detected_at: datetime
    detected_by: str  # "automated" or "human" or user identifier
    ai_system_id: str
    ai_system_name: str
    member_state: str  # EU member state where incident occurred
    
    # Classification
    severity: Optional[IncidentSeverity] = None
    incident_type: Optional[SeriousIncidentType] = None
    is_serious: bool = False
    causal_link_established: bool = False
    causal_link_established_at: Optional[datetime] = None
    
    # Timeline tracking (Article 73)
    reporting_deadline: Optional[datetime] = None
    reporting_timeline_days: Optional[int] = None  # 2, 10, or 15 days
    initial_report_submitted: bool = False
    initial_report_submitted_at: Optional[datetime] = None
    complete_report_submitted: bool = False
    complete_report_submitted_at: Optional[datetime] = None
    
    # Status
    status: IncidentStatus = IncidentStatus.DETECTED
    
    # Remediation
    remediation_actions: List[str] = field(default_factory=list)
    remediation_status: str = "pending"
    corrective_actions: List[str] = field(default_factory=list)
    
    # Regulatory
    authority_notified: bool = False
    authority_notified_at: Optional[datetime] = None
    authority_contact: Optional[str] = None
    
    # Investigation
    investigation_notes: List[str] = field(default_factory=list)
    risk_assessment: Optional[str] = None
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict = field(default_factory=dict)

class IncidentManager:
    """Manages incident detection, classification, tracking, and reporting for EU AI Act Article 73"""
    
    def __init__(self, use_ai: bool = True):
        self.console = Console()
        self.incidents_dir = INCIDENTS_DIR
        self.use_ai = use_ai and genai is not None
        self.client = None
        
        if self.use_ai:
            api_key = os.environ.get("GEMINI_API_KEY")
            if api_key:
                try:
                    self.client = genai.Client(api_key=api_key)
                except Exception as e:
                    self.console.print(f"[yellow]Warning: Could not initialize AI client: {e}[/yellow]")
                    self.use_ai = False
    
    def create_incident(
        self,
        title: str,
        description: str,
        ai_system_id: str,
        ai_system_name: str,
        member_state: str,
        detected_by: str = "automated",
        metadata: Optional[Dict] = None
    ) -> Incident:
        """Create a new incident record"""
        incident_id = f"INC-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{len(list(self.incidents_dir.glob('*.json')))}"
        
        incident = Incident(
            id=incident_id,
            title=title,
            description=description,
            detected_at=datetime.now(),
            detected_by=detected_by,
            ai_system_id=ai_system_id,
            ai_system_name=ai_system_name,
            member_state=member_state,
            metadata=metadata or {}
        )
        
        # Auto-classify if AI is available
        if self.use_ai:
            self.classify_severity(incident)
        
        self.save_incident(incident)
        return incident
    
    def classify_severity(self, incident: Incident) -> Tuple[IncidentSeverity, SeriousIncidentType, int]:
        """
        Classify incident severity and determine reporting timeline.
        Uses AI if available, otherwise requires manual classification.
        
        Returns: (severity, incident_type, reporting_days)
        """
        if self.use_ai and self.client:
            # AI-assisted classification
            classification = self._ai_classify_incident(incident)
            incident.severity = classification['severity']
            incident.incident_type = classification['incident_type']
            incident.is_serious = classification['is_serious']
        else:
            # Manual classification required
            self.console.print("[yellow]AI classification not available. Manual classification required.[/yellow]")
            return None, None, None
        
        # Determine reporting timeline based on Article 73
        reporting_days = self._calculate_reporting_timeline(incident)
        incident.reporting_timeline_days = reporting_days
        
        # Calculate deadline (starts when causal link is established)
        if incident.causal_link_established and incident.causal_link_established_at:
            incident.reporting_deadline = incident.causal_link_established_at + timedelta(days=reporting_days)
        else:
            # Default: deadline is from detection + reporting days
            incident.reporting_deadline = incident.detected_at + timedelta(days=reporting_days)
        
        incident.status = IncidentStatus.CLASSIFIED
        incident.updated_at = datetime.now()
        self.save_incident(incident)
        
        return incident.severity, incident.incident_type, reporting_days
    
    def _ai_classify_incident(self, incident: Incident) -> Dict:
        """Use AI to classify incident severity and type"""
        prompt = f"""You are an expert on EU AI Act Article 73 compliance. Classify the following incident according to Article 3, point (49) definitions.

Incident Title: {incident.title}
Incident Description: {incident.description}
AI System: {incident.ai_system_name}
Member State: {incident.member_state}

EU AI Act Article 3(49) - Serious Incident Definition:
(a) Death of a person, or serious harm to a person's health
(b) Serious and irreversible disruption of the management or operation of critical infrastructure
(c) Infringement of obligations under Union law intended to protect fundamental rights
(d) Serious harm to property or the environment

Article 73 Reporting Timelines:
- Standard serious incident: 15 days maximum
- Widespread infringement or critical infrastructure disruption (type b): 2 days maximum
- Death (type a): 10 days maximum

Classify this incident and return JSON with:
- "severity": "critical", "high", "medium", or "low"
- "incident_type": "a", "b", "c", "d", or null if not serious
- "is_serious": true or false
- "reasoning": brief explanation

Return only valid JSON, no markdown formatting."""

        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0.1)
            )
            
            # Parse JSON response
            response_text = response.text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            classification = json.loads(response_text)
            
            # Convert to enums
            severity_map = {
                "critical": IncidentSeverity.CRITICAL,
                "high": IncidentSeverity.HIGH,
                "medium": IncidentSeverity.MEDIUM,
                "low": IncidentSeverity.LOW
            }
            
            type_map = {
                "a": SeriousIncidentType.DEATH_OR_SERIOUS_HARM,
                "b": SeriousIncidentType.CRITICAL_INFRASTRUCTURE_DISRUPTION,
                "c": SeriousIncidentType.FUNDAMENTAL_RIGHTS_INFRINGEMENT,
                "d": SeriousIncidentType.PROPERTY_ENVIRONMENT_HARM
            }
            
            return {
                "severity": severity_map.get(classification.get("severity", "medium"), IncidentSeverity.MEDIUM),
                "incident_type": type_map.get(classification.get("incident_type")) if classification.get("incident_type") else None,
                "is_serious": classification.get("is_serious", False),
                "reasoning": classification.get("reasoning", "")
            }
        except Exception as e:
            self.console.print(f"[red]AI classification error: {e}[/red]")
            # Fallback to manual classification
            return {
                "severity": IncidentSeverity.MEDIUM,
                "incident_type": None,
                "is_serious": False,
                "reasoning": "AI classification failed, manual review required"
            }
    
    def _calculate_reporting_timeline(self, incident: Incident) -> int:
        """Calculate reporting timeline in days based on Article 73"""
        if not incident.is_serious:
            return 0  # No reporting required
        
        if incident.incident_type == SeriousIncidentType.CRITICAL_INFRASTRUCTURE_DISRUPTION:
            # Article 73(3): 2 days for critical infrastructure
            return 2
        elif incident.incident_type == SeriousIncidentType.DEATH_OR_SERIOUS_HARM:
            # Article 73(4): 10 days for death
            return 10
        else:
            # Article 73(2): 15 days for other serious incidents
            return 15
    
    def establish_causal_link(self, incident: Incident, established: bool = True, notes: str = "") -> None:
        """Establish causal link between AI system and incident (Article 73(2))"""
        incident.causal_link_established = established
        incident.causal_link_established_at = datetime.now()
        
        if notes:
            incident.investigation_notes.append(f"Causal link established: {notes}")
        
        # Recalculate deadline from causal link establishment
        if established and incident.reporting_timeline_days:
            incident.reporting_deadline = incident.causal_link_established_at + timedelta(days=incident.reporting_timeline_days)
        
        incident.status = IncidentStatus.INVESTIGATING
        incident.updated_at = datetime.now()
        self.save_incident(incident)
    
    def suggest_remediation(self, incident: Incident) -> List[str]:
        """AI-suggested remediation actions"""
        if not self.use_ai or not self.client:
            return ["Manual remediation review required"]
        
        prompt = f"""You are an expert on EU AI Act compliance and incident remediation. Suggest remediation actions for this incident.

Incident: {incident.title}
Description: {incident.description}
Severity: {incident.severity.value if incident.severity else 'unknown'}
Type: {incident.incident_type.value if incident.incident_type else 'unknown'}
AI System: {incident.ai_system_name}

Provide a JSON array of remediation action suggestions. Each action should be specific and actionable.
Return only valid JSON array, no markdown formatting."""

        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0.2)
            )
            
            response_text = response.text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            actions = json.loads(response_text)
            return actions if isinstance(actions, list) else [str(actions)]
        except Exception as e:
            self.console.print(f"[yellow]AI remediation suggestion error: {e}[/yellow]")
            return [
                "Conduct root cause analysis",
                "Implement immediate containment measures",
                "Review and update risk management system (Article 9)",
                "Update technical documentation",
                "Notify affected users if required"
            ]
    
    def add_remediation_action(self, incident: Incident, action: str, ai_suggested: bool = False) -> None:
        """Add a remediation action to the incident"""
        prefix = "[AI Suggested] " if ai_suggested else ""
        incident.remediation_actions.append(f"{prefix}{action}")
        incident.status = IncidentStatus.REMEDIATING
        incident.updated_at = datetime.now()
        self.save_incident(incident)
    
    def track_reporting_timeline(self, incident: Incident) -> Dict:
        """Track reporting timeline and return status"""
        now = datetime.now()
        
        if not incident.reporting_deadline:
            return {
                "status": "no_deadline",
                "message": "Reporting deadline not set. Classify incident first."
            }
        
        days_remaining = (incident.reporting_deadline - now).days
        hours_remaining = (incident.reporting_deadline - now).total_seconds() / 3600
        
        if incident.complete_report_submitted:
            status = "reported"
            message = f"Report submitted on {incident.complete_report_submitted_at.strftime('%Y-%m-%d %H:%M')}"
        elif incident.initial_report_submitted:
            status = "partial"
            message = f"Initial report submitted. Complete report pending. {days_remaining} days remaining."
        elif days_remaining < 0:
            status = "overdue"
            message = f"⚠️ OVERDUE: Reporting deadline passed {abs(days_remaining)} days ago!"
        elif days_remaining <= 1:
            status = "urgent"
            message = f"⚠️ URGENT: {hours_remaining:.1f} hours remaining until deadline"
        elif days_remaining <= 3:
            status = "warning"
            message = f"⚠️ WARNING: {days_remaining} days remaining until deadline"
        else:
            status = "on_track"
            message = f"✓ {days_remaining} days remaining until deadline"
        
        return {
            "status": status,
            "message": message,
            "days_remaining": days_remaining,
            "hours_remaining": hours_remaining,
            "deadline": incident.reporting_deadline.isoformat(),
            "timeline_days": incident.reporting_timeline_days
        }
    
    def submit_initial_report(self, incident: Incident, report_content: str) -> None:
        """Submit initial incomplete report (Article 73(5))"""
        incident.initial_report_submitted = True
        incident.initial_report_submitted_at = datetime.now()
        incident.status = IncidentStatus.REPORTED
        incident.investigation_notes.append(f"Initial report submitted: {report_content[:100]}...")
        incident.updated_at = datetime.now()
        self.save_incident(incident)
    
    def submit_complete_report(self, incident: Incident, report_content: str) -> None:
        """Submit complete incident report"""
        incident.complete_report_submitted = True
        incident.complete_report_submitted_at = datetime.now()
        incident.investigation_notes.append(f"Complete report submitted")
        incident.updated_at = datetime.now()
        self.save_incident(incident)
        
        # Save report content
        report_file = self.incidents_dir / f"{incident.id}_report.txt"
        report_file.write_text(report_content, encoding='utf-8')
    
    def notify_authority(self, incident: Incident, authority_contact: str, notification_content: str) -> None:
        """Notify market surveillance authority (Article 73(1))"""
        incident.authority_notified = True
        incident.authority_notified_at = datetime.now()
        incident.authority_contact = authority_contact
        incident.investigation_notes.append(f"Authority notified: {authority_contact}")
        incident.updated_at = datetime.now()
        self.save_incident(incident)
        
        # Save notification
        notification_file = self.incidents_dir / f"{incident.id}_authority_notification.txt"
        notification_file.write_text(notification_content, encoding='utf-8')
    
    def perform_investigation(self, incident: Incident, risk_assessment: str, corrective_actions: List[str]) -> None:
        """Perform investigation and risk assessment (Article 73(6))"""
        incident.risk_assessment = risk_assessment
        incident.corrective_actions = corrective_actions
        incident.investigation_notes.append(f"Investigation completed: {risk_assessment[:100]}...")
        incident.updated_at = datetime.now()
        self.save_incident(incident)
    
    def resolve_incident(self, incident: Incident, resolution_notes: str) -> None:
        """Mark incident as resolved"""
        incident.status = IncidentStatus.RESOLVED
        incident.remediation_status = "completed"
        incident.investigation_notes.append(f"Resolved: {resolution_notes}")
        incident.updated_at = datetime.now()
        self.save_incident(incident)
    
    def save_incident(self, incident: Incident) -> None:
        """Save incident to JSON file"""
        incident_file = self.incidents_dir / f"{incident.id}.json"
        
        # Convert to dict, handling datetime and enum serialization
        incident_dict = asdict(incident)
        incident_dict['detected_at'] = incident.detected_at.isoformat()
        incident_dict['created_at'] = incident.created_at.isoformat()
        incident_dict['updated_at'] = incident.updated_at.isoformat()
        
        if incident.causal_link_established_at:
            incident_dict['causal_link_established_at'] = incident.causal_link_established_at.isoformat()
        if incident.reporting_deadline:
            incident_dict['reporting_deadline'] = incident.reporting_deadline.isoformat()
        if incident.initial_report_submitted_at:
            incident_dict['initial_report_submitted_at'] = incident.initial_report_submitted_at.isoformat()
        if incident.complete_report_submitted_at:
            incident_dict['complete_report_submitted_at'] = incident.complete_report_submitted_at.isoformat()
        if incident.authority_notified_at:
            incident_dict['authority_notified_at'] = incident.authority_notified_at.isoformat()
        
        if incident.severity:
            incident_dict['severity'] = incident.severity.value
        if incident.incident_type:
            incident_dict['incident_type'] = incident.incident_type.value
        incident_dict['status'] = incident.status.value
        
        incident_file.write_text(json.dumps(incident_dict, indent=2), encoding='utf-8')
    
    def load_incident(self, incident_id: str) -> Optional[Incident]:
        """Load incident from JSON file"""
        incident_file = self.incidents_dir / f"{incident_id}.json"
        if not incident_file.exists():
            return None
        
        incident_dict = json.loads(incident_file.read_text(encoding='utf-8'))
        
        # Reconstruct Incident object
        incident_dict['detected_at'] = datetime.fromisoformat(incident_dict['detected_at'])
        incident_dict['created_at'] = datetime.fromisoformat(incident_dict['created_at'])
        incident_dict['updated_at'] = datetime.fromisoformat(incident_dict['updated_at'])
        
        if incident_dict.get('causal_link_established_at'):
            incident_dict['causal_link_established_at'] = datetime.fromisoformat(incident_dict['causal_link_established_at'])
        if incident_dict.get('reporting_deadline'):
            incident_dict['reporting_deadline'] = datetime.fromisoformat(incident_dict['reporting_deadline'])
        if incident_dict.get('initial_report_submitted_at'):
            incident_dict['initial_report_submitted_at'] = datetime.fromisoformat(incident_dict['initial_report_submitted_at'])
        if incident_dict.get('complete_report_submitted_at'):
            incident_dict['complete_report_submitted_at'] = datetime.fromisoformat(incident_dict['complete_report_submitted_at'])
        if incident_dict.get('authority_notified_at'):
            incident_dict['authority_notified_at'] = datetime.fromisoformat(incident_dict['authority_notified_at'])
        
        if incident_dict.get('severity'):
            incident_dict['severity'] = IncidentSeverity(incident_dict['severity'])
        if incident_dict.get('incident_type'):
            incident_dict['incident_type'] = SeriousIncidentType(incident_dict['incident_type'])
        incident_dict['status'] = IncidentStatus(incident_dict['status'])
        
        return Incident(**incident_dict)
    
    def list_incidents(self, status: Optional[IncidentStatus] = None, severity: Optional[IncidentSeverity] = None) -> List[Incident]:
        """List all incidents, optionally filtered"""
        incidents = []
        for incident_file in self.incidents_dir.glob("*.json"):
            if incident_file.name.endswith("_report.json") or incident_file.name.endswith("_authority_notification.json"):
                continue
            try:
                incident = self.load_incident(incident_file.stem)
                if incident:
                    if status and incident.status != status:
                        continue
                    if severity and incident.severity != severity:
                        continue
                    incidents.append(incident)
            except Exception as e:
                self.console.print(f"[yellow]Error loading {incident_file}: {e}[/yellow]")
        
        return sorted(incidents, key=lambda x: x.detected_at, reverse=True)
    
    def display_incident(self, incident: Incident) -> None:
        """Display incident details using Rich"""
        timeline = self.track_reporting_timeline(incident)
        
        # Status panel
        status_color = {
            "reported": "green",
            "on_track": "green",
            "warning": "yellow",
            "urgent": "red",
            "overdue": "bold red",
            "partial": "yellow"
        }.get(timeline['status'], "white")
        
        self.console.print(Panel.fit(
            f"[bold]{incident.title}[/bold]\n\n"
            f"ID: {incident.id}\n"
            f"Status: {incident.status.value}\n"
            f"Severity: {incident.severity.value if incident.severity else 'Unclassified'}\n"
            f"Type: {incident.incident_type.value if incident.incident_type else 'N/A'}\n"
            f"Serious: {'Yes' if incident.is_serious else 'No'}\n\n"
            f"[{status_color}]{timeline['message']}[/{status_color}]\n\n"
            f"Detected: {incident.detected_at.strftime('%Y-%m-%d %H:%M')}\n"
            f"AI System: {incident.ai_system_name}\n"
            f"Member State: {incident.member_state}",
            title="Incident Details",
            border_style=status_color
        ))
        
        # Description
        self.console.print(Panel(incident.description, title="Description", border_style="cyan"))
        
        # Timeline table
        table = Table(title="Reporting Timeline")
        table.add_column("Event", style="cyan")
        table.add_column("Date/Time", style="green")
        table.add_column("Status", style="yellow")
        
        table.add_row("Detected", incident.detected_at.strftime('%Y-%m-%d %H:%M'), "✓")
        
        if incident.causal_link_established_at:
            table.add_row("Causal Link Established", incident.causal_link_established_at.strftime('%Y-%m-%d %H:%M'), "✓")
        
        if incident.reporting_deadline:
            table.add_row("Reporting Deadline", incident.reporting_deadline.strftime('%Y-%m-%d %H:%M'), 
                         "⚠️" if timeline['status'] in ['urgent', 'overdue'] else "✓")
        
        if incident.initial_report_submitted_at:
            table.add_row("Initial Report", incident.initial_report_submitted_at.strftime('%Y-%m-%d %H:%M'), "✓")
        
        if incident.complete_report_submitted_at:
            table.add_row("Complete Report", incident.complete_report_submitted_at.strftime('%Y-%m-%d %H:%M'), "✓")
        
        if incident.authority_notified_at:
            table.add_row("Authority Notified", incident.authority_notified_at.strftime('%Y-%m-%d %H:%M'), "✓")
        
        self.console.print(table)
        
        # Remediation actions
        if incident.remediation_actions:
            self.console.print(Panel(
                "\n".join(f"• {action}" for action in incident.remediation_actions),
                title="Remediation Actions",
                border_style="yellow"
            ))

if __name__ == "__main__":
    # Example usage
    console = Console()
    console.print("[bold cyan]EU AI Act Article 73 - Incident Management System[/bold cyan]\n")
    
    manager = IncidentManager()
    
    # Example: Create an incident
    incident = manager.create_incident(
        title="AI System Produced Harmful Medical Advice",
        description="The AI system provided incorrect dosage recommendations that could lead to patient harm.",
        ai_system_id="MED-AI-001",
        ai_system_name="Medical Diagnosis Assistant v2.0",
        member_state="Germany",
        detected_by="automated"
    )
    
    console.print(f"\n[green]Created incident: {incident.id}[/green]")
    manager.display_incident(incident)
