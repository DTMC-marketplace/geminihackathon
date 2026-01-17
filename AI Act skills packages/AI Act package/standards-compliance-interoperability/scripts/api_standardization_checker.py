#!/usr/bin/env python3
"""
API Standardization Checker
============================
Validates API standardization compliance including OpenAPI conformance,
OAuth compliance, versioning, and interoperability per EU AI Act Article 40.

Usage:
    python api_standardization_checker.py --openapi api.yaml
    python api_standardization_checker.py --endpoints endpoints.json --oauth
    python api_standardization_checker.py --versioning api_config.json
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any
import yaml
import re


class APIChecker:
    """Validates API standardization and compliance."""
    
    def __init__(self):
        self.check_results = []
        self.errors = []
        self.warnings = []
    
    def validate_openapi(self, openapi_spec_path: str) -> Dict[str, Any]:
        """
        Validate OpenAPI specification compliance.
        
        Args:
            openapi_spec_path: Path to OpenAPI specification file
            
        Returns:
            Validation results dictionary
        """
        results = {
            "type": "openapi_validation",
            "spec_file": openapi_spec_path,
            "valid": True,
            "errors": [],
            "warnings": [],
            "checks": {}
        }
        
        try:
            spec_path = Path(openapi_spec_path)
            if not spec_path.exists():
                results["valid"] = False
                results["errors"].append(f"OpenAPI specification file not found: {openapi_spec_path}")
                return results
            
            # Load specification
            with spec_path.open('r', encoding='utf-8') as f:
                if spec_path.suffix in ['.yaml', '.yml']:
                    spec = yaml.safe_load(f)
                else:
                    spec = json.load(f)
            
            # Perform checks
            results["checks"]["structure"] = self._check_openapi_structure(spec)
            results["checks"]["paths"] = self._check_paths_structure(spec)
            results["checks"]["operations"] = self._check_operations(spec)
            results["checks"]["schemas"] = self._check_schemas(spec)
            results["checks"]["responses"] = self._check_responses(spec)
            results["checks"]["security"] = self._check_security_definitions(spec)
            results["checks"]["documentation"] = self._check_documentation(spec)
            
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
            
        except yaml.YAMLError as e:
            results["valid"] = False
            results["errors"].append(f"Invalid YAML format: {str(e)}")
        except json.JSONDecodeError as e:
            results["valid"] = False
            results["errors"].append(f"Invalid JSON format: {str(e)}")
        except Exception as e:
            results["valid"] = False
            results["errors"].append(f"Error validating OpenAPI specification: {str(e)}")
        
        self.check_results.append(results)
        return results
    
    def check_oauth_compliance(self, api_endpoints: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Check OAuth 2.0 compliance for API endpoints.
        
        Args:
            api_endpoints: List of API endpoint configurations
            
        Returns:
            OAuth compliance check results
        """
        results = {
            "type": "oauth_compliance",
            "valid": True,
            "errors": [],
            "warnings": [],
            "checks": {}
        }
        
        try:
            # Check for OAuth endpoints
            results["checks"]["authorization_endpoint"] = self._check_authorization_endpoint(api_endpoints)
            results["checks"]["token_endpoint"] = self._check_token_endpoint(api_endpoints)
            results["checks"]["grant_types"] = self._check_grant_types(api_endpoints)
            results["checks"]["token_format"] = self._check_token_format(api_endpoints)
            results["checks"]["security_headers"] = self._check_security_headers(api_endpoints)
            
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
            results["errors"].append(f"Error checking OAuth compliance: {str(e)}")
        
        self.check_results.append(results)
        return results
    
    def verify_versioning(self, api_versioning_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verify API versioning strategy.
        
        Args:
            api_versioning_config: API versioning configuration
            
        Returns:
            Versioning verification results
        """
        results = {
            "type": "versioning_verification",
            "valid": True,
            "errors": [],
            "warnings": [],
            "checks": {}
        }
        
        try:
            versioning_strategy = api_versioning_config.get("strategy", "none")
            current_version = api_versioning_config.get("current_version")
            supported_versions = api_versioning_config.get("supported_versions", [])
            
            # Check versioning strategy
            results["checks"]["strategy"] = self._check_versioning_strategy(versioning_strategy)
            results["checks"]["version_format"] = self._check_version_format(current_version)
            results["checks"]["backward_compatibility"] = self._check_backward_compatibility(
                current_version, supported_versions
            )
            results["checks"]["deprecation_policy"] = self._check_deprecation_policy(api_versioning_config)
            
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
            results["errors"].append(f"Error verifying versioning: {str(e)}")
        
        self.check_results.append(results)
        return results
    
    def _check_openapi_structure(self, spec: Dict) -> Dict[str, Any]:
        """Check OpenAPI structure."""
        check = {"valid": False, "errors": [], "warnings": []}
        
        # Check required top-level fields
        required_fields = ["openapi", "info", "paths"]
        missing = [field for field in required_fields if field not in spec]
        
        if missing:
            check["errors"].extend([f"Missing required field: {field}" for field in missing])
        else:
            check["valid"] = True
        
        # Check OpenAPI version
        if "openapi" in spec:
            version = spec["openapi"]
            if not version.startswith("3."):
                check["warnings"].append(f"OpenAPI version {version} - consider upgrading to 3.x")
        
        return check
    
    def _check_paths_structure(self, spec: Dict) -> Dict[str, Any]:
        """Check paths structure."""
        check = {"valid": False, "errors": [], "warnings": []}
        
        paths = spec.get("paths", {})
        if not paths:
            check["errors"].append("No paths defined in API")
            return check
        
        check["valid"] = True
        check["path_count"] = len(paths)
        
        # Check path naming conventions
        for path in paths.keys():
            if not path.startswith("/"):
                check["warnings"].append(f"Path '{path}' should start with '/'")
            if "//" in path:
                check["warnings"].append(f"Path '{path}' contains double slashes")
        
        return check
    
    def _check_operations(self, spec: Dict) -> Dict[str, Any]:
        """Check HTTP operations."""
        check = {"valid": True, "errors": [], "warnings": []}
        
        standard_methods = ["get", "post", "put", "patch", "delete", "head", "options"]
        paths = spec.get("paths", {})
        
        for path, path_item in paths.items():
            if isinstance(path_item, dict):
                methods = [method for method in path_item.keys() if method in standard_methods]
                if not methods:
                    check["warnings"].append(f"Path '{path}' has no HTTP operations")
                else:
                    # Check for proper operation IDs
                    for method in methods:
                        operation = path_item[method]
                        if isinstance(operation, dict) and "operationId" not in operation:
                            check["warnings"].append(
                                f"Operation {method.upper()} {path} missing operationId"
                            )
        
        return check
    
    def _check_schemas(self, spec: Dict) -> Dict[str, Any]:
        """Check schema definitions."""
        check = {"valid": True, "errors": [], "warnings": []}
        
        components = spec.get("components", {})
        schemas = components.get("schemas", {})
        
        if not schemas:
            check["warnings"].append("No schema definitions found")
        else:
            check["schema_count"] = len(schemas)
            
            # Check schema structure
            for schema_name, schema in schemas.items():
                if isinstance(schema, dict):
                    if "type" not in schema and "$ref" not in schema:
                        check["warnings"].append(f"Schema '{schema_name}' missing type or $ref")
        
        return check
    
    def _check_responses(self, spec: Dict) -> Dict[str, Any]:
        """Check response definitions."""
        check = {"valid": True, "errors": [], "warnings": []}
        
        paths = spec.get("paths", {})
        standard_status_codes = ["200", "201", "400", "401", "403", "404", "500"]
        
        for path, path_item in paths.items():
            if isinstance(path_item, dict):
                for method, operation in path_item.items():
                    if method.lower() in ["get", "post", "put", "patch", "delete"]:
                        if isinstance(operation, dict):
                            responses = operation.get("responses", {})
                            if not responses:
                                check["warnings"].append(
                                    f"Operation {method.upper()} {path} has no response definitions"
                                )
                            else:
                                # Check for standard status codes
                                has_standard = any(code in responses for code in standard_status_codes)
                                if not has_standard:
                                    check["warnings"].append(
                                        f"Operation {method.upper()} {path} missing standard status codes"
                                    )
        
        return check
    
    def _check_security_definitions(self, spec: Dict) -> Dict[str, Any]:
        """Check security definitions."""
        check = {"valid": True, "errors": [], "warnings": []}
        
        components = spec.get("components", {})
        security_schemes = components.get("securitySchemes", {})
        
        if not security_schemes:
            check["warnings"].append("No security schemes defined")
        else:
            # Check for standard security schemes
            standard_types = ["oauth2", "openIdConnect", "http", "apiKey"]
            found_standard = False
            
            for scheme_name, scheme in security_schemes.items():
                if isinstance(scheme, dict):
                    scheme_type = scheme.get("type", "")
                    if scheme_type in standard_types:
                        found_standard = True
                        if scheme_type == "oauth2":
                            flows = scheme.get("flows", {})
                            if not flows:
                                check["warnings"].append(
                                    f"OAuth2 scheme '{scheme_name}' missing flows"
                                )
            
            if not found_standard:
                check["warnings"].append("No standard security schemes found")
        
        return check
    
    def _check_documentation(self, spec: Dict) -> Dict[str, Any]:
        """Check API documentation."""
        check = {"valid": True, "errors": [], "warnings": []}
        
        info = spec.get("info", {})
        
        # Check required info fields
        if "description" not in info:
            check["warnings"].append("API description missing")
        
        if "contact" not in info:
            check["warnings"].append("API contact information missing")
        
        # Check operation descriptions
        paths = spec.get("paths", {})
        operations_without_desc = 0
        
        for path, path_item in paths.items():
            if isinstance(path_item, dict):
                for method, operation in path_item.items():
                    if method.lower() in ["get", "post", "put", "patch", "delete"]:
                        if isinstance(operation, dict) and "description" not in operation:
                            operations_without_desc += 1
        
        if operations_without_desc > 0:
            check["warnings"].append(
                f"{operations_without_desc} operations missing descriptions"
            )
        
        return check
    
    def _check_authorization_endpoint(self, endpoints: List[Dict]) -> Dict[str, Any]:
        """Check for OAuth authorization endpoint."""
        check = {"valid": False, "errors": [], "warnings": []}
        
        auth_endpoints = [
            ep for ep in endpoints
            if "authorize" in ep.get("path", "").lower() or
               "auth" in ep.get("path", "").lower()
        ]
        
        if not auth_endpoints:
            check["errors"].append("OAuth authorization endpoint not found")
        else:
            check["valid"] = True
            check["endpoint"] = auth_endpoints[0].get("path")
        
        return check
    
    def _check_token_endpoint(self, endpoints: List[Dict]) -> Dict[str, Any]:
        """Check for OAuth token endpoint."""
        check = {"valid": False, "errors": [], "warnings": []}
        
        token_endpoints = [
            ep for ep in endpoints
            if "token" in ep.get("path", "").lower()
        ]
        
        if not token_endpoints:
            check["errors"].append("OAuth token endpoint not found")
        else:
            check["valid"] = True
            check["endpoint"] = token_endpoints[0].get("path")
        
        return check
    
    def _check_grant_types(self, endpoints: List[Dict]) -> Dict[str, Any]:
        """Check OAuth grant types."""
        check = {"valid": True, "errors": [], "warnings": []}
        
        standard_grants = ["authorization_code", "client_credentials", "refresh_token"]
        config = endpoints[0].get("oauth_config", {}) if endpoints else {}
        supported_grants = config.get("grant_types", [])
        
        if not supported_grants:
            check["warnings"].append("No OAuth grant types specified")
        else:
            has_standard = any(grant in standard_grants for grant in supported_grants)
            if not has_standard:
                check["warnings"].append("No standard OAuth grant types found")
        
        return check
    
    def _check_token_format(self, endpoints: List[Dict]) -> Dict[str, Any]:
        """Check token format."""
        check = {"valid": True, "errors": [], "warnings": []}
        
        config = endpoints[0].get("oauth_config", {}) if endpoints else {}
        token_type = config.get("token_type", "").upper()
        
        if token_type != "BEARER":
            check["warnings"].append(f"Token type '{token_type}' - standard is 'Bearer'")
        
        return check
    
    def _check_security_headers(self, endpoints: List[Dict]) -> Dict[str, Any]:
        """Check security headers."""
        check = {"valid": True, "errors": [], "warnings": []}
        
        required_headers = ["Content-Type", "Authorization"]
        
        for endpoint in endpoints:
            headers = endpoint.get("headers", [])
            missing = [h for h in required_headers if h not in headers]
            if missing:
                check["warnings"].append(
                    f"Endpoint {endpoint.get('path')} missing headers: {', '.join(missing)}"
                )
        
        return check
    
    def _check_versioning_strategy(self, strategy: str) -> Dict[str, Any]:
        """Check versioning strategy."""
        check = {"valid": False, "errors": [], "warnings": []}
        
        valid_strategies = ["url", "header", "query", "media_type"]
        
        if strategy == "none":
            check["errors"].append("No API versioning strategy defined")
        elif strategy not in valid_strategies:
            check["warnings"].append(f"Versioning strategy '{strategy}' - consider standard approaches")
        else:
            check["valid"] = True
            check["strategy"] = strategy
        
        return check
    
    def _check_version_format(self, version: Optional[str]) -> Dict[str, Any]:
        """Check version format."""
        check = {"valid": True, "errors": [], "warnings": []}
        
        if not version:
            check["warnings"].append("Current API version not specified")
        else:
            # Check semantic versioning
            semver_pattern = r'^\d+\.\d+(\.\d+)?(-[a-zA-Z0-9]+)?(\+[a-zA-Z0-9]+)?$'
            if not re.match(semver_pattern, version):
                check["warnings"].append(
                    f"Version '{version}' - consider semantic versioning (e.g., 1.0.0)"
                )
        
        return check
    
    def _check_backward_compatibility(self, current: Optional[str], supported: List[str]) -> Dict[str, Any]:
        """Check backward compatibility."""
        check = {"valid": True, "errors": [], "warnings": []}
        
        if not supported:
            check["warnings"].append("No supported versions specified")
        elif current and current not in supported:
            check["warnings"].append(f"Current version '{current}' not in supported versions list")
        
        return check
    
    def _check_deprecation_policy(self, config: Dict) -> Dict[str, Any]:
        """Check deprecation policy."""
        check = {"valid": True, "errors": [], "warnings": []}
        
        if "deprecation_policy" not in config:
            check["warnings"].append("No API deprecation policy defined")
        else:
            policy = config["deprecation_policy"]
            if "notice_period" not in policy:
                check["warnings"].append("Deprecation policy missing notice period")
        
        return check
    
    def generate_report(self) -> str:
        """Generate validation report."""
        report_lines = [
            "=" * 60,
            "API Standardization Validation Report",
            "=" * 60,
            ""
        ]
        
        for result in self.check_results:
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
        description="Validate API standardization compliance"
    )
    parser.add_argument("--openapi", help="Path to OpenAPI specification file")
    parser.add_argument("--endpoints", help="Path to API endpoints JSON file")
    parser.add_argument("--oauth", action="store_true", help="Check OAuth compliance")
    parser.add_argument("--versioning", help="Path to API versioning configuration JSON file")
    parser.add_argument("--output", help="Output file for report")
    
    args = parser.parse_args()
    
    checker = APIChecker()
    
    if args.openapi:
        print(f"Validating OpenAPI specification: {args.openapi}")
        result = checker.validate_openapi(args.openapi)
        print(f"OpenAPI Validation: {'✓ VALID' if result['valid'] else '✗ INVALID'}")
    
    if args.endpoints and args.oauth:
        print(f"Checking OAuth compliance: {args.endpoints}")
        with open(args.endpoints, 'r') as f:
            endpoints = json.load(f)
        result = checker.check_oauth_compliance(endpoints)
        print(f"OAuth Compliance: {'✓ VALID' if result['valid'] else '✗ INVALID'}")
    
    if args.versioning:
        print(f"Verifying versioning: {args.versioning}")
        with open(args.versioning, 'r') as f:
            config = json.load(f)
        result = checker.verify_versioning(config)
        print(f"Versioning: {'✓ VALID' if result['valid'] else '✗ INVALID'}")
    
    # Generate report
    report = checker.generate_report()
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"\nReport saved to: {args.output}")
    else:
        print("\n" + report)


if __name__ == "__main__":
    main()
