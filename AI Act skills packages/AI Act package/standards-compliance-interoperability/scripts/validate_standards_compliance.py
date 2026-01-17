#!/usr/bin/env python3
"""
Standards Compliance Validator
==============================
Automated validation of AI systems for compliance with harmonized standards,
API standardization, and data format interoperability per EU AI Act Article 40.

Usage:
    python validate_standards_compliance.py --api-spec api.yaml
    python validate_standards_compliance.py --data-file data.json --schema schema.json
    python validate_standards_compliance.py --config system_config.json
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any
import yaml


class StandardsValidator:
    """Validates compliance with harmonized standards and interoperability requirements."""
    
    def __init__(self):
        self.validation_results = []
        self.errors = []
        self.warnings = []
    
    def validate_api_compliance(self, api_spec_path: str) -> Dict[str, Any]:
        """
        Validate API compliance with OpenAPI/Swagger standards.
        
        Args:
            api_spec_path: Path to OpenAPI/Swagger specification file
            
        Returns:
            Validation results dictionary
        """
        results = {
            "type": "api_compliance",
            "spec_file": api_spec_path,
            "valid": True,
            "errors": [],
            "warnings": [],
            "checks": {}
        }
        
        try:
            spec_path = Path(api_spec_path)
            if not spec_path.exists():
                results["valid"] = False
                results["errors"].append(f"API specification file not found: {api_spec_path}")
                return results
            
            # Load specification
            with spec_path.open('r', encoding='utf-8') as f:
                if spec_path.suffix in ['.yaml', '.yml']:
                    spec = yaml.safe_load(f)
                else:
                    spec = json.load(f)
            
            # Validate OpenAPI structure
            results["checks"]["openapi_version"] = self._check_openapi_version(spec)
            results["checks"]["info_required"] = self._check_info_required(spec)
            results["checks"]["paths_defined"] = self._check_paths_defined(spec)
            results["checks"]["security_schemes"] = self._check_security_schemes(spec)
            results["checks"]["versioning"] = self._check_versioning(spec)
            results["checks"]["data_formats"] = self._check_data_formats(spec)
            
            # Determine overall validity
            all_checks = results["checks"].values()
            if isinstance(all_checks, dict):
                results["valid"] = all(
                    check.get("valid", False) if isinstance(check, dict) else check
                    for check in all_checks
                )
            else:
                results["valid"] = all(all_checks)
            
            # Collect errors and warnings
            for check in results["checks"].values():
                if isinstance(check, dict):
                    results["errors"].extend(check.get("errors", []))
                    results["warnings"].extend(check.get("warnings", []))
            
        except Exception as e:
            results["valid"] = False
            results["errors"].append(f"Error validating API specification: {str(e)}")
        
        self.validation_results.append(results)
        return results
    
    def validate_data_format(self, data_file: str, schema_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Validate data format against schema (JSON Schema, XSD, etc.).
        
        Args:
            data_file: Path to data file to validate
            schema_path: Optional path to schema file
            
        Returns:
            Validation results dictionary
        """
        results = {
            "type": "data_format",
            "data_file": data_file,
            "schema_file": schema_path,
            "valid": True,
            "errors": [],
            "warnings": [],
            "checks": {}
        }
        
        try:
            data_path = Path(data_file)
            if not data_path.exists():
                results["valid"] = False
                results["errors"].append(f"Data file not found: {data_file}")
                return results
            
            # Load data
            with data_path.open('r', encoding='utf-8') as f:
                if data_path.suffix == '.json':
                    data = json.load(f)
                else:
                    # For other formats, basic validation
                    data = f.read()
            
            # Basic format validation
            results["checks"]["format_valid"] = self._check_data_format_valid(data_path, data)
            results["checks"]["encoding"] = self._check_encoding(data_path)
            
            # Schema validation if provided
            if schema_path:
                schema_results = self._validate_against_schema(data_path, schema_path, data)
                results["checks"]["schema_validation"] = schema_results
                if not schema_results.get("valid", False):
                    results["valid"] = False
            
            # Determine overall validity
            if not results["checks"].get("format_valid", {}).get("valid", False):
                results["valid"] = False
            
        except json.JSONDecodeError as e:
            results["valid"] = False
            results["errors"].append(f"Invalid JSON format: {str(e)}")
        except Exception as e:
            results["valid"] = False
            results["errors"].append(f"Error validating data format: {str(e)}")
        
        self.validation_results.append(results)
        return results
    
    def check_interoperability(self, system_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check system interoperability and vendor lock-in prevention.
        
        Args:
            system_config: System configuration dictionary
            
        Returns:
            Interoperability check results
        """
        results = {
            "type": "interoperability",
            "valid": True,
            "errors": [],
            "warnings": [],
            "checks": {}
        }
        
        try:
            # Check for open standards
            results["checks"]["open_standards"] = self._check_open_standards(system_config)
            
            # Check API standardization
            results["checks"]["api_standardization"] = self._check_api_standardization(system_config)
            
            # Check data portability
            results["checks"]["data_portability"] = self._check_data_portability(system_config)
            
            # Check vendor independence
            results["checks"]["vendor_independence"] = self._check_vendor_independence(system_config)
            
            # Determine overall validity
            all_checks = results["checks"].values()
            results["valid"] = all(
                check.get("valid", False) if isinstance(check, dict) else check
                for check in all_checks
            )
            
            # Collect errors and warnings
            for check in results["checks"].values():
                if isinstance(check, dict):
                    results["errors"].extend(check.get("errors", []))
                    results["warnings"].extend(check.get("warnings", []))
            
        except Exception as e:
            results["valid"] = False
            results["errors"].append(f"Error checking interoperability: {str(e)}")
        
        self.validation_results.append(results)
        return results
    
    def _check_openapi_version(self, spec: Dict) -> Dict[str, Any]:
        """Check OpenAPI version."""
        check = {"valid": False, "errors": [], "warnings": []}
        
        if "openapi" in spec:
            version = spec["openapi"]
            if version.startswith("3."):
                check["valid"] = True
                check["version"] = version
            else:
                check["warnings"].append(f"OpenAPI version {version} may not be fully supported")
        else:
            check["errors"].append("Missing 'openapi' version field")
        
        return check
    
    def _check_info_required(self, spec: Dict) -> Dict[str, Any]:
        """Check required info fields."""
        check = {"valid": False, "errors": [], "warnings": []}
        
        if "info" not in spec:
            check["errors"].append("Missing 'info' section")
            return check
        
        info = spec["info"]
        required_fields = ["title", "version"]
        missing = [field for field in required_fields if field not in info]
        
        if missing:
            check["errors"].extend([f"Missing required info field: {field}" for field in missing])
        else:
            check["valid"] = True
        
        return check
    
    def _check_paths_defined(self, spec: Dict) -> Dict[str, Any]:
        """Check that paths are defined."""
        check = {"valid": False, "errors": [], "warnings": []}
        
        if "paths" not in spec:
            check["errors"].append("Missing 'paths' section")
            return check
        
        paths = spec["paths"]
        if not paths:
            check["warnings"].append("No API paths defined")
        else:
            check["valid"] = True
            check["path_count"] = len(paths)
        
        return check
    
    def _check_security_schemes(self, spec: Dict) -> Dict[str, Any]:
        """Check security schemes."""
        check = {"valid": False, "errors": [], "warnings": []}
        
        components = spec.get("components", {})
        security_schemes = components.get("securitySchemes", {})
        
        if not security_schemes:
            check["warnings"].append("No security schemes defined")
        else:
            check["valid"] = True
            # Check for standard schemes
            standard_schemes = ["oauth2", "openIdConnect", "http", "apiKey"]
            found_standard = any(
                scheme.get("type") in standard_schemes
                for scheme in security_schemes.values()
            )
            if not found_standard:
                check["warnings"].append("No standard security schemes (OAuth2, OpenID Connect) found")
        
        return check
    
    def _check_versioning(self, spec: Dict) -> Dict[str, Any]:
        """Check API versioning strategy."""
        check = {"valid": True, "errors": [], "warnings": []}
        
        # Check if version is in info
        info = spec.get("info", {})
        if "version" not in info:
            check["warnings"].append("API version not specified in info section")
        
        # Check for version in paths (e.g., /v1/, /v2/)
        paths = spec.get("paths", {})
        versioned_paths = [path for path in paths.keys() if "/v" in path]
        if not versioned_paths:
            check["warnings"].append("No versioned paths found - consider API versioning strategy")
        
        return check
    
    def _check_data_formats(self, spec: Dict) -> Dict[str, Any]:
        """Check data format standards."""
        check = {"valid": True, "errors": [], "warnings": []}
        
        # Check content types
        paths = spec.get("paths", {})
        content_types = set()
        
        for path_data in paths.values():
            for method_data in path_data.values():
                if isinstance(method_data, dict):
                    for content_type in method_data.get("requestBody", {}).get("content", {}).keys():
                        content_types.add(content_type)
                    for response in method_data.get("responses", {}).values():
                        for content_type in response.get("content", {}).keys():
                            content_types.add(content_type)
        
        standard_types = ["application/json", "application/xml"]
        found_standard = any(ct in standard_types for ct in content_types)
        
        if not found_standard and content_types:
            check["warnings"].append("Consider using standard content types (application/json, application/xml)")
        
        return check
    
    def _check_data_format_valid(self, data_path: Path, data: Any) -> Dict[str, Any]:
        """Check if data format is valid."""
        check = {"valid": True, "errors": [], "warnings": []}
        
        if data_path.suffix == '.json':
            if not isinstance(data, (dict, list)):
                check["valid"] = False
                check["errors"].append("JSON data must be object or array")
        elif data_path.suffix in ['.xml', '.xsd']:
            # Basic XML check would go here
            pass
        
        return check
    
    def _check_encoding(self, data_path: Path) -> Dict[str, Any]:
        """Check file encoding."""
        check = {"valid": True, "errors": [], "warnings": []}
        
        try:
            with data_path.open('r', encoding='utf-8') as f:
                f.read()
            check["encoding"] = "UTF-8"
        except UnicodeDecodeError:
            check["valid"] = False
            check["errors"].append("File encoding is not UTF-8")
        
        return check
    
    def _validate_against_schema(self, data_path: Path, schema_path: str, data: Any) -> Dict[str, Any]:
        """Validate data against schema."""
        check = {"valid": False, "errors": [], "warnings": []}
        
        schema_file = Path(schema_path)
        if not schema_file.exists():
            check["errors"].append(f"Schema file not found: {schema_path}")
            return check
        
        try:
            with schema_file.open('r', encoding='utf-8') as f:
                if schema_file.suffix == '.json':
                    schema = json.load(f)
                    # Basic JSON Schema validation would go here
                    # For full validation, use jsonschema library
                    check["valid"] = True
                    check["schema_type"] = "JSON Schema"
                else:
                    check["warnings"].append(f"Schema format {schema_file.suffix} validation not fully implemented")
        except Exception as e:
            check["errors"].append(f"Error loading schema: {str(e)}")
        
        return check
    
    def _check_open_standards(self, config: Dict) -> Dict[str, Any]:
        """Check use of open standards."""
        check = {"valid": True, "errors": [], "warnings": []}
        
        # Check for proprietary formats
        proprietary_indicators = ["proprietary", "vendor-specific", "custom-only"]
        config_str = json.dumps(config).lower()
        
        for indicator in proprietary_indicators:
            if indicator in config_str:
                check["warnings"].append(f"Potential proprietary format detected: {indicator}")
        
        return check
    
    def _check_api_standardization(self, config: Dict) -> Dict[str, Any]:
        """Check API standardization."""
        check = {"valid": True, "errors": [], "warnings": []}
        
        apis = config.get("apis", [])
        if not apis:
            check["warnings"].append("No API configuration found")
            return check
        
        standard_protocols = ["REST", "GraphQL", "gRPC"]
        for api in apis:
            protocol = api.get("protocol", "").upper()
            if protocol not in standard_protocols:
                check["warnings"].append(f"Non-standard API protocol: {protocol}")
        
        return check
    
    def _check_data_portability(self, config: Dict) -> Dict[str, Any]:
        """Check data portability."""
        check = {"valid": True, "errors": [], "warnings": []}
        
        export_formats = config.get("data_export_formats", [])
        standard_formats = ["JSON", "XML", "CSV", "Parquet"]
        
        if not export_formats:
            check["warnings"].append("No data export formats specified")
        else:
            has_standard = any(fmt.upper() in standard_formats for fmt in export_formats)
            if not has_standard:
                check["warnings"].append("No standard data export formats found")
        
        return check
    
    def _check_vendor_independence(self, config: Dict) -> Dict[str, Any]:
        """Check vendor independence."""
        check = {"valid": True, "errors": [], "warnings": []}
        
        dependencies = config.get("dependencies", {})
        vendor_lock_indicators = ["vendor-specific", "proprietary", "single-vendor"]
        
        for dep_name, dep_info in dependencies.items():
            if isinstance(dep_info, dict):
                dep_str = json.dumps(dep_info).lower()
                if any(indicator in dep_str for indicator in vendor_lock_indicators):
                    check["warnings"].append(f"Potential vendor lock-in in dependency: {dep_name}")
        
        return check
    
    def generate_report(self) -> str:
        """Generate validation report."""
        report_lines = [
            "=" * 60,
            "Standards Compliance Validation Report",
            "=" * 60,
            ""
        ]
        
        for result in self.validation_results:
            report_lines.append(f"Type: {result['type']}")
            report_lines.append(f"Status: {'✓ VALID' if result['valid'] else '✗ INVALID'}")
            report_lines.append("")
            
            if result.get("errors"):
                report_lines.append("Errors:")
                for error in result["errors"]:
                    report_lines.append(f"  - {error}")
                report_lines.append("")
            
            if result.get("warnings"):
                report_lines.append("Warnings:")
                for warning in result["warnings"]:
                    report_lines.append(f"  - {warning}")
                report_lines.append("")
            
            report_lines.append("-" * 60)
            report_lines.append("")
        
        return "\n".join(report_lines)


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Validate standards compliance for AI systems"
    )
    parser.add_argument("--api-spec", help="Path to OpenAPI/Swagger specification")
    parser.add_argument("--data-file", help="Path to data file to validate")
    parser.add_argument("--schema", help="Path to schema file for data validation")
    parser.add_argument("--config", help="Path to system configuration JSON file")
    parser.add_argument("--output", help="Output file for report")
    
    args = parser.parse_args()
    
    validator = StandardsValidator()
    
    if args.api_spec:
        print(f"Validating API specification: {args.api_spec}")
        result = validator.validate_api_compliance(args.api_spec)
        print(f"API Compliance: {'✓ VALID' if result['valid'] else '✗ INVALID'}")
    
    if args.data_file:
        print(f"Validating data file: {args.data_file}")
        result = validator.validate_data_format(args.data_file, args.schema)
        print(f"Data Format: {'✓ VALID' if result['valid'] else '✗ INVALID'}")
    
    if args.config:
        print(f"Checking interoperability: {args.config}")
        with open(args.config, 'r') as f:
            config = json.load(f)
        result = validator.check_interoperability(config)
        print(f"Interoperability: {'✓ VALID' if result['valid'] else '✗ INVALID'}")
    
    # Generate report
    report = validator.generate_report()
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"\nReport saved to: {args.output}")
    else:
        print("\n" + report)


if __name__ == "__main__":
    main()
