# Output Templates

Templates for ethics assessment deliverables.

## Executive Summary Template

```markdown
# AI Ethics Assessment: Executive Summary

**System**: [Name]
**Date**: [Date]
**Assessment Type**: [Tier 1 Rapid / Tier 2 Comprehensive]
**Overall Risk Level**: [Low / Medium / High / Critical]

## Key Findings

### Strengths
1. [Strength 1]
2. [Strength 2]
3. [Strength 3]

### Concerns
1. [Concern 1] - Severity: [High/Medium/Low]
2. [Concern 2] - Severity: [High/Medium/Low]
3. [Concern 3] - Severity: [High/Medium/Low]

## Risk Summary

| Category | Risk Level | Key Issue |
|----------|------------|-----------|
| Fairness | | |
| Transparency | | |
| Accountability | | |
| Privacy | | |
| Human Oversight | | |
| Community Impact | | |

## Recommendations

### Immediate Actions (Before Deployment)
1. [Action] - Owner: [Name] - Due: [Date]
2. [Action] - Owner: [Name] - Due: [Date]

### Short-term (30 days)
1. [Action]
2. [Action]

### Medium-term (90 days)
1. [Action]
2. [Action]

## Deployment Recommendation

[ ] APPROVE - Ready for deployment
[ ] APPROVE WITH CONDITIONS - Deploy after addressing [items]
[ ] HOLD - Significant work needed before deployment
[ ] DO NOT APPROVE - Fundamental concerns requiring redesign

## Next Steps
[Summary of what happens next]
```

## Technical Report Template

```markdown
# AI Ethics Technical Assessment Report

**System**: [Name]
**Version**: [Version]
**Date**: [Date]
**Assessor**: [Name]

## 1. System Overview

### 1.1 Purpose and Scope
[Description of what the system does and its intended use]

### 1.2 Technical Architecture
[High-level architecture description]

### 1.3 Data Sources
| Source | Type | Volume | Update Frequency |
|--------|------|--------|------------------|
| | | | |

### 1.4 Model Details
- Model type: [Description]
- Training period: [Dates]
- Key features: [List]
- Output: [Description]

## 2. Fairness Assessment

### 2.1 Protected Attributes Analyzed
[List of attributes and groups tested]

### 2.2 Fairness Metrics

| Metric | Group A | Group B | Disparity | Threshold | Status |
|--------|---------|---------|-----------|-----------|--------|
| Selection Rate | | | | 80% | |
| TPR | | | | 5% | |
| FPR | | | | 5% | |

### 2.3 Intersectional Analysis
[Analysis of intersecting groups]

### 2.4 Bias Sources Identified
1. [Source]: [Description and evidence]
2. [Source]: [Description and evidence]

### 2.5 Mitigation Applied
[Description of mitigation steps and effectiveness]

## 3. Explainability Assessment

### 3.1 Explainability Methods
[Methods implemented and their application]

### 3.2 Feature Importance
| Feature | Importance | Direction |
|---------|------------|-----------|
| | | |

### 3.3 Explanation Quality
[Assessment of explanation accuracy and comprehensibility]

## 4. Privacy Assessment

### 4.1 Data Inventory
[Summary of personal data used]

### 4.2 Privacy Risks
[Identified risks and mitigations]

### 4.3 Compliance Status
[Regulatory compliance assessment]

## 5. Human Oversight

### 5.1 Automation Level
[Current level and appropriateness]

### 5.2 Override Mechanisms
[Description of human control capabilities]

### 5.3 Monitoring Plan
[Ongoing oversight procedures]

## 6. Testing Summary

| Test Type | Scope | Result | Date |
|-----------|-------|--------|------|
| Functional | | | |
| Fairness | | | |
| Security | | | |
| Load | | | |

## 7. Risk Register

| Risk | Likelihood | Impact | Mitigation | Residual Risk |
|------|------------|--------|------------|---------------|
| | | | | |

## 8. Recommendations

### 8.1 Required Before Deployment
[List of blocking items]

### 8.2 Recommended Improvements
[List of non-blocking recommendations]

### 8.3 Ongoing Monitoring
[Required monitoring activities]

## 9. Appendices
[Supporting documentation]
```

## Stakeholder Communication Template

```markdown
# [System Name]: Information for [Stakeholder Group]

## What is [System Name]?

[Plain language description of the system and its purpose]

## How It Affects You

[Clear explanation of how this system impacts this stakeholder group]

## How It Works

[Simple, jargon-free explanation of the decision-making process]

The key factors that influence decisions are:
- [Factor 1]
- [Factor 2]
- [Factor 3]

## Your Rights

You have the right to:
- **Know**: Be informed when this system is used
- **Understand**: Receive an explanation of decisions
- **Challenge**: Request human review of decisions
- **Correct**: Update information about you

## If You Have Concerns

If you believe a decision was unfair or incorrect:

1. [Step 1 for raising concerns]
2. [Step 2]
3. [Step 3]

Contact: [Information]

## Our Commitments

We commit to:
- [Commitment 1]
- [Commitment 2]
- [Commitment 3]

## Questions?

[Contact information and resources]
```

## Incident Report Template

```markdown
# AI Ethics Incident Report

**Incident ID**: [ID]
**System**: [Name]
**Date Detected**: [Date]
**Severity**: [P0/P1/P2/P3]
**Status**: [Open/Investigating/Resolved/Closed]

## Incident Summary
[Brief description of what happened]

## Timeline
| Time | Event |
|------|-------|
| [Time] | Issue first detected |
| [Time] | [Subsequent events] |
| [Time] | Issue resolved |

## Impact Assessment

### Who Was Affected
- Number of individuals: [Count]
- Demographics: [If relevant]
- Nature of impact: [Description]

### Harm Assessment
[Description of actual or potential harm]

## Root Cause Analysis

### Contributing Factors
1. [Factor 1]
2. [Factor 2]

### Root Cause
[Underlying cause identified]

## Response Actions

### Immediate
1. [Action taken]
2. [Action taken]

### Remediation
1. [Step to fix issue]
2. [Step to fix issue]

### Communication
- Internal: [Who was notified]
- External: [Who was notified]
- Affected individuals: [How they were informed]

## Prevention

### Process Changes
1. [Change to prevent recurrence]

### Technical Changes
1. [Change to prevent recurrence]

### Monitoring Improvements
1. [New monitoring]

## Lessons Learned
[Key takeaways from this incident]

## Appendices
[Supporting documentation]
```

## Quick Reference Card

```markdown
# AI Ethics Quick Reference

## Rapid Check Questions
1. Who could be harmed?
2. Is there fairness testing?
3. Can decisions be explained?
4. Can humans override?
5. Is there an appeal process?

## Red Flags → Escalate
- No fairness testing
- Protected attributes as features
- No human oversight for high stakes
- Cannot explain decisions
- No appeal mechanism

## Fairness Metrics Quick Guide
- **80% Rule**: Minority rate ≥ 80% of majority
- **5% Disparity**: Error rates within 5%
- Test intersectional groups (e.g., Black women)

## Documentation Checklist
- [ ] Purpose documented
- [ ] Data sources listed
- [ ] Testing results recorded
- [ ] Known limitations stated
- [ ] Monitoring plan defined

## Escalation Contacts
- Ethics: [Contact]
- Legal: [Contact]
- Security: [Contact]
```
