#!/usr/bin/env python3
"""
Example usage scenarios for the port scanner
Run these examples to see the scanner in action
"""

import subprocess
import sys

def run_example(description, command):
    """Run an example command"""
    print(f"\n{'='*60}")
    print(f"Example: {description}")
    print(f"Command: {command}")
    print('='*60)
    
    response = input("Run this example? (y/n): ")
    if response.lower() == 'y':
        subprocess.run(command, shell=True)
        input("\nPress Enter to continue...")

def main():
    print("""
    Port Scanner - Example Usage
    =============================
    
    These examples demonstrate different scanning modes.
    Make sure you have permission before scanning any target!
    """)
    
    # Example 1: Common ports
    run_example(
        "Scan common ports on localhost",
        "python3 ../port_scanner.py -t 127.0.0.1"
    )
    
    # Example 2: Port range
    run_example(
        "Scan port range 1-100",
        "python3 ../port_scanner.py -t 127.0.0.1 -p 1-100"
    )
    
    # Example 3: Specific ports
    run_example(
        "Scan specific ports (80, 443, 8080)",
        "python3 ../port_scanner.py -t 127.0.0.1 -p 80,443,8080"
    )
    
    # Example 4: Verbose mode
    run_example(
        "Scan with verbose output",
        "python3 ../port_scanner.py -t 127.0.0.1 -p 1-50 -v"
    )
    
    # Example 5: Custom settings
    run_example(
        "Fast scan with custom timeout and threads",
        "python3 ../port_scanner.py -t 127.0.0.1 -p 1-1000 --timeout 0.5 --threads 200"
    )
    
    print("\n" + "="*60)
    print("Examples complete!")
    print("="*60)

if __name__ == "__main__":
    main()
