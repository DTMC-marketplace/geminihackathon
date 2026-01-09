# Tier 1: Rapid Ethics Screen

Quick assessment for low-risk systems or initial evaluation. Complete in 15-30 minutes.

## Risk Classification Checklist

### Critical Risk Indicators (Any = escalate to Tier 2)
- [ ] Affects employment, lending, housing, healthcare, criminal justice, or education
- [ ] Involves vulnerable populations (children, elderly, disabled, economically disadvantaged)
- [ ] Uses biometric data (facial recognition, fingerprints, voice)
- [ ] Makes automated decisions without human review
- [ ] Affects >10,000 people
- [ ] Operates in heavily regulated domain

### High Risk Indicators (2+ = consider Tier 2)
- [ ] Uses demographic data as features
- [ ] Training data from historical human decisions
- [ ] Outputs affect access to resources or opportunities
- [ ] Operates with limited transparency
- [ ] No established feedback mechanism
- [ ] Novel application without precedent

## Quick Assessment Questions

### 1. Purpose & Context
- What problem does this solve?
- Who benefits? Who might be harmed?
- What happens if the system is wrong?

### 2. Data & Training
- What data trains the model?
- Could historical bias be present?
- Are all relevant groups represented?

### 3. Fairness Indicators
- Could outputs differ by demographic group?
- Is there a fairness definition in use?
- How are edge cases handled?

### 4. Human Oversight
- Can humans override decisions?
- Is there an appeals process?
- Who monitors for problems?

### 5. Transparency
- Can decisions be explained?
- Do affected people know AI is involved?
- Is there documentation?

## Red Flags Requiring Escalation

| Red Flag | Action |
|----------|--------|
| No fairness testing | Escalate + recommend testing |
| Protected attributes as features | Escalate immediately |
| No human oversight for high-stakes | Escalate + flag governance gap |
| Unexplainable decisions | Escalate + XAI requirement |
| Affected communities not consulted | Escalate + stakeholder analysis |
| No incident response plan | Escalate + deployment safeguards |

## Quick Recommendations Template

```markdown
## Rapid Ethics Screen Results

**System**: [Name]
**Date**: [Date]
**Reviewer**: [Name]

### Risk Level: [Low/Medium/High/Critical]

### Key Findings
1. [Finding 1]
2. [Finding 2]
3. [Finding 3]

### Immediate Actions Required
- [ ] [Action 1]
- [ ] [Action 2]

### Recommended Next Steps
- [ ] [Step 1]
- [ ] [Step 2]

### Escalation Needed: [Yes/No]
If yes, recommend: [Tier 2 modules to load]
```

## Escalation Guidance

| Risk Level | Recommendation |
|------------|----------------|
| Low | Document and proceed with monitoring |
| Medium | Tier 2 focused assessment (2-3 modules) |
| High | Full Tier 2 assessment |
| Critical | Full Tier 2 + regulatory review + leadership briefing |
