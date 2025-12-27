# Port Scanner

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-lightgrey)

A clean, multithreaded Python port scanner for network reconnaissance and security auditing.

> ⚠️ **Legal Notice**: Only scan networks and systems you own or have explicit permission to test. Unauthorized scanning may be illegal in your jurisdiction.

## Features

- Fast multithreaded scanning
- Scan port ranges or specific ports
- Common ports quick scan
- Service detection
- Progress tracking
- Verbose mode
- Customizable timeout and thread count

## Table of Contents

- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## Quick Start

```bash
# Clone the repository
git clone https://github.com/YOUR-USERNAME/port-scanner.git
cd port-scanner

# Run the quick setup
chmod +x setup.sh
./setup.sh

# Start scanning
python3 port_scanner.py -t 192.168.1.1
```

## Installation

### Prerequisites

- Python 3.6+
- No external dependencies (uses only standard library)

### Clone and Setup

```bash
git clone https://github.com/YOUR-USERNAME/port-scanner.git
cd port-scanner
chmod +x port_scanner.py setup.sh
./setup.sh
```

For detailed installation instructions, see [docs/INSTALL.md](docs/INSTALL.md).

## Usage

### Basic Scan (Common Ports)

Scan the most common ports:

```bash
python3 port_scanner.py -t 192.168.1.1
```

### Port Range Scan

Scan a range of ports:

```bash
python3 port_scanner.py -t example.com -p 1-1000
```

### Specific Ports

Scan specific ports:

```bash
python3 port_scanner.py -t 192.168.1.1 -p 80,443,8080,3306
```

### Full Port Scan

Scan all ports (this will take a while):

```bash
python3 port_scanner.py -t 192.168.1.1 -p 1-65535
```

### Verbose Mode

Show both open and closed ports:

```bash
python3 port_scanner.py -t 192.168.1.1 -p 1-1000 -v
```

### Custom Settings

Adjust timeout and thread count:

```bash
python3 port_scanner.py -t 192.168.1.1 -p 1-5000 --timeout 0.5 --threads 200
```

## Command Line Options

```
-t, --target    Target IP address or hostname (required)
-p, --ports     Port range (1-1000) or specific ports (80,443)
-v, --verbose   Show all ports (open and closed)
--timeout       Socket timeout in seconds (default: 1)
--threads       Number of concurrent threads (default: 100)
```

For detailed usage guide, see [docs/USAGE.md](docs/USAGE.md).

## Examples

```
============================================================
Port Scanner v1.0
============================================================

[*] Starting scan on example.com (93.184.216.34)
[*] Scanning ports 1-1000
[*] Scan started at 2024-12-27 10:30:45

[+] Port    80 - OPEN (http)
[+] Port   443 - OPEN (https)
[*] Progress: 50.0% (500/1000)
[*] Progress: 100.0% (1000/1000)

[*] Scan completed at 2024-12-27 10:31:12
[*] Found 2 open ports

[*] Open ports: 80, 443
```

## Legal Notice

This tool is for educational purposes and authorized security testing only. Always ensure you have permission before scanning any network or system. Unauthorized port scanning may be illegal in your jurisdiction.

## Documentation

- [Installation Guide](docs/INSTALL.md) - Detailed installation instructions
- [Usage Guide](docs/USAGE.md) - Comprehensive usage documentation
- [Changelog](CHANGELOG.md) - Version history and updates

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
git clone https://github.com/YOUR-USERNAME/port-scanner.git
cd port-scanner
# Make your changes
# Test thoroughly
# Submit a pull request
```

## How It Works

The scanner uses Python's socket library to attempt TCP connections to specified ports. Multithreading allows for fast concurrent scanning of multiple ports. When a connection succeeds, the port is marked as open and the service name is resolved if available.

## Roadmap

- [ ] UDP port scanning
- [ ] OS fingerprinting
- [ ] Banner grabbing
- [ ] Output to JSON/CSV formats
- [ ] Configuration file support
- [ ] Stealth scanning modes

## Support

- 📖 [Documentation](docs/)
- 🐛 [Report Bug](https://github.com/YOUR-USERNAME/port-scanner/issues)
- 💡 [Request Feature](https://github.com/YOUR-USERNAME/port-scanner/issues)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with Python's standard library
- Inspired by classic network scanning tools
- Created for educational and security research purposes

---

**Remember**: With great power comes great responsibility. Use this tool ethically and legally.
