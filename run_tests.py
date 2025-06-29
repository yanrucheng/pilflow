#!/usr/bin/env python3
"""
Run all tests for the pilflow package with coverage reporting.

This script runs pytest with coverage reporting and generates a coverage report.

Usage:
    python run_tests.py [--html] [--xml]

Options:
    --html: Generate HTML coverage report
    --xml: Generate XML coverage report
"""

import sys
import subprocess
import argparse

def main():
    parser = argparse.ArgumentParser(description='Run tests for pilflow with coverage reporting')
    parser.add_argument('--html', action='store_true', help='Generate HTML coverage report')
    parser.add_argument('--xml', action='store_true', help='Generate XML coverage report')
    args = parser.parse_args()
    
    # Base command to run tests with coverage
    cmd = ['python', '-m', 'pytest', '--cov=pilflow', '--cov-report=term']
    
    # Add HTML coverage report if requested
    if args.html:
        cmd.append('--cov-report=html')
    
    # Add XML coverage report if requested
    if args.xml:
        cmd.append('--cov-report=xml')
    
    # Run the tests
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    
    # Return the exit code from pytest
    return result.returncode

if __name__ == '__main__':
    sys.exit(main())