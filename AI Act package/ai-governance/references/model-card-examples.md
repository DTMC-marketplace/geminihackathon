# Model Card Examples

## Example 1: Credit Scoring Model

```yaml
model_card:
  model_details:
    name: "CreditRisk-XGB-v2.3"
    version: "2.3.0"
    type: "Binary Classification (Gradient Boosting)"
    developer: "Risk Analytics Team, Acme Financial"
    license: "Proprietary - Internal Use Only"
    release_date: "2024-11-15"
    contact: "model-risk@acmefinancial.com"

  intended_use:
    primary_use_cases:
      - "Consumer credit application decisioning"
      - "Risk-based pricing recommendations"
    intended_users:
      - "Underwriting systems"
      - "Credit analysts (for manual review)"
    out_of_scope_uses:
      - "Commercial/business lending"
      - "Mortgage lending"
      - "Insurance underwriting"
      - "Employment decisions"

  factors:
    relevant_factors:
      - "Credit history length"
      - "Payment history"
      - "Credit utilization"
      - "Account mix"
      - "Recent inquiries"
    evaluation_factors:
      - "Age group (for fairness analysis)"
      - "Geographic region"
      - "Income bracket"

  metrics:
    performance_measures:
      auc_roc: 0.82
      ks_statistic: 0.54
      gini_coefficient: 0.64
      accuracy: 0.79
      precision_default_class: 0.71
      recall_default_class: 0.68
    decision_thresholds:
      approve_threshold: 0.25
      decline_threshold: 0.65
      manual_review_range: "0.25-0.65"
    fairness_metrics:
      disparate_impact_ratio_age: 0.92
      disparate_impact_ratio_gender: 0.95
      equalized_odds_difference: 0.03

  evaluation_data:
    datasets:
      - name: "Internal validation set"
        size: "150,000 applications"
        time_period: "2023-01-01 to 2023-12-31"
    preprocessing:
      - "Missing value imputation (median for numeric)"
      - "Outlier capping at 99th percentile"
      - "Feature standardization"

  training_data:
    datasets:
      - name: "Historical credit applications"
        size: "2.1 million applications"
        time_period: "2020-01-01 to 2022-12-31"
    motivation: "Representative sample of credit decisions with observed outcomes"
    preprocessing:
      - "12-month performance window for label definition"
      - "Exclusion of fraud cases"
      - "Reject inference applied"

  quantitative_analyses:
    unitary_results:
      - "Model performs consistently across income brackets"
      - "Slight performance degradation for thin-file applicants"
    intersectional_results:
      - "Young + thin-file segment shows 8% lower precision"
      - "No significant disparities in other intersections"

  ethical_considerations:
    sensitive_use_cases:
      - "Model output directly affects credit access"
      - "Potential for economic harm from false positives"
    known_limitations:
      - "Limited performance on applicants with no credit history"
      - "Does not account for sudden income changes"
    bias_mitigations:
      - "Reject inference applied to reduce selection bias"
      - "Regular disparate impact monitoring"
      - "Fair lending review before deployment"

  caveats_recommendations:
    known_issues:
      - "Performance degrades for applications with >50% missing features"
      - "Not validated for economic downturn conditions"
    recommendations:
      - "Use with human review for borderline decisions"
      - "Monitor performance monthly for drift"
      - "Retrain annually or when PSI exceeds 0.25"
    additional_testing:
      - "Quarterly fair lending analysis"
      - "Annual third-party audit"
```

## Example 2: Medical Imaging Classifier

```yaml
model_card:
  model_details:
    name: "ChestXR-Pneumonia-Detector-v1.2"
    version: "1.2.0"
    type: "Convolutional Neural Network (ResNet-50 backbone)"
    developer: "AI Research Lab, Metro Health System"
    license: "Research Use Only"
    release_date: "2024-09-01"
    regulatory_status: "FDA 510(k) pending"
    contact: "ai-safety@metrohealth.org"

  intended_use:
    primary_use_cases:
      - "Prioritization of chest X-rays for radiologist review"
      - "Detection of pneumonia patterns requiring urgent attention"
    intended_users:
      - "Radiologists (as decision support)"
      - "Emergency department triage systems"
    out_of_scope_uses:
      - "Standalone diagnosis without radiologist confirmation"
      - "Pediatric patients (under 18)"
      - "Portable/bedside X-ray images"
      - "Non-PA/AP chest views"

  factors:
    relevant_factors:
      - "Image acquisition parameters"
      - "Patient positioning"
      - "Image quality/artifacts"
    evaluation_factors:
      - "Patient age groups (18-40, 41-60, 61-80, 80+)"
      - "Sex"
      - "BMI categories"
      - "Presence of other lung conditions"

  metrics:
    performance_measures:
      auc_roc: 0.94
      sensitivity: 0.91
      specificity: 0.89
      ppv: 0.87
      npv: 0.92
      f1_score: 0.89
    decision_thresholds:
      urgent_flag_threshold: 0.85
      normal_threshold: 0.15
    subgroup_performance:
      age_18_40:
        sensitivity: 0.93
        specificity: 0.91
      age_61_80:
        sensitivity: 0.89
        specificity: 0.87
      age_80_plus:
        sensitivity: 0.85
        specificity: 0.84

  evaluation_data:
    datasets:
      - name: "Internal validation set"
        size: "15,000 X-rays"
        source: "Metro Health System PACS"
        time_period: "2023-06-01 to 2024-05-31"
      - name: "External validation set"
        size: "5,000 X-rays"
        source: "NIH ChestX-ray14 (subset)"
    preprocessing:
      - "DICOM to PNG conversion"
      - "Resize to 512x512"
      - "Histogram equalization"
      - "Intensity normalization"

  training_data:
    datasets:
      - name: "Training dataset"
        size: "120,000 X-rays"
        pneumonia_positive: "28,000 (23%)"
        time_period: "2018-01-01 to 2022-12-31"
    label_source: "Radiologist reports with NLP extraction + manual verification"
    preprocessing:
      - "Data augmentation (rotation, flip, brightness)"
      - "Class balancing via oversampling"

  quantitative_analyses:
    unitary_results:
      - "Consistent performance across image quality levels"
      - "3% sensitivity drop for patients with COPD"
    intersectional_results:
      - "Male + age 80+ shows 5% lower specificity"
      - "Female + obese shows 4% lower sensitivity"

  ethical_considerations:
    sensitive_use_cases:
      - "Missed pneumonia could delay treatment"
      - "False positives could lead to unnecessary treatment"
    known_limitations:
      - "Not validated for atypical pneumonia presentations"
      - "Performance degraded for patients with multiple comorbidities"
      - "Not designed for COVID-19 specific patterns"
    bias_mitigations:
      - "Balanced training across demographic groups"
      - "Regular subgroup analysis"
      - "Radiologist override always available"

  caveats_recommendations:
    known_issues:
      - "False negatives more common in elderly patients"
      - "Artifacts from pacemakers may cause false positives"
    recommendations:
      - "Always confirm with radiologist review"
      - "Do not use for pediatric patients"
      - "Flag for manual review if confidence < 0.7"
    additional_testing:
      - "Prospective clinical trial (ongoing)"
      - "External validation at 3 additional sites"

  human_oversight:
    oversight_model: "Human-in-the-loop"
    oversight_mechanisms:
      - "All positive predictions reviewed by radiologist"
      - "Confidence score displayed with prediction"
      - "Easy override mechanism in PACS integration"
    escalation_path: "Low-confidence cases automatically flagged for senior radiologist"
```

## Example 3: Resume Screening Model

```yaml
model_card:
  model_details:
    name: "TalentMatch-NLP-v3.0"
    version: "3.0.1"
    type: "Transformer-based NLP (fine-tuned BERT)"
    developer: "HR Tech Team, TechCorp Inc."
    license: "Proprietary"
    release_date: "2024-07-15"
    contact: "ai-ethics@techcorp.com"
    bias_audit_date: "2024-06-01"
    bias_auditor: "Independent AI Audit LLC"

  intended_use:
    primary_use_cases:
      - "Initial resume screening for software engineering roles"
      - "Candidate ranking for recruiter review"
    intended_users:
      - "Recruiters (for prioritization)"
      - "Hiring managers (for context)"
    out_of_scope_uses:
      - "Final hiring decisions without human review"
      - "Non-technical roles"
      - "Executive-level positions"
      - "Internal promotion decisions"

  factors:
    relevant_factors:
      - "Technical skills mentioned"
      - "Experience level indicators"
      - "Education and certifications"
      - "Project descriptions"
    evaluation_factors:
      - "Gender (inferred from name for audit purposes only)"
      - "Ethnicity (inferred from name for audit purposes only)"
      - "Educational institution prestige tier"
      - "Career gap presence"

  metrics:
    performance_measures:
      recall_at_k_50: 0.78
      precision_at_k_10: 0.65
      ndcg: 0.72
      inter_rater_reliability: 0.81
    fairness_metrics:
      selection_rate_ratio_gender: 0.94
      selection_rate_ratio_ethnicity: 0.91
      selection_rate_ratio_education_tier: 0.88
      career_gap_impact: "+2% selection rate (controlled)"

  evaluation_data:
    datasets:
      - name: "Historical hiring validation"
        size: "25,000 applications"
        time_period: "2022-01-01 to 2023-12-31"
        successful_hires: "2,100"
    preprocessing:
      - "Resume parsing and standardization"
      - "PII removal for audit dataset"

  training_data:
    datasets:
      - name: "Successful hire resumes"
        size: "15,000 resumes"
        positive_samples: "Employees with positive performance reviews"
      - name: "Industry benchmark resumes"
        size: "50,000 resumes"
        source: "Anonymized industry dataset"
    motivation: "Learn patterns associated with successful technical hires"
    preprocessing:
      - "Name and demographic indicator removal"
      - "Standardized skill extraction"
      - "Experience level normalization"

  quantitative_analyses:
    unitary_results:
      - "No significant performance difference by gender"
      - "Slight preference for candidates from top-tier universities"
    intersectional_results:
      - "Female + non-traditional education: 8% lower ranking"
      - "Career gap + female: no additional penalty vs career gap alone"

  ethical_considerations:
    sensitive_use_cases:
      - "Directly affects employment opportunities"
      - "Historical data may encode past biases"
    known_limitations:
      - "May undervalue non-traditional backgrounds"
      - "Limited effectiveness for career changers"
      - "Cannot assess soft skills or culture fit"
    bias_mitigations:
      - "Name and demographic indicators removed from input"
      - "Regular bias audits (NYC LL144 compliant)"
      - "Human review required for all decisions"
      - "Alternative assessment path available"

  caveats_recommendations:
    known_issues:
      - "Overweights keyword matching vs demonstrated impact"
      - "May miss candidates with non-standard resume formats"
    recommendations:
      - "Use only for initial prioritization, not elimination"
      - "Always include human review of ranked candidates"
      - "Periodically review rejected candidates for false negatives"
      - "Provide alternative application path for accessibility"
    additional_testing:
      - "Annual third-party bias audit"
      - "Quarterly adverse impact analysis"

  transparency:
    candidate_notification: "Required before AI screening"
    audit_summary_publication: "Annual summary published on careers page"
    appeal_process: "Candidates may request human-only review"

  compliance:
    nyc_ll144: "Compliant"
    eeoc_guidance: "Reviewed and aligned"
    eu_ai_act_classification: "High-risk (employment)"
```

## Model Card Template (Empty)

```yaml
model_card:
  model_details:
    name: ""
    version: ""
    type: ""
    developer: ""
    license: ""
    release_date: ""
    contact: ""

  intended_use:
    primary_use_cases: []
    intended_users: []
    out_of_scope_uses: []

  factors:
    relevant_factors: []
    evaluation_factors: []

  metrics:
    performance_measures: {}
    decision_thresholds: {}
    fairness_metrics: {}

  evaluation_data:
    datasets: []
    preprocessing: []

  training_data:
    datasets: []
    motivation: ""
    preprocessing: []

  quantitative_analyses:
    unitary_results: []
    intersectional_results: []

  ethical_considerations:
    sensitive_use_cases: []
    known_limitations: []
    bias_mitigations: []

  caveats_recommendations:
    known_issues: []
    recommendations: []
    additional_testing: []
```

---

**Last Updated:** 2025-12-26
