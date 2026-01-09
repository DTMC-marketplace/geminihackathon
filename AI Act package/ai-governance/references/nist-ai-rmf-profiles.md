# NIST AI RMF Sector-Specific Profiles

## Framework Overview

The NIST AI Risk Management Framework provides voluntary guidance for managing AI risks. Organizations can create profiles tailored to their sector, risk tolerance, and regulatory requirements.

## Healthcare AI Profile

```yaml
healthcare_ai_profile:
  sector: "Healthcare and Life Sciences"
  risk_tolerance: "Low (patient safety critical)"
  regulatory_context:
    - "FDA AI/ML guidance"
    - "HIPAA"
    - "21 CFR Part 11"
    - "EU MDR (for medical devices)"

  govern:
    policies:
      - "Clinical AI governance committee with physician representation"
      - "IRB-style review for patient-facing AI"
      - "Clear liability and accountability assignments"

    accountability:
      - "Chief Medical Officer oversight for clinical AI"
      - "Clinical validation team with domain expertise"
      - "Patient safety officer involvement"

  map:
    use_case_categories:
      diagnostic_support:
        risk_level: "High"
        considerations:
          - "Potential for delayed/missed diagnosis"
          - "Clinician over-reliance"
          - "Disparate performance across demographics"

      administrative:
        risk_level: "Medium"
        considerations:
          - "Billing accuracy"
          - "Scheduling fairness"

      drug_discovery:
        risk_level: "Medium-High"
        considerations:
          - "False positive/negative candidates"
          - "Bias in patient population modeling"

    affected_parties:
      - "Patients (primary)"
      - "Clinicians"
      - "Healthcare administrators"
      - "Insurers"

  measure:
    required_metrics:
      clinical_performance:
        - "Sensitivity and specificity"
        - "PPV and NPV for target population"
        - "AUC-ROC with confidence intervals"

      fairness:
        - "Performance parity across demographics"
        - "Subgroup analysis (age, sex, race, comorbidities)"

      safety:
        - "False negative rate in critical conditions"
        - "Alert fatigue metrics"
        - "Near-miss tracking"

    validation_requirements:
      - "External validation on independent datasets"
      - "Prospective clinical validation where feasible"
      - "Ongoing performance monitoring post-deployment"

  manage:
    mitigation_strategies:
      - "Clinician-in-the-loop for all diagnostic decisions"
      - "Confidence thresholds with human review"
      - "Regular retraining on updated clinical data"
      - "Fail-safe defaults when confidence is low"

    incident_response:
      - "Adverse event reporting procedures"
      - "FDA MAUDE reporting for medical devices"
      - "Root cause analysis protocols"
```

## Financial Services AI Profile

```yaml
financial_services_ai_profile:
  sector: "Banking and Financial Services"
  risk_tolerance: "Medium (with strict fairness requirements)"
  regulatory_context:
    - "Fair lending laws (ECOA, FHA)"
    - "SR 11-7 (Fed model risk management)"
    - "CFPB adverse action requirements"
    - "EU AI Act (credit scoring as high-risk)"

  govern:
    policies:
      - "Model Risk Management framework (SR 11-7 aligned)"
      - "Fair lending committee oversight"
      - "Three lines of defense model"

    accountability:
      - "Chief Model Risk Officer"
      - "Model validation team (independent)"
      - "Fair lending officer"

  map:
    use_case_categories:
      credit_decisioning:
        risk_level: "High"
        considerations:
          - "Disparate impact on protected classes"
          - "Adverse action explanation requirements"
          - "Economic harm from incorrect decisions"

      fraud_detection:
        risk_level: "Medium-High"
        considerations:
          - "False positive customer friction"
          - "False negative financial losses"
          - "Adaptive adversaries"

      customer_service:
        risk_level: "Medium"
        considerations:
          - "Service quality disparities"
          - "Escalation path availability"

    protected_classes:
      - "Race/ethnicity"
      - "Sex"
      - "Age"
      - "National origin"
      - "Religion"

  measure:
    required_metrics:
      performance:
        - "KS statistic"
        - "Gini coefficient"
        - "Population stability index"

      fairness:
        - "Disparate impact ratio (80% rule)"
        - "Equalized odds"
        - "Calibration by group"

      explainability:
        - "Feature importance rankings"
        - "Adverse action reason codes"
        - "Counterfactual explanations"

    validation_cadence:
      - "Annual model validation minimum"
      - "Quarterly monitoring reports"
      - "Trigger-based re-validation"

  manage:
    mitigation_strategies:
      - "Pre-processing fairness interventions"
      - "In-processing constraints"
      - "Post-processing adjustments with legal review"
      - "Human review for borderline decisions"

    documentation:
      - "Model development documentation"
      - "Model validation reports"
      - "Ongoing monitoring reports"
      - "Adverse action reason code documentation"
```

## Employment/HR AI Profile

```yaml
employment_ai_profile:
  sector: "Human Resources and Employment"
  risk_tolerance: "Low (fundamental rights impact)"
  regulatory_context:
    - "Title VII (Civil Rights Act)"
    - "ADA (Americans with Disabilities Act)"
    - "EEOC guidance on AI in employment"
    - "EU AI Act (employment as high-risk)"
    - "NYC Local Law 144"

  govern:
    policies:
      - "AI in employment policy with legal review"
      - "Candidate/employee notification requirements"
      - "Bias audit requirements (annual minimum)"

    accountability:
      - "CHRO accountability for AI hiring tools"
      - "Legal/compliance review for new tools"
      - "Vendor management for third-party tools"

  map:
    use_case_categories:
      resume_screening:
        risk_level: "High"
        considerations:
          - "Historical bias in training data"
          - "Proxy discrimination"
          - "Accessibility for disabled candidates"

      video_interviewing:
        risk_level: "High"
        considerations:
          - "Disability accommodation"
          - "Non-native speaker bias"
          - "Emotional analysis validity"

      performance_monitoring:
        risk_level: "High"
        considerations:
          - "Privacy implications"
          - "Psychological impact"
          - "Union/labor law considerations"

  measure:
    required_metrics:
      selection_rate:
        - "Selection rate by protected class"
        - "4/5ths rule compliance"
        - "Impact ratio for each stage"

      validity:
        - "Job-relatedness evidence"
        - "Criterion validity studies"
        - "Content validity documentation"

      accessibility:
        - "Accessibility for candidates with disabilities"
        - "Accommodation request handling"

    audit_requirements:
      - "Annual bias audit (NYC LL144 compliant)"
      - "Adverse impact analysis per selection tool"
      - "Third-party audit for high-volume hiring"

  manage:
    mitigation_strategies:
      - "Human review at each selection stage"
      - "Alternative assessment paths"
      - "Regular bias testing and remediation"
      - "Structured interview backup"

    transparency:
      - "Candidate notification of AI use"
      - "Explanation of assessment criteria"
      - "Appeal/review process"
```

## Autonomous Systems Profile

```yaml
autonomous_systems_profile:
  sector: "Autonomous Vehicles, Robotics, Drones"
  risk_tolerance: "Very Low (life safety critical)"
  regulatory_context:
    - "NHTSA AV guidance"
    - "FAA Part 107 (drones)"
    - "ISO 26262 (automotive safety)"
    - "IEC 61508 (functional safety)"

  govern:
    policies:
      - "Safety-first development culture"
      - "Operational design domain (ODD) governance"
      - "Fail-safe design requirements"

    accountability:
      - "Safety officer with veto authority"
      - "Independent safety assessment team"
      - "Clear chain of command for safety decisions"

  map:
    use_case_categories:
      perception:
        risk_level: "Critical"
        considerations:
          - "Object detection failures"
          - "Adverse weather performance"
          - "Edge case handling"

      decision_making:
        risk_level: "Critical"
        considerations:
          - "Ethical dilemmas"
          - "Unexpected scenario handling"
          - "Human handoff procedures"

      control:
        risk_level: "Critical"
        considerations:
          - "Actuator failures"
          - "Latency requirements"
          - "Graceful degradation"

  measure:
    required_metrics:
      safety:
        - "Miles/hours between disengagements"
        - "Collision rates vs human baseline"
        - "Near-miss frequency"

      perception:
        - "Object detection mAP by class"
        - "False negative rates for critical objects"
        - "Degradation in adverse conditions"

      reliability:
        - "MTBF for critical components"
        - "Fail-safe activation rates"
        - "Recovery success rates"

    testing_requirements:
      - "Simulation testing (billions of miles)"
      - "Closed-course testing"
      - "Public road testing with safety drivers"
      - "Periodic re-certification"

  manage:
    mitigation_strategies:
      - "Redundant perception systems"
      - "Conservative ODD boundaries"
      - "Graceful degradation modes"
      - "Remote monitoring and intervention"

    incident_response:
      - "Automated incident data capture"
      - "Immediate post-incident analysis"
      - "Fleet-wide safety bulletin process"
      - "Regulatory notification procedures"
```

## Government/Public Sector Profile

```yaml
government_ai_profile:
  sector: "Government and Public Sector"
  risk_tolerance: "Low (public trust critical)"
  regulatory_context:
    - "Executive Order 14110 (US)"
    - "OMB M-24-10 guidance"
    - "Agency-specific AI strategies"
    - "Constitutional due process requirements"

  govern:
    policies:
      - "Agency AI governance board"
      - "Public transparency requirements"
      - "Procurement standards for AI vendors"

    accountability:
      - "Chief AI Officer (CAIO)"
      - "Agency AI ethics board"
      - "Inspector General oversight"

  map:
    use_case_categories:
      benefits_determination:
        risk_level: "High"
        considerations:
          - "Due process requirements"
          - "Impact on vulnerable populations"
          - "Appeal rights preservation"

      fraud_detection:
        risk_level: "Medium-High"
        considerations:
          - "False positive burden on citizens"
          - "Due process before adverse action"

      service_delivery:
        risk_level: "Medium"
        considerations:
          - "Equitable access"
          - "Digital divide considerations"

  measure:
    required_metrics:
      equity:
        - "Demographic parity in outcomes"
        - "Error rates by population segment"
        - "Access and uptake rates"

      accuracy:
        - "False positive/negative rates"
        - "Accuracy in edge cases"

      efficiency:
        - "Processing time improvements"
        - "Cost savings vs error rates"

    transparency_requirements:
      - "AI use case inventory (public)"
      - "Annual AI impact assessments"
      - "Algorithmic impact assessments for high-risk"

  manage:
    mitigation_strategies:
      - "Human review for rights-affecting decisions"
      - "Clear appeal and redress processes"
      - "Regular audits by GAO/IG"
      - "Public comment periods for new AI use"

    public_engagement:
      - "Public notice of AI use"
      - "Community input mechanisms"
      - "Ongoing stakeholder engagement"
```

## Profile Customization Guide

### Creating Custom Profiles

```yaml
customization_steps:
  1_assess_context:
    - "Identify applicable regulations"
    - "Determine organizational risk tolerance"
    - "Map stakeholder expectations"
    - "Inventory existing AI systems"

  2_tailor_govern:
    - "Adapt policies to organizational structure"
    - "Define accountability based on org chart"
    - "Establish appropriate oversight bodies"

  3_customize_map:
    - "Categorize use cases by actual deployment"
    - "Identify organization-specific risks"
    - "Map affected parties in your context"

  4_define_measure:
    - "Select metrics relevant to your use cases"
    - "Set thresholds based on risk tolerance"
    - "Establish monitoring frequency"

  5_plan_manage:
    - "Design mitigations for identified risks"
    - "Create incident response procedures"
    - "Document residual risk acceptance"

  6_iterate:
    - "Review profile annually"
    - "Update for regulatory changes"
    - "Incorporate lessons learned"
```

---

**Last Updated:** 2025-12-26
