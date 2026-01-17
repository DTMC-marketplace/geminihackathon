# Standards Compliance Scripts

This directory contains Python scripts for automated standards compliance testing and validation per EU AI Act Article 40.

## Scripts

### validate_standards_compliance.py

Automated validation of AI systems for compliance with harmonized standards, API standardization, and data format interoperability.

**Usage:**
```bash
# Validate API specification
python validate_standards_compliance.py --api-spec api.yaml

# Validate data file against schema
python validate_standards_compliance.py --data-file data.json --schema schema.json

# Check system interoperability
python validate_standards_compliance.py --config system_config.json

# Save report to file
python validate_standards_compliance.py --api-spec api.yaml --output report.txt
```

**Features:**
- OpenAPI/Swagger specification validation
- Data format validation (JSON, XML, etc.)
- Schema validation (JSON Schema, XSD)
- Interoperability checks
- Vendor lock-in detection
- Standards compliance reporting

### suggest_standard_implementation.py

AI-assisted suggestions for standard-compliant implementations.

**Usage:**
```bash
# Get API design suggestions
python suggest_standard_implementation.py --api-requirements requirements.json

# Get data format recommendation
python suggest_standard_implementation.py --use-case "data exchange" --format json

# Get integration pattern proposal
python suggest_standard_implementation.py --ecosystem ecosystem_config.json

# Get compliance improvement suggestions
python suggest_standard_implementation.py --improvements current_impl.json
```

**Features:**
- API design recommendations (REST, GraphQL, gRPC)
- Data format recommendations (JSON, XML, Protocol Buffers, Parquet)
- Integration pattern proposals (API Gateway, Message Queue, Event-Driven)
- Compliance improvement suggestions
- Standards-based implementation guidance

### api_standardization_checker.py

Validates API standardization compliance including OpenAPI conformance, OAuth compliance, and versioning.

**Usage:**
```bash
# Validate OpenAPI specification
python api_standardization_checker.py --openapi api.yaml

# Check OAuth compliance
python api_standardization_checker.py --endpoints endpoints.json --oauth

# Verify API versioning
python api_standardization_checker.py --versioning api_config.json

# Generate comprehensive report
python api_standardization_checker.py --openapi api.yaml --output report.txt
```

**Features:**
- OpenAPI structure validation
- OAuth 2.0 compliance checking
- API versioning verification
- Security scheme validation
- Documentation completeness checks

## Dependencies

Required Python packages:
- `pyyaml` - For YAML file parsing
- Standard library: `json`, `argparse`, `pathlib`, `re`

Install dependencies:
```bash
pip install pyyaml
```

## Example Configurations

### API Requirements JSON
```json
{
  "use_case": "web services",
  "performance": "standard",
  "real_time": false,
  "mobile_support": true
}
```

### System Configuration JSON
```json
{
  "apis": [
    {
      "protocol": "REST",
      "specification": "OpenAPI 3.0"
    }
  ],
  "data_export_formats": ["JSON", "XML"],
  "dependencies": {
    "api_client": {
      "type": "standard",
      "specification": "OpenAPI"
    }
  }
}
```

### API Versioning Configuration JSON
```json
{
  "strategy": "url",
  "current_version": "1.0.0",
  "supported_versions": ["1.0.0", "0.9.0"],
  "deprecation_policy": {
    "notice_period": "6 months"
  }
}
```

## Integration

These scripts can be integrated into CI/CD pipelines for continuous compliance validation:

```yaml
# Example GitHub Actions workflow
- name: Validate Standards Compliance
  run: |
    python validate_standards_compliance.py --api-spec api/openapi.yaml
    python api_standardization_checker.py --openapi api/openapi.yaml
```

## Output Formats

All scripts support:
- **Text output**: Human-readable validation reports
- **JSON output**: Machine-readable results (for `suggest_standard_implementation.py` with `--format json`)

## Error Handling

Scripts handle:
- Missing files gracefully
- Invalid file formats
- Malformed specifications
- Missing required fields

All errors are reported in the validation results with clear messages.
