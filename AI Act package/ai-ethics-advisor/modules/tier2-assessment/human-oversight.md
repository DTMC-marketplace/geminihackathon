# Human Oversight Assessment

Evaluation of human control, override capabilities, and meaningful human agency.

## Levels of Automation

| Level | Description | Human Role | Appropriate For |
|-------|-------------|------------|-----------------|
| **0 - No automation** | Human does everything | Full control | Highest stakes |
| **1 - Decision support** | AI provides information | Makes decision | High stakes |
| **2 - Human-in-the-loop** | AI recommends, human approves | Approves each decision | Moderate-high stakes |
| **3 - Human-on-the-loop** | AI acts, human monitors | Monitors, can intervene | Moderate stakes |
| **4 - Human-out-of-loop** | AI acts autonomously | Post-hoc review only | Low stakes |
| **5 - Full automation** | No human involvement | None | Trivial decisions |

### Determining Appropriate Level
| Factor | Lower automation | Higher automation |
|--------|------------------|-------------------|
| Stakes | High (life, liberty) | Low (convenience) |
| Reversibility | Irreversible | Easily reversed |
| Uncertainty | High | Low, well-calibrated |
| Domain | Novel, changing | Stable, well-understood |
| Affected population | Vulnerable | General |

## Human-in-the-Loop Assessment

### Meaningful Human Review
Human oversight is only meaningful if humans:
- [ ] Have sufficient time to review
- [ ] Have necessary information and context
- [ ] Have relevant expertise
- [ ] Can actually override the system
- [ ] Face accountability for decisions
- [ ] Are not penalized for overrides

### Automation Bias Risks
| Risk Factor | Mitigation |
|-------------|------------|
| Over-reliance on AI | Training on AI limitations |
| Rubber-stamping | Random audits of approvals |
| Alert fatigue | Appropriate threshold setting |
| Time pressure | Adequate staffing and time |
| Skill degradation | Maintaining manual capabilities |

### Quality of Override
- Is override easy to execute?
- Are overrides tracked and analyzed?
- Is there a process for learning from overrides?
- Are overriders supported, not punished?

## Override Mechanisms

### Technical Requirements
- [ ] Override capability exists
- [ ] Override is accessible to appropriate roles
- [ ] Override is timely (before harm occurs)
- [ ] Override logging in place
- [ ] Override doesn't create new risks

### Organizational Requirements
- [ ] Clear authority to override
- [ ] Training on when to override
- [ ] Psychological safety to override
- [ ] Process for escalation
- [ ] Review of override patterns

## Human Agency Considerations

### For Affected Individuals
- Can they opt out of automated processing?
- Can they request human review?
- Are they informed that AI is involved?
- Can they understand and contest decisions?

### For Operators
- Can they understand system behavior?
- Can they identify when system is failing?
- Can they intervene effectively?
- Are they empowered to raise concerns?

## Emergency Protocols

### Kill Switch Requirements
- [ ] Ability to immediately halt system
- [ ] Clear authority to activate
- [ ] Communication plan
- [ ] Fallback procedures
- [ ] Recovery process

### Failure Mode Planning
| Failure Type | Detection | Response | Recovery |
|--------------|-----------|----------|----------|
| Model failure | | | |
| Data pipeline failure | | | |
| Bias incident | | | |
| Security breach | | | |

## Assessment Checklist

### Design Phase
- [ ] Automation level justified for stakes
- [ ] Human review points identified
- [ ] Override mechanisms designed
- [ ] Fallback procedures planned

### Implementation Phase
- [ ] Override functionality works
- [ ] Humans can access needed information
- [ ] Timing allows meaningful review
- [ ] Training provided

### Operations Phase
- [ ] Human review actually occurring
- [ ] Overrides being made when appropriate
- [ ] Override patterns analyzed
- [ ] No automation bias observed

## Output: Human Oversight Summary

```markdown
## Human Oversight Assessment

### Automation Level
- Current level: [0-5]
- Appropriate level: [0-5]
- Gap: [If any]

### Human Review
- [ ] Review points exist
- [ ] Review is meaningful
- [ ] Time adequate
- [ ] Expertise adequate
- [ ] Authority to override

### Override Capabilities
- [ ] Technical capability exists
- [ ] Organizational support exists
- [ ] Overrides tracked and analyzed

### Automation Bias Risk
- Risk level: [Low/Medium/High]
- Mitigation: [Measures in place]

### Individual Agency
- [ ] Opt-out available
- [ ] Human review requestable
- [ ] AI involvement disclosed

### Recommendations
1. [Priority action]
2. [Priority action]
```

## Key Questions

1. Is the automation level appropriate for the stakes?
2. Can humans meaningfully override the system?
3. Are humans actually exercising oversight?
4. What prevents automation bias?
5. Can affected individuals request human review?
