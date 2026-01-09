# EU AI Act Detailed Requirements

## Regulatory Structure

### Act Scope (Article 2)

```yaml
in_scope:
  - "Providers placing AI systems on EU market"
  - "Deployers of AI systems within EU"
  - "Providers/deployers outside EU if output used in EU"
  - "Importers and distributors"
  - "Product manufacturers integrating AI"

out_of_scope:
  - "Military and national security AI"
  - "AI for scientific research only"
  - "AI for personal non-professional use"
  - "AI under development (not placed on market)"
```

### Key Definitions (Article 3)

```yaml
definitions:
  ai_system:
    text: "Machine-based system designed to operate with varying levels of autonomy, that may exhibit adaptiveness after deployment, and that, for explicit or implicit objectives, infers, from the input it receives, how to generate outputs such as predictions, content, recommendations, or decisions that can influence physical or virtual environments"

  provider:
    text: "Natural or legal person that develops an AI system or GPAI model, or has an AI system developed, and places it on the market or puts it into service under its own name or trademark"

  deployer:
    text: "Natural or legal person that uses an AI system under its authority except where the AI system is used in the course of a personal non-professional activity"

  high_risk_ai:
    text: "AI system referred to in Article 6, that poses significant risks to health, safety, or fundamental rights"

  general_purpose_ai:
    text: "AI model trained with large amounts of data using self-supervision at scale, that displays significant generality and is capable of competently performing a wide range of distinct tasks"
```

## High-Risk Requirements Detail

### Article 9: Risk Management System

```yaml
risk_management_system:
  nature: "Continuous iterative process throughout AI lifecycle"

  requirements:
    - id: "9.2.a"
      requirement: "Identification and analysis of known and reasonably foreseeable risks"
      verification: "Risk register with categorized risks"

    - id: "9.2.b"
      requirement: "Estimation and evaluation of risks arising from intended use and foreseeable misuse"
      verification: "Risk assessment with probability and impact scores"

    - id: "9.2.c"
      requirement: "Evaluation of risks based on post-market monitoring data"
      verification: "Monitoring data analysis reports"

    - id: "9.2.d"
      requirement: "Adoption of appropriate risk management measures"
      verification: "Implemented mitigations with effectiveness tracking"

  testing_requirements:
    - id: "9.6"
      requirement: "Testing against defined metrics and probabilistic thresholds"
      verification: "Test plans and results documentation"

    - id: "9.7"
      requirement: "Testing procedures for foreseeable conditions"
      verification: "Edge case and stress testing results"

    - id: "9.8"
      requirement: "Testing for foreseeable misuse scenarios"
      verification: "Adversarial testing documentation"
```

### Article 10: Data and Data Governance

```yaml
data_governance:
  training_data:
    - id: "10.2"
      requirement: "Training, validation, and testing data sets subject to appropriate data governance"
      includes:
        - "Design choices"
        - "Data collection processes"
        - "Relevant data preparation operations"
        - "Formulation of relevant assumptions"
        - "Prior assessment of data availability and suitability"
        - "Examination for possible biases"
        - "Gap identification and remediation"

  data_quality:
    - id: "10.3"
      requirement: "Data sets must be relevant, sufficiently representative, and to the best extent possible, free of errors and complete"
      verification: "Data quality reports with metrics"

    - id: "10.4"
      requirement: "Account for characteristics specific to geographic, contextual, behavioral, or functional setting"
      verification: "Representativeness analysis"

  special_categories:
    - id: "10.5"
      requirement: "Processing of special categories only when strictly necessary for bias detection/correction"
      safeguards:
        - "Technical limitations on re-use"
        - "State-of-the-art security measures"
        - "Logging of access"
        - "Data minimization"
```

### Article 11: Technical Documentation

```yaml
technical_documentation:
  timing: "Before placing on market or putting into service"
  update: "Keep up to date"

  content_annex_iv:
    general:
      - "General description of AI system"
      - "Intended purpose"
      - "Version identifier"
      - "How AI system interacts with hardware/software"
      - "Versions of relevant software/firmware"
      - "Instructions of use for deployers"

    technical:
      - "Description of development process"
      - "Design specifications including architecture"
      - "Description of computational resources used"
      - "Description of all changes made during lifecycle"
      - "Pre-determined changes and their management"

    data:
      - "Description of training methodologies and techniques"
      - "Description of training data (origin, scope, characteristics)"
      - "Data preparation (annotation, labeling, cleaning)"
      - "Relevance and representativeness analysis"

    performance:
      - "Description of metrics used"
      - "Expected level of accuracy"
      - "Robustness specifications"
      - "Cybersecurity specifications"
      - "Known limitations"

    risk:
      - "Description of risk management system"
      - "Description of risks and mitigations"
      - "Monitoring and post-market processes"

    human_oversight:
      - "Description of oversight measures"
      - "Technical measures facilitating oversight"
```

### Article 12: Record-Keeping

```yaml
record_keeping:
  automatic_logging:
    - id: "12.1"
      requirement: "High-risk AI systems shall technically allow automatic recording of events (logs)"

  logged_data:
    - "Period of use (start and end date/time)"
    - "Reference database used for input data verification"
    - "Input data for which search led to match"
    - "Natural persons involved in verification"
    - "For biometrics: conditions, results, output"

  traceability:
    - id: "12.2"
      requirement: "Appropriate to intended purpose and common logging practices"
      formats: "Compliant with relevant standards"

  retention:
    - id: "12.4"
      requirement: "Retention appropriate to intended purpose of high-risk AI system"
```

### Article 13: Transparency

```yaml
transparency_to_deployers:
  instructions_for_use:
    - "Identity and contact details of provider"
    - "Characteristics, capabilities, and limitations including purpose, accuracy, robustness, cybersecurity"
    - "Changes with implications for AI system"
    - "Human oversight measures including technical measures"
    - "Expected lifetime and maintenance measures"
    - "For systems learning after deployment: technical specifications and how system changes"

  performance_information:
    - "Levels of accuracy and accuracy metrics"
    - "Foreseeable unintended outcomes and sources of risks"
    - "Input data specifications"
    - "Where applicable: training, validation, testing data sets info"
```

### Article 14: Human Oversight

```yaml
human_oversight:
  design_requirements:
    - id: "14.2"
      requirement: "Enable effective oversight by natural persons during period of use"

  oversight_capabilities:
    - id: "14.4.a"
      capability: "Fully understand AI system capacities and limitations"

    - id: "14.4.b"
      capability: "Correctly interpret AI system output"

    - id: "14.4.c"
      capability: "Able to decide not to use AI system"

    - id: "14.4.d"
      capability: "Able to disregard, override, or reverse output"

    - id: "14.4.e"
      capability: "Intervene on operation or interrupt with stop button"

  proportionality:
    - id: "14.3"
      principle: "Measures proportionate to risks, level of autonomy, and context of use"
```

## GPAI Model Requirements

### General-Purpose AI (Chapter V)

```yaml
gpai_requirements:
  all_gpai_models:
    - "Technical documentation per Annex XI"
    - "Information for downstream providers"
    - "Copyright policy compliance"
    - "Training data summary publication"

  systemic_risk_gpai:
    criteria:
      - "Cumulative compute > 10^25 FLOP"
      - "Designated by Commission based on capabilities"

    additional_requirements:
      - "Model evaluation per standardized protocols"
      - "Systemic risk assessment and mitigation"
      - "Track, document, report serious incidents"
      - "Adequate cybersecurity protection"

  systemic_risk_mitigations:
    - "Red teaming"
    - "Downstream risk assessment"
    - "Internal/external security testing"
    - "Incident response and correction procedures"
```

## Conformity Assessment

### Self-Assessment Route

```yaml
self_assessment:
  applicable_to: "Most high-risk AI systems"

  steps:
    - "Implement all requirements (Articles 9-15)"
    - "Prepare technical documentation"
    - "Establish quality management system"
    - "Draw up EU declaration of conformity"
    - "Affix CE marking"

  eu_declaration:
    content:
      - "AI system identification"
      - "Name and address of provider"
      - "Statement that declaration is issued under sole responsibility"
      - "Statement of compliance with requirements"
      - "Reference to harmonized standards used"
      - "Name and signature of authorized person"
```

### Third-Party Assessment Route

```yaml
third_party_assessment:
  applicable_to:
    - "Remote biometric identification systems"
    - "When requested by provider"

  notified_body_role:
    - "Review quality management system"
    - "Review technical documentation"
    - "Conduct testing where needed"
    - "Issue certificate of conformity"

  certificate_validity: "Maximum 5 years, renewable"
```

## Timeline and Enforcement

```yaml
timeline:
  entry_into_force: "August 1, 2024"

  key_dates:
    prohibited_ai: "February 2, 2025"
    gpai_rules: "August 2, 2025"
    high_risk_annex_iii: "August 2, 2026"
    high_risk_product_safety: "August 2, 2027"

penalties:
  prohibited_practices: "Up to EUR 35 million or 7% global turnover"
  high_risk_non_compliance: "Up to EUR 15 million or 3% global turnover"
  incorrect_information: "Up to EUR 7.5 million or 1% global turnover"
```

---

**Last Updated:** 2025-12-26
