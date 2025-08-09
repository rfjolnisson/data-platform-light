#!/usr/bin/env python3
"""
Environment validation script.

Checks:
- Required environment variables are set
- API connectivity to all sources
- Write permissions to Bronze directory
- Python dependencies are installed
"""

import os
import sys
import requests
from pathlib import Path
from typing import List, Tuple, Dict, Any
import yaml


def check_env_vars() -> List[Tuple[str, bool, str]]:
    """Check if all required environment variables are set."""
    required_vars = [
        "JIRA_URL",
        "JIRA_EMAIL", 
        "JIRA_API_TOKEN",
        "BITBUCKET_WORKSPACE",
        "BITBUCKET_USERNAME",
        "BITBUCKET_APP_PASSWORD",
        "JENKINS_URL",
        "JENKINS_USERNAME",
        "JENKINS_API_TOKEN"
    ]
    
    results = []
    for var in required_vars:
        value = os.getenv(var)
        is_set = value is not None and value.strip() != ""
        message = "✓ Set" if is_set else "✗ Missing or empty"
        results.append((var, is_set, message))
    
    return results


def check_api_connectivity() -> List[Tuple[str, bool, str]]:
    """Test API connectivity to all sources."""
    results = []
    
    # Test Jira
    try:
        jira_url = os.getenv("JIRA_URL")
        jira_email = os.getenv("JIRA_EMAIL")
        jira_token = os.getenv("JIRA_API_TOKEN")
        
        if all([jira_url, jira_email, jira_token]):
            response = requests.get(
                f"{jira_url}/rest/api/3/myself",
                auth=(jira_email, jira_token),
                timeout=10
            )
            if response.status_code == 200:
                results.append(("Jira API", True, "✓ Connected"))
            else:
                results.append(("Jira API", False, f"✗ HTTP {response.status_code}"))
        else:
            results.append(("Jira API", False, "✗ Missing credentials"))
    except Exception as e:
        results.append(("Jira API", False, f"✗ Error: {str(e)[:50]}"))
    
    # Test Bitbucket
    try:
        bb_workspace = os.getenv("BITBUCKET_WORKSPACE")
        bb_username = os.getenv("BITBUCKET_USERNAME")
        bb_password = os.getenv("BITBUCKET_APP_PASSWORD")
        
        if all([bb_workspace, bb_username, bb_password]):
            response = requests.get(
                f"https://api.bitbucket.org/2.0/workspaces/{bb_workspace}",
                auth=(bb_username, bb_password),
                timeout=10
            )
            if response.status_code == 200:
                results.append(("Bitbucket API", True, "✓ Connected"))
            else:
                results.append(("Bitbucket API", False, f"✗ HTTP {response.status_code}"))
        else:
            results.append(("Bitbucket API", False, "✗ Missing credentials"))
    except Exception as e:
        results.append(("Bitbucket API", False, f"✗ Error: {str(e)[:50]}"))
    
    # Test Jenkins
    try:
        jenkins_url = os.getenv("JENKINS_URL")
        jenkins_username = os.getenv("JENKINS_USERNAME")
        jenkins_token = os.getenv("JENKINS_API_TOKEN")
        
        if all([jenkins_url, jenkins_username, jenkins_token]):
            response = requests.get(
                f"{jenkins_url}/api/json",
                auth=(jenkins_username, jenkins_token),
                timeout=10
            )
            if response.status_code == 200:
                results.append(("Jenkins API", True, "✓ Connected"))
            else:
                results.append(("Jenkins API", False, f"✗ HTTP {response.status_code}"))
        else:
            results.append(("Jenkins API", False, "✗ Missing credentials"))
    except Exception as e:
        results.append(("Jenkins API", False, f"✗ Error: {str(e)[:50]}"))
    
    return results


def check_directories() -> List[Tuple[str, bool, str]]:
    """Check directory structure and write permissions."""
    results = []
    
    # Check Bronze directory
    bronze_dir = Path("./bronze")
    try:
        bronze_dir.mkdir(parents=True, exist_ok=True)
        # Test write permission
        test_file = bronze_dir / ".test_write"
        test_file.write_text("test")
        test_file.unlink()
        results.append(("Bronze directory", True, "✓ Writable"))
    except Exception as e:
        results.append(("Bronze directory", False, f"✗ Error: {str(e)[:50]}"))
    
    # Check config directory
    config_dir = Path("./config")
    if config_dir.exists():
        results.append(("Config directory", True, "✓ Exists"))
    else:
        results.append(("Config directory", False, "✗ Missing"))
    
    return results


def check_dependencies() -> List[Tuple[str, bool, str]]:
    """Check if required Python packages are installed."""
    results = []
    
    # Test packages that are safe to import
    safe_packages = [
        "requests", 
        "yaml",
        "pandas",
        "pyarrow"
    ]
    
    for package in safe_packages:
        try:
            __import__(package)
            results.append((f"Python: {package}", True, "✓ Installed"))
        except ImportError:
            results.append((f"Python: {package}", False, "✗ Not installed"))
    
    # Test dlt using subprocess to avoid import issues
    try:
        import subprocess
        result = subprocess.run(["python3", "-c", "import dlt; print(dlt.__version__)"], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version = result.stdout.strip()
            results.append((f"Python: dlt", True, f"✓ Installed (v{version})"))
        else:
            results.append((f"Python: dlt", False, "✗ Import failed"))
    except Exception as e:
        results.append((f"Python: dlt", False, f"✗ Error: {str(e)[:30]}"))
    
    return results


def main():
    """Run all validation checks."""
    print("🔍 Data Platform Light - Environment Validation")
    print("=" * 50)
    
    all_checks = [
        ("Environment Variables", check_env_vars()),
        ("API Connectivity", check_api_connectivity()),
        ("Directories & Permissions", check_directories()),
        ("Python Dependencies", check_dependencies())
    ]
    
    total_passed = 0
    total_checks = 0
    
    for section_name, checks in all_checks:
        print(f"\n{section_name}:")
        section_passed = 0
        
        for name, passed, message in checks:
            print(f"  {name:<25} {message}")
            if passed:
                section_passed += 1
            total_checks += 1
        
        total_passed += section_passed
        print(f"  → {section_passed}/{len(checks)} passed")
    
    print("\n" + "=" * 50)
    print(f"Overall: {total_passed}/{total_checks} checks passed")
    
    if total_passed == total_checks:
        print("🎉 All checks passed! Ready to run data pipelines.")
        return 0
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
