# Privacy Assessment

Evaluation of data protection, consent, and privacy-preserving practices.

## Privacy Principles

| Principle | Description | Assessment Question |
|-----------|-------------|---------------------|
| **Minimization** | Collect only necessary data | Is each data point justified? |
| **Purpose limitation** | Use data only for stated purposes | Are all uses disclosed and consented? |
| **Accuracy** | Keep data correct and current | Are correction mechanisms available? |
| **Storage limitation** | Retain only as long as needed | Are retention periods defined? |
| **Security** | Protect against unauthorized access | Are appropriate safeguards in place? |
| **Accountability** | Demonstrate compliance | Is compliance documented? |

## Data Inventory

### Personal Data Mapping
| Data Element | Source | Purpose | Legal Basis | Retention | Access |
|--------------|--------|---------|-------------|-----------|--------|
| [Element 1] | | | | | |
| [Element 2] | | | | | |

### Sensitive Data Categories
- [ ] Racial/ethnic origin
- [ ] Political opinions
- [ ] Religious beliefs
- [ ] Trade union membership
- [ ] Genetic data
- [ ] Biometric data
- [ ] Health data
- [ ] Sexual orientation
- [ ] Criminal history
- [ ] Financial data
- [ ] Location data
- [ ] Children's data

## Consent Assessment

### Consent Requirements
| Element | Required | Present |
|---------|----------|---------|
| Freely given | Yes | [ ] |
| Specific | Yes | [ ] |
| Informed | Yes | [ ] |
| Unambiguous | Yes | [ ] |
| Withdrawable | Yes | [ ] |

### Consent Documentation
- How is consent obtained?
- What information is provided?
- How can consent be withdrawn?
- How are consent records maintained?

### Special Consent Situations
- [ ] Children (parental consent required)
- [ ] Employees (power imbalance considerations)
- [ ] Research subjects (ethics board approval)
- [ ] Vulnerable populations (additional safeguards)

## Privacy Risk Assessment

### Risk Categories
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Unauthorized access | | | |
| Data breach | | | |
| Function creep | | | |
| Re-identification | | | |
| Inference attacks | | | |
| Discrimination | | | |

### Re-identification Risks
- What quasi-identifiers exist?
- Could data be linked to external sources?
- Is k-anonymity sufficient? (Generally k ≥ 5)
- Has differential privacy been considered?

## Privacy-Preserving Techniques

### Data Minimization
- Feature selection to reduce data collected
- Aggregation where individual records not needed
- Anonymization/pseudonymization

### Technical Safeguards
| Technique | Use Case | Tradeoffs |
|-----------|----------|-----------|
| Differential privacy | Statistical queries | Accuracy loss |
| Federated learning | Distributed training | Complexity, some leakage |
| Homomorphic encryption | Computation on encrypted data | Performance overhead |
| Secure multi-party computation | Joint computation | Communication overhead |
| K-anonymity | Dataset release | Information loss |
| Synthetic data | Testing, sharing | Fidelity concerns |

### Access Controls
- Principle of least privilege
- Role-based access
- Audit logging
- Encryption at rest and in transit

## Regulatory Compliance

### GDPR (EU)
- [ ] Lawful basis identified
- [ ] Privacy notice provided
- [ ] Data subject rights enabled
- [ ] Data protection impact assessment (if high risk)
- [ ] Data processing agreements with processors
- [ ] Cross-border transfer mechanisms

### CCPA (California)
- [ ] Right to know
- [ ] Right to delete
- [ ] Right to opt-out of sale
- [ ] Non-discrimination

### Sector-Specific
- [ ] HIPAA (healthcare)
- [ ] FERPA (education)
- [ ] COPPA (children)
- [ ] GLBA (financial)

## Data Subject Rights

| Right | Process | Timeline |
|-------|---------|----------|
| Access | [Process description] | [X days] |
| Rectification | [Process description] | [X days] |
| Erasure | [Process description] | [X days] |
| Portability | [Process description] | [X days] |
| Objection | [Process description] | [X days] |
| Restrict processing | [Process description] | [X days] |

## Output: Privacy Assessment Summary

```markdown
## Privacy Assessment

### Data Inventory Summary
- Personal data elements: [Count]
- Sensitive data categories: [List]
- Data sources: [Count/List]

### Consent Status
- [ ] Valid consent obtained
- [ ] Withdrawal mechanism available
- [ ] Consent records maintained

### Key Risks Identified
1. [Risk 1]: [Severity] - [Mitigation]
2. [Risk 2]: [Severity] - [Mitigation]

### Compliance Status
- GDPR: [Compliant/Gaps identified]
- CCPA: [Compliant/Gaps identified]
- Sector-specific: [Status]

### Privacy-Preserving Measures
- [Measure 1]: [Status]
- [Measure 2]: [Status]

### Recommendations
1. [Priority action]
2. [Priority action]
```
