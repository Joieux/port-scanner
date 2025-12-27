# Installation Guide

## Prerequisites

- Python 3.6 or higher
- No external dependencies required

## Quick Install

### Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/port-scanner.git
cd port-scanner
```

### Make Executable

```bash
chmod +x port_scanner.py
```

### Test Installation

```bash
python3 port_scanner.py -t 127.0.0.1
```

## Installation Methods

### Method 1: Direct Use

Simply download `port_scanner.py` and run it:

```bash
python3 port_scanner.py -t TARGET -p PORTS
```

### Method 2: Add to PATH

Make it available system-wide:

```bash
# Copy to a directory in your PATH
sudo cp port_scanner.py /usr/local/bin/port-scanner

# Make executable
sudo chmod +x /usr/local/bin/port-scanner

# Now you can run it from anywhere
port-scanner -t 192.168.1.1
```

### Method 3: Create Alias

Add to your `~/.bashrc` or `~/.zshrc`:

```bash
alias portscan='python3 /path/to/port_scanner.py'
```

Then reload your shell:

```bash
source ~/.bashrc
```

Now you can use:

```bash
portscan -t 192.168.1.1 -p 1-1000
```

## Verify Installation

Check Python version:

```bash
python3 --version
```

Should be 3.6 or higher.

Run help command:

```bash
python3 port_scanner.py --help
```

## Troubleshooting

### Permission Denied

If you get permission errors:

```bash
chmod +x port_scanner.py
```

### Python Not Found

Make sure Python 3 is installed:

```bash
# On Ubuntu/Debian
sudo apt-get install python3

# On macOS
brew install python3

# On Windows
# Download from python.org
```

### Module Import Errors

The scanner uses only standard library modules. If you get import errors, your Python installation may be incomplete. Reinstall Python.

## Uninstall

Simply delete the files:

```bash
rm -rf port-scanner/
```

If you installed to PATH:

```bash
sudo rm /usr/local/bin/port-scanner
```

## Next Steps

See [README.md](README.md) for usage examples and documentation.
