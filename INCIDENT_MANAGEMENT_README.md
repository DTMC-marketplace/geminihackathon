# EU AI Act Article 73 - Incident Management System

## Overview

Comprehensive incident management system for high-risk AI systems to ensure compliance with **EU AI Act Article 73 - Reporting of serious incidents**. The system provides:

- **Incident Detection**: Automated and manual incident detection
- **Severity Classification**: AI-assisted classification according to Article 3(49) definitions
- **Timeline Tracking**: Automatic calculation and tracking of 2/10/15 day reporting deadlines
- **Remediation Workflow**: AI-suggested remediation actions with human approval
- **Regulatory Notification**: Tracking of market surveillance authority notifications
- **Investigation & Risk Assessment**: Support for Article 73(6) requirements

## EU AI Act Article 73 Requirements

### Reporting Timelines

According to Article 73, serious incidents must be reported within:

- **2 days**: Serious and irreversible disruption of critical infrastructure (Article 73(3))
- **10 days**: Death of a person (Article 73(4))
- **15 days**: Other serious incidents (Article 73(2))

### Serious Incident Types (Article 3(49))

- **(a)**: Death of a person, or serious harm to a person's health → 10 days
- **(b)**: Serious and irreversible disruption of critical infrastructure → 2 days
- **(c)**: Infringement of obligations under Union law protecting fundamental rights → 15 days
- **(d)**: Serious harm to property or the environment → 15 days

### Key Obligations

1. **Immediate Reporting** (Article 73(2)): Report immediately after establishing causal link, but not later than deadline
2. **Causal Link** (Article 73(2)): Must establish causal link between AI system and incident
3. **Initial Report** (Article 73(5)): May submit incomplete initial report if needed
4. **Investigation** (Article 73(6)): Must perform risk assessment and corrective action
5. **Authority Notification** (Article 73(1)): Notify market surveillance authority in Member State where incident occurred

## Installation

```bash
# Install dependencies
pip install google-genai rich

# Set API key (optional, for AI features)
export GEMINI_API_KEY="your-api-key-here"
```

## Usage

### Command Line Interface

#### Create an Incident

```bash
python incident_cli.py create \
  --title "AI System Produced Harmful Medical Advice" \
  --description "The AI system provided incorrect dosage recommendations..." \
  --ai-system-id "MED-AI-001" \
  --ai-system-name "Medical Diagnosis Assistant v2.0" \
  --member-state "Germany" \
  --detected-by "automated"
```

#### Classify Incident Severity

```bash
# AI-assisted classification
python incident_cli.py classify INC-20260117-102838-0

# Human override
python incident_cli.py classify INC-20260117-102838-0 --override a
```

#### Establish Causal Link

```bash
python incident_cli.py causal-link INC-20260117-102838-0 \
  --established \
  --evidence "Root cause analysis confirms AI model error in dosage calculation"
```

#### Check Reporting Timeline

```bash
python incident_cli.py timeline INC-20260117-102838-0
```

#### Suggest Remediation Actions

```bash
python incident_cli.py suggest-remediation INC-20260117-102838-0
```

#### Notify Authority

```bash
python incident_cli.py notify-authority INC-20260117-102838-0 \
  --authority-contact "market-surveillance@authority.de" \
  --notification-content "Serious incident report submitted"
```

#### Submit Report

```bash
# Initial report (incomplete)
python incident_cli.py submit-report INC-20260117-102838-0 \
  --type initial \
  --content "Initial report pending full investigation"

# Complete report
python incident_cli.py submit-report INC-20260117-102838-0 \
  --type complete \
  --content "Complete incident report with full details"
```

#### Record Risk Assessment

```bash
python incident_cli.py risk-assessment INC-20260117-102838-0 \
  --assessment "High risk of patient harm. Immediate containment required."
```

#### List Incidents

```bash
# List all incidents
python incident_cli.py list

# Filter by status
python incident_cli.py list --status remediating
```

#### Show Incident Details

```bash
python incident_cli.py show INC-20260117-102838-0
```

### Python API

```python
from incident_management import IncidentManager, Incident

# Initialize manager
manager = IncidentManager(use_ai=True)

# Create incident
incident = manager.create_incident(
    title="AI System Error",
    description="Detailed description...",
    ai_system_id="AI-001",
    ai_system_name="Medical AI System",
    member_state="Germany",
    detected_by="automated"
)

# Classify severity (AI-assisted)
incident = manager.classify_severity(incident)

# Establish causal link
incident = manager.establish_causal_link(
    incident,
    established=True,
    evidence="Evidence of causal link..."
)

# Track timeline
timeline = manager.track_reporting_timeline(incident)
print(f"Days remaining: {timeline['days_remaining']}")

# Suggest remediation
suggestions = manager.suggest_remediation(incident)

# Notify authority
incident = manager.notify_authority(
    incident,
    authority_contact="authority@example.com",
    notification_content="Incident report"
)

# Submit report
incident = manager.submit_report(
    incident,
    report_type="complete",
    report_content="Full report details"
)

# Risk assessment
incident = manager.perform_risk_assessment(
    incident,
    assessment="Risk assessment details..."
)
```

## Workflow

### Phase 1: Incident Detection
1. Incident detected (automated or manual)
2. Create incident record using `create_incident()`
3. System records detection time and method

### Phase 2: Severity Classification
1. Use `classify_severity()` for AI-assisted classification
2. **Human review required** for serious incidents
3. System calculates reporting deadline based on type
4. Timeline tracking begins

### Phase 3: Causal Link Establishment
1. Investigate incident to determine AI system causality
2. Use `establish_causal_link()` to record determination
3. Timeline recalculated from causal link establishment

### Phase 4: Remediation Planning
1. Use `suggest_remediation()` for AI-generated suggestions
2. **Human approval required** before implementation
3. Track remediation actions and status

### Phase 5: Reporting
1. Monitor timeline using `track_reporting_timeline()`
2. Submit initial report if needed (Article 73(5))
3. Submit complete report before deadline
4. Use `notify_authority()` to record notification

### Phase 6: Investigation
1. Perform risk assessment using `perform_risk_assessment()`
2. Document investigation findings
3. Implement corrective actions
4. Cooperate with authorities

### Phase 7: Resolution
1. Verify all remediation completed
2. Document resolution
3. Close incident
4. Conduct post-incident review

## AI-Assisted Automation

The system uses AI for:
- **Incident Classification**: Analyzing incidents against Article 3(49) definitions
- **Remediation Suggestions**: Generating action recommendations

**Human judgment is ALWAYS required for:**
- Serious incident confirmation
- Causal link establishment
- Remediation approval
- Report submission authorization
- Authority communications

## Data Storage

Incidents are stored as JSON files in the `incidents/` directory:
- Format: `{incident_id}.json`
- Structure: Full incident record with all fields
- Persistence: All changes are automatically saved

## Compliance Checklist

- [ ] Incident detected and recorded immediately
- [ ] Severity classified according to Article 3(49) within 1 hour
- [ ] Causal link established and documented
- [ ] Reporting deadline calculated correctly (2/10/15 days)
- [ ] Timeline tracking active with alerts for approaching deadlines
- [ ] Initial report submitted if needed (Article 73(5))
- [ ] Complete report submitted before deadline
- [ ] Market surveillance authority notified (Article 73(1))
- [ ] Investigation and risk assessment completed (Article 73(6))
- [ ] Corrective actions implemented and documented
- [ ] Evidence preserved for audit (no system alterations before authority notification)

## Integration

The system integrates with:
- `ai_act_cli.py`: Query EU AI Act for compliance guidance
- `query_ai_act.py`: Semantic search for relevant articles
- Incident responder skill package: Workflow automation

## References

- **EU AI Act Article 73**: Reporting of serious incidents
- **EU AI Act Article 3(49)**: Definition of serious incident
- **Regulation (EU) 2024/1689**: Full text available in `articles/` directory

## Support

For questions or issues:
1. Review EU AI Act Article 73 requirements
2. Check incident management documentation
3. Consult legal counsel for compliance decisions

**Important**: This system assists with compliance but does not constitute legal advice. Always consult qualified legal counsel for compliance decisions.
