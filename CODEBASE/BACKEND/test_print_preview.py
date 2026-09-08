"""
Test script to verify print preview in browser.
Opens the public result page and validates A4 layout.
"""

import webbrowser
import time

# Test with a known student (from seed data)
ROLL_NUMBER = "2024001"  # Rohit Sharma
DOB = "2005-02-15"

print("=" * 60)
print("PRINT PREVIEW TEST")
print("=" * 60)
print()
print("This script will:")
print("1. Open the public result lookup page")
print("2. You need to manually enter:")
print(f"   Roll Number: {ROLL_NUMBER}")
print(f"   Date of Birth: {DOB}")
print("3. Then open Print Preview (Ctrl+P / Cmd+P)")
print("4. Verify:")
print("   - Page count is exactly 1/1")
print("   - All 6 subjects visible")
print("   - All 7 table columns visible")
print("   - Professional academic document appearance")
print("   - No clipping or overlap")
print()
print("=" * 60)

# Open the lookup page
url = "http://127.0.0.1:5000/results/lookup"
print(f"\nOpening: {url}")
print()
webbrowser.open(url)

print("Please test the print preview and report results.")
print()
print("Expected credentials:")
print(f"  Roll Number: {ROLL_NUMBER}")
print(f"  Date of Birth: 15/02/2005")
