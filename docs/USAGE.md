# Usage Guide

Complete guide to using the Port Scanner effectively.

## Table of Contents

- [Basic Usage](#basic-usage)
- [Scan Modes](#scan-modes)
- [Advanced Options](#advanced-options)
- [Output Interpretation](#output-interpretation)
- [Performance Tuning](#performance-tuning)
- [Common Use Cases](#common-use-cases)
- [Troubleshooting](#troubleshooting)

## Basic Usage

The simplest way to scan a target:

```bash
python3 port_scanner.py -t TARGET
```

This scans common ports on the target.

## Scan Modes

### Common Ports Scan

Quickly scan the most frequently used ports:

```bash
python3 port_scanner.py -t 192.168.1.1
```

Scans ports: 20, 21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080, 8443

### Port Range Scan

Scan a continuous range of ports:

```bash
python3 port_scanner.py -t example.com -p 1-1000
```

### Specific Ports

Scan particular ports you're interested in:

```bash
python3 port_scanner.py -t 192.168.1.1 -p 22,80,443,3306,8080
```

### Full Port Scan

Scan all 65535 ports (takes a while):

```bash
python3 port_scanner.py -t 192.168.1.1 -p 1-65535
```

## Advanced Options

### Verbose Mode

See all ports (both open and closed):

```bash
python3 port_scanner.py -t 192.168.1.1 -p 1-100 -v
```

### Custom Timeout

Adjust socket timeout (in seconds):

```bash
python3 port_scanner.py -t 192.168.1.1 -p 1-1000 --timeout 0.5
```

Lower timeout = faster scan, but may miss slow-responding ports.

### Thread Count

Control number of concurrent threads:

```bash
python3 port_scanner.py -t 192.168.1.1 -p 1-5000 --threads 200
```

More threads = faster, but don't go too high or you'll hit rate limits.

## Output Interpretation

### Standard Output

```
[*] Starting scan on example.com (93.184.216.34)
[*] Scanning ports 1-1000
[*] Scan started at 2024-12-27 10:30:45

[+] Port    80 - OPEN (http)
[+] Port   443 - OPEN (https)
```

- `[*]` = Information
- `[+]` = Open port found
- `[-]` = Closed port (verbose mode only)
- `[!]` = Error or warning

### Service Names

The scanner attempts to identify the service running on each open port:

- `http` = Web server
- `https` = Secure web server
- `ssh` = Secure shell
- `ftp` = File transfer
- `mysql` = MySQL database
- `unknown` = Service not recognized

## Performance Tuning

### Fast Local Network Scan

```bash
python3 port_scanner.py -t 192.168.1.1 -p 1-65535 --timeout 0.3 --threads 300
```

### Careful Internet Scan

```bash
python3 port_scanner.py -t example.com -p 1-1000 --timeout 2 --threads 50
```

### Recommended Settings

| Network Type | Timeout | Threads |
|--------------|---------|---------|
| Local LAN    | 0.3-0.5 | 200-500 |
| Internet     | 1-2     | 50-100  |
| Slow/Remote  | 2-5     | 20-50   |

## Common Use Cases

### Web Server Check

```bash
python3 port_scanner.py -t mywebsite.com -p 80,443,8080,8443
```

### Database Server Audit

```bash
python3 port_scanner.py -t dbserver.local -p 3306,5432,1433,27017
```

### Network Device Scan

```bash
python3 port_scanner.py -t 192.168.1.1 -p 22,23,80,443,161,8080
```

### Quick Security Check

```bash
python3 port_scanner.py -t yourserver.com -p 21,22,23,25,3389
```

### Comprehensive Audit

```bash
python3 port_scanner.py -t 192.168.1.100 -p 1-65535 --threads 200 > scan_results.txt
```

## Troubleshooting

### No Ports Found

- Check if target is reachable: `ping TARGET`
- Try increasing timeout: `--timeout 3`
- Verify you're scanning the right IP/hostname
- Check firewall rules aren't blocking your scans

### Scan Too Slow

- Increase threads: `--threads 200`
- Decrease timeout: `--timeout 0.5`
- Scan smaller port ranges
- Check your network connection speed

### Permission Errors

- Run with appropriate permissions
- Some systems require root/admin for raw sockets
- Check local firewall settings

### Connection Refused vs Timeout

- Connection refused = port is closed but host is up
- Timeout = port is filtered or host is down
- Both show as closed in standard mode

### Rate Limiting

If you're being rate limited:
- Reduce thread count: `--threads 25`
- Increase timeout: `--timeout 2`
- Scan smaller ranges at a time
- Add delays between scans

## Tips

1. Always get permission before scanning
2. Start with common ports, then expand if needed
3. Save important scan results to a file
4. Use verbose mode for troubleshooting
5. Adjust threads based on your network
6. Don't scan all 65535 ports unless necessary
7. Monitor your network impact
8. Keep scan logs for compliance

## Examples Repository

See the `examples/` directory for more usage scenarios and scripts.
