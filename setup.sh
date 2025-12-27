#!/bin/bash
# Quick setup and test script for Port Scanner

echo "=========================================="
echo "Port Scanner - Quick Setup"
echo "=========================================="
echo ""

# Check Python version
echo "[*] Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "[+] Found: $PYTHON_VERSION"
else
    echo "[!] Error: Python 3 not found"
    echo "    Please install Python 3.6 or higher"
    exit 1
fi

# Make scanner executable
echo ""
echo "[*] Making port_scanner.py executable..."
chmod +x port_scanner.py
echo "[+] Done"

# Test help command
echo ""
echo "[*] Testing help command..."
python3 port_scanner.py --help
if [ $? -eq 0 ]; then
    echo "[+] Help command works!"
else
    echo "[!] Error running help command"
    exit 1
fi

# Quick test scan
echo ""
echo "[*] Running quick test scan on localhost..."
echo "    (This will scan a few common ports)"
echo ""
python3 port_scanner.py -t 127.0.0.1 -p 80,443,8080

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Try these commands:"
echo "  python3 port_scanner.py -t 127.0.0.1"
echo "  python3 port_scanner.py -t example.com -p 1-1000"
echo "  python3 port_scanner.py --help"
echo ""
echo "See README.md for more usage examples"
