#!/usr/bin/env python3
"""
Port Scanner
A simple yet effective port scanner for network reconnaissance
"""

import socket
import sys
from datetime import datetime
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import ipaddress

class PortScanner:
    def __init__(self, target, timeout=1, threads=100):
        """
        Initialize the port scanner
        
        Args:
            target: IP address or hostname to scan
            timeout: Socket timeout in seconds
            threads: Number of concurrent threads
        """
        self.target = target
        self.timeout = timeout
        self.threads = threads
        self.open_ports = []
        
    def resolve_target(self):
        """Resolve hostname to IP address"""
        try:
            self.ip = socket.gethostbyname(self.target)
            return True
        except socket.gaierror:
            print(f"[!] Error: Could not resolve hostname {self.target}")
            return False
    
    def scan_port(self, port):
        """
        Scan a single port
        
        Args:
            port: Port number to scan
            
        Returns:
            Port number if open, None otherwise
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((self.ip, port))
            sock.close()
            
            if result == 0:
                return port
            return None
        except socket.error:
            return None
    
    def get_service_name(self, port):
        """Get common service name for a port"""
        try:
            return socket.getservbyport(port)
        except:
            return "unknown"
    
    def scan_range(self, start_port, end_port, verbose=False):
        """
        Scan a range of ports using multithreading
        
        Args:
            start_port: Starting port number
            end_port: Ending port number
            verbose: Show all attempted ports
        """
        print(f"\n[*] Starting scan on {self.target} ({self.ip})")
        print(f"[*] Scanning ports {start_port}-{end_port}")
        print(f"[*] Scan started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        total_ports = end_port - start_port + 1
        scanned = 0
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            future_to_port = {
                executor.submit(self.scan_port, port): port 
                for port in range(start_port, end_port + 1)
            }
            
            for future in as_completed(future_to_port):
                port = future_to_port[future]
                scanned += 1
                
                try:
                    result = future.result()
                    if result:
                        service = self.get_service_name(result)
                        print(f"[+] Port {result:5d} - OPEN ({service})")
                        self.open_ports.append(result)
                    elif verbose:
                        print(f"[-] Port {port:5d} - CLOSED")
                except Exception as e:
                    if verbose:
                        print(f"[!] Port {port:5d} - ERROR: {str(e)}")
                
                # Progress indicator
                if scanned % 100 == 0:
                    progress = (scanned / total_ports) * 100
                    print(f"[*] Progress: {progress:.1f}% ({scanned}/{total_ports})")
        
        print(f"\n[*] Scan completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"[*] Found {len(self.open_ports)} open ports")
        
        if self.open_ports:
            print(f"\n[*] Open ports: {', '.join(map(str, sorted(self.open_ports)))}")
    
    def scan_common_ports(self):
        """Scan common ports (top 100)"""
        common_ports = [
            20, 21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993,
            995, 1723, 3306, 3389, 5900, 8080, 8443
        ]
        
        print(f"\n[*] Scanning common ports on {self.target} ({self.ip})")
        print(f"[*] Scan started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        for port in common_ports:
            result = self.scan_port(port)
            if result:
                service = self.get_service_name(result)
                print(f"[+] Port {result:5d} - OPEN ({service})")
                self.open_ports.append(result)
        
        print(f"\n[*] Scan completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"[*] Found {len(self.open_ports)} open ports")


def main():
    parser = argparse.ArgumentParser(
        description="Simple and effective port scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -t 192.168.1.1                    # Scan common ports
  %(prog)s -t example.com -p 1-1000          # Scan ports 1-1000
  %(prog)s -t 192.168.1.1 -p 80,443,8080     # Scan specific ports
  %(prog)s -t 192.168.1.1 -p 1-65535 -v      # Full scan with verbose output
        """
    )
    
    parser.add_argument('-t', '--target', required=True, 
                       help='Target IP address or hostname')
    parser.add_argument('-p', '--ports', 
                       help='Port range (e.g., 1-1000) or specific ports (e.g., 80,443)')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Show all ports (open and closed)')
    parser.add_argument('--timeout', type=float, default=1,
                       help='Socket timeout in seconds (default: 1)')
    parser.add_argument('--threads', type=int, default=100,
                       help='Number of threads (default: 100)')
    
    args = parser.parse_args()
    
    # Banner
    print("=" * 60)
    print("Port Scanner v1.0")
    print("=" * 60)
    
    # Initialize scanner
    scanner = PortScanner(args.target, timeout=args.timeout, threads=args.threads)
    
    # Resolve target
    if not scanner.resolve_target():
        sys.exit(1)
    
    try:
        if args.ports:
            # Parse port specification
            if '-' in args.ports:
                # Port range
                start, end = map(int, args.ports.split('-'))
                scanner.scan_range(start, end, verbose=args.verbose)
            elif ',' in args.ports:
                # Specific ports
                ports = [int(p.strip()) for p in args.ports.split(',')]
                print(f"\n[*] Scanning specific ports on {args.target} ({scanner.ip})")
                print(f"[*] Ports: {', '.join(map(str, ports))}\n")
                
                for port in ports:
                    result = scanner.scan_port(port)
                    if result:
                        service = scanner.get_service_name(result)
                        print(f"[+] Port {result:5d} - OPEN ({service})")
                        scanner.open_ports.append(result)
                    elif args.verbose:
                        print(f"[-] Port {port:5d} - CLOSED")
            else:
                # Single port
                port = int(args.ports)
                result = scanner.scan_port(port)
                if result:
                    service = scanner.get_service_name(result)
                    print(f"[+] Port {result} is OPEN ({service})")
                else:
                    print(f"[-] Port {port} is CLOSED")
        else:
            # Scan common ports
            scanner.scan_common_ports()
            
    except KeyboardInterrupt:
        print("\n\n[!] Scan interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
