"""#!/usr/bin/env python3
"""
"""
Port Scanner v1.2

Enhancements in this commit:
 - Banner grabbing for open ports (plain/TLS-aware for common HTTP ports)
 - Basic service detection using port mapping and banner keyword heuristics
 - CLI flags: --banner and --service-detect to enable these features
 - Scan results (JSON/text) now include banners and detected services

Notes:
 - Banner grabbing attempts to be conservative and only sends small probes for HTTP-like ports.
 - TLS-aware banner grabbing uses the ssl module for ports such as 443/8443.
 - Service detection combines socket.getservbyport and banner keyword matching; it's heuristic.
"""

import argparse
import ipaddress
import json
import socket
import sys
import os
import ssl
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import List, Optional, Tuple

COMMON_PORTS = [
    20, 21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993,
    995, 1723, 3306, 3389, 5900, 8080, 8443
]

class PortScanner:
    def __init__(self, target: str, timeout: float = 1.0, threads: int = 100):
        """
        target: a hostname or IP string (IPv4/IPv6)
        """
        self.target = target
        self.timeout = timeout
        self.threads = threads
        self.open_ports: List[int] = []
        self.banners: dict = {}
        self.detected_services: dict = {}
        self.addr: Optional[str] = None    # textual IP address we will connect to
        self.family: Optional[int] = None  # socket.AF_INET or AF_INET6

    def resolve_target(self) -> bool:
        """
        Resolve the provided target into an IP address and detect address family.
        - If target is a literal IP, set family directly.
        - Otherwise, perform DNS resolution (getaddrinfo) and pick the first usable result.
        Returns True on success, False on failure.
        """
        # If it's a literal IP, ipaddress will parse it
        try:
            ip_obj = ipaddress.ip_address(self.target)
            self.addr = str(ip_obj)
            self.family = socket.AF_INET6 if ip_obj.version == 6 else socket.AF_INET
            return True
        except ValueError:
            # Not a literal IP; attempt DNS resolution
            try:
                # getaddrinfo(target, None) returns tuples including (family, ..., sockaddr)
                infos = socket.getaddrinfo(self.target, None, type=socket.SOCK_STREAM)
                # prefer AF_INET first, but accept AF_INET6 as well
                chosen = None
                for info in infos:
                    fam, _, _, _, sockaddr = info
                    if fam in (socket.AF_INET, socket.AF_INET6):
                        chosen = info
                        break
                if not chosen:
                    print(f"[!] Error: No IPv4/IPv6 address found for {self.target}")
                    return False
                fam, _, _, _, sockaddr = chosen
                # sockaddr is like ('1.2.3.4', 0) or ('::1', 0, flow, scope)
                self.family = fam
                self.addr = sockaddr[0]
                return True
            except socket.gaierror:
                print(f"[!] Error: Could not resolve hostname {self.target}")
                return False
            except Exception as e:
                print(f"[!] Unexpected error resolving {self.target}: {e}")
                return False

    def scan_port(self, port: int) -> Optional[int]:
        """
        Attempt to connect to (self.addr, port) using the detected family.
        Returns port if open, None otherwise.
        """
        if not self.addr or not self.family:
            return None
        try:
            sock = socket.socket(self.family, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            if self.family == socket.AF_INET:
                sockaddr = (self.addr, port)
            else:
                sockaddr = (self.addr, port, 0, 0)
            result = sock.connect_ex(sockaddr)
            sock.close()
            if result == 0:
                return port
            return None
        except Exception:
            return None

    def get_service_name(self, port: int, proto: str = 'tcp') -> str:
        try:
            return socket.getservbyport(port, proto)
        except Exception:
            return "unknown"

    def grab_banner(self, port: int, banner_timeout: float = 2.0) -> Optional[str]:
        """
        Attempt to fetch a banner or initial response from the service at (addr, port).
        This function is conservative: it will only send small probes for HTTP-like ports
        and otherwise attempt to read any initial banner. It supports TLS-wrapping for
        common HTTPS ports.
        Returns a decoded banner string (stripped) or None.
        """
        if not self.addr or not self.family:
            return None
        try:
            sock = socket.socket(self.family, socket.SOCK_STREAM)
            sock.settimeout(min(self.timeout, banner_timeout))
            if self.family == socket.AF_INET:
                sockaddr = (self.addr, port)
            else:
                sockaddr = (self.addr, port, 0, 0)

            # For ports that commonly use TLS (HTTPS), attempt to wrap in SSL
            tls_ports = {443, 8443, 9443}
            http_ports = {80, 8080, 8000, 81, 8888, 8008}

            try:
                sock.connect(sockaddr)
            except Exception:
                sock.close()
                return None

            banner = b''

            # If this looks like HTTPS, try TLS handshake and an HTTP HEAD
            if port in tls_ports:
                try:
                    ctx = ssl.create_default_context()
                    tls_sock = ctx.wrap_socket(sock, server_hostname=self.target)
                    tls_sock.settimeout(min(self.timeout, banner_timeout))
                    try:
                        # Send a minimal HEAD to get a response
                        req = f"HEAD / HTTP/1.0\r\nHost: {self.target}\r\n\r\n".encode('utf-8')
                        tls_sock.sendall(req)
                        banner = tls_sock.recv(4096) or b''
                    except Exception:
                        # Even if we can't send, attempt to read server response
                        try:
                            banner = tls_sock.recv(4096) or b''
                        except Exception:
                            banner = b''
                    try:
                        tls_sock.close()
                    except Exception:
                        pass
                except Exception:
                    # TLS failed; fall back to plain read
                    try:
                        banner = sock.recv(4096) or b''
                    except Exception:
                        banner = b''
                    try:
                        sock.close()
                    except Exception:
                        pass
            else:
                # Non-TLS: for HTTP-ish ports, send a HEAD to prompt a response
                if port in http_ports:
                    try:
                        req = f"HEAD / HTTP/1.0\r\nHost: {self.target}\r\n\r\n".encode('utf-8')
                        sock.sendall(req)
                    except Exception:
                        pass
                try:
                    banner = sock.recv(4096) or b''
                except Exception:
                    banner = b''
                try:
                    sock.close()
                except Exception:
                    pass

            if not banner:
                return None
            try:
                text = banner.decode('utf-8', errors='ignore').strip()
            except Exception:
                text = str(banner)
            return text
        except Exception:
            return None

    def detect_service_from_banner(self, port: int, banner: Optional[str]) -> str:
        """
        Heuristically detect service name from port and banner contents.
        Combines getservbyport and keyword matching against banner text.
        Returns a string describing the likely service.
        """
        # Start with well-known service from port table
        svc = self.get_service_name(port)
        if svc and svc != 'unknown':
            base = svc
        else:
            base = None

        if not banner:
            return base or 'unknown'

        b = banner.lower()
        # simple keyword checks
        checks = [
            ('nginx', 'nginx'),
            ('apache', 'apache'),
            ('iis', 'iis'),
            ('tomcat', 'tomcat'),
            ('ssh', 'ssh'),
            ('smtp', 'smtp'),
            ('esmtp', 'smtp'),
            ('ftp', 'ftp'),
            ('mysql', 'mysql'),
            ('mariadb', 'mysql'),
            ('postgres', 'postgresql'),
            ('http', 'http'),
            ('http/', 'http'),
            ('ssl', 'ssl'),
            ('openssl', 'ssl'),
            ('ssh-', 'ssh'),
            ('postfix', 'smtp'),
            ('exim', 'smtp'),
            ('dovecot', 'imap/pop3'),
            ('imap', 'imap'),
            ('pop3', 'pop3'),
            ('rdp', 'rdp'),
        ]
        for key, name in checks:
            if key in b:
                if base:
                    return f"{base} ({name})"
                return name
        return base or 'unknown'

    def scan_range(self, start_port: int, end_port: int, verbose: bool = False,
                   do_banner: bool = False, do_service_detect: bool = False) -> None:
        print(f"\n[*] Starting scan on {self.target} ({self.addr})")
        print(f"[*] Scanning ports {start_port}-{end_port} using {self.threads} threads")
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
                        if do_banner:
                            banner = self.grab_banner(result)
                            if banner:
                                print(f"    Banner: {banner.splitlines()[0]}")
                                self.banners[result] = banner
                            else:
                                self.banners[result] = None
                        if do_service_detect:
                            detected = self.detect_service_from_banner(result, self.banners.get(result))
                            self.detected_services[result] = detected
                    elif verbose:
                        print(f"[-] Port {port:5d} - CLOSED")
                except Exception as e:
                    if verbose:
                        print(f"[!] Port {port:5d} - ERROR: {e}")

                if scanned % 100 == 0:
                    progress = (scanned / total_ports) * 100
                    print(f"[*] Progress: {progress:.1f}% ({scanned}/{total_ports})")

        print(f"\n[*] Scan completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"[*] Found {len(self.open_ports)} open ports")
        if self.open_ports:
            print(f"\n[*] Open ports: {', '.join(map(str, sorted(self.open_ports)))}")

    def scan_common_ports(self, do_banner: bool = False, do_service_detect: bool = False) -> None:
        print(f"\n[*] Scanning common ports on {self.target} ({self.addr})")
        print(f"[*] Scan started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        for port in COMMON_PORTS:
            result = self.scan_port(port)
            if result:
                service = self.get_service_name(result)
                print(f"[+] Port {result:5d} - OPEN ({service})")
                self.open_ports.append(result)
                if do_banner:
                    banner = self.grab_banner(result)
                    if banner:
                        print(f"    Banner: {banner.splitlines()[0]}")
                        self.banners[result] = banner
                    else:
                        self.banners[result] = None
                if do_service_detect:
                    detected = self.detect_service_from_banner(result, self.banners.get(result))
                    self.detected_services[result] = detected

        print(f"\n[*] Scan completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}" )
        print(f"[*] Found {len(self.open_ports)} open ports")


def parse_ports_spec(ports_spec: Optional[str]) -> Tuple[str, Optional[object]]:
    """
    Returns (mode, data)
    mode in {"common", "range", "list", "single"}
    data is tuple/list/int depending on mode
    """
    if not ports_spec:
        return ("common", None)
    ports_spec = ports_spec.strip()
    if '-' in ports_spec:
        start, end = map(int, ports_spec.split('-', 1))
        return ("range", (start, end))
    if ',' in ports_spec:
        ports = [int(p.strip()) for p in ports_spec.split(',') if p.strip()]
        return ("list", ports)
    return ("single", int(ports_spec))

def load_targets_from_file(path: str) -> List[str]:
    targets: List[str] = []
    try:
        with open(path, 'r', encoding='utf-8') as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                targets.append(line)
    except Exception as e:
        print(f"[!] Could not read targets file {path}: {e}")
    return targets

def expand_cidr_if_needed(target: str) -> List[str]:
    """
    If target contains '/', treat it as CIDR and return list of host IP strings.
    Otherwise return [target].
    """
    if '/' in target:
        try:
            network = ipaddress.ip_network(target, strict=False)
            return [str(ip) for ip in network.hosts()] or [str(next(network.hosts()))]
        except Exception as e:
            raise ValueError(f"Invalid network {target}: {e}")
    return [target]

def confirm_prompt(msg: str) -> bool:
    try:
        ans = input(msg + " [y/N]: ").strip().lower()
        return ans == 'y' or ans == 'yes'
    except Exception:
        return False

def write_scan_result(
    output_file: Optional[str],
    output_format: str,
    result: dict,
    append: bool = True
) -> None:
    if not output_file:
        return
    try:
        mode = 'a' if append else 'w'
        os.makedirs(os.path.dirname(output_file), exist_ok=True) if os.path.dirname(output_file) else None
        if output_format == 'json':
            # NDJSON: one JSON object per line
            with open(output_file, mode, encoding='utf-8') as fh:
                fh.write(json.dumps(result, default=str) + '\n')
        else:
            # human readable text
            with open(output_file, mode, encoding='utf-8') as fh:
                fh.write(f"Scan result for {result.get('target')} ({result.get('addr')})\n")
                fh.write(f"  started_at: {result.get('started_at')}\n")
                fh.write(f"  finished_at: {result.get('finished_at')}\n")
                fh.write(f"  open_ports: {', '.join(map(str, result.get('open_ports', []))) or 'none'}\n")
                # include banners and detected services in text output
                if result.get('banners'):
                    fh.write("  banners:\n")
                    for p, b in result.get('banners', {}).items():
                        fh.write(f"    {p}: {str(b).splitlines()[0] if b else 'None'}\n")
                if result.get('detected_services'):
                    fh.write("  detected_services:\n")
                    for p, s in result.get('detected_services', {}).items():
                        fh.write(f"    {p}: {s}\n")
                fh.write("-" * 40 + "\n")
    except Exception as e:
        print(f"[!] Could not write scan result to {output_file}: {e}")

def scan_one_target(
    target: str,
    ports_mode: str,
    ports_data,
    verbose: bool,
    timeout: float,
    threads: int,
    output_file: Optional[str],
    output_format: str,
    do_banner: bool,
    do_service_detect: bool
) -> None:
    scanner = PortScanner(target, timeout=timeout, threads=threads)
    if not scanner.resolve_target():
        return

    started_at = datetime.now().isoformat()
    try:
        if ports_mode == "range":
            start, end = ports_data
            scanner.scan_range(start, end, verbose=verbose, do_banner=do_banner, do_service_detect=do_service_detect)
        elif ports_mode == "list":
            ports = ports_data
            print(f"\n[*] Scanning specific ports on {scanner.target} ({scanner.addr})")
            print(f"[*] Ports: {', '.join(map(str, ports))}\n")
            for port in ports:
                result = scanner.scan_port(port)
                if result:
                    service = scanner.get_service_name(result)
                    print(f"[+] Port {result:5d} - OPEN ({service})")
                    scanner.open_ports.append(result)
                    if do_banner:
                        banner = scanner.grab_banner(result)
                        if banner:
                            print(f"    Banner: {banner.splitlines()[0]}")
                            scanner.banners[result] = banner
                        else:
                            scanner.banners[result] = None
                    if do_service_detect:
                        detected = scanner.detect_service_from_banner(result, scanner.banners.get(result))
                        scanner.detected_services[result] = detected
                elif verbose:
                    print(f"[-] Port {port:5d} - CLOSED")
        elif ports_mode == "single":
            port = ports_data
            result = scanner.scan_port(port)
            if result:
                service = scanner.get_service_name(result)
                print(f"[+] Port {result} is OPEN ({service})")
                scanner.open_ports.append(result)
                if do_banner:
                    banner = scanner.grab_banner(result)
                    if banner:
                        print(f"    Banner: {banner.splitlines()[0]}")
                        scanner.banners[result] = banner
                    else:
                        scanner.banners[result] = None
                if do_service_detect:
                    detected = scanner.detect_service_from_banner(result, scanner.banners.get(result))
                    scanner.detected_services[result] = detected
            else:
                print(f"[-] Port {port} is CLOSED")
        else:
            scanner.scan_common_ports(do_banner=do_banner, do_service_detect=do_service_detect)

    except KeyboardInterrupt:
        print("\n\n[!] Scan interrupted by user")
        # Still attempt to log partial results
    except Exception as e:
        print(f"\n[!] Error while scanning {target}: {e}")
    finished_at = datetime.now().isoformat()

    # Prepare result object and write if requested
    result_obj = {
        "target": target,
        "addr": scanner.addr,
        "family": "ipv6" if scanner.family == socket.AF_INET6 else "ipv4" if scanner.family == socket.AF_INET else None,
        "started_at": started_at,
        "finished_at": finished_at,
        "open_ports": sorted(scanner.open_ports),
        "banners": {str(k): v for k, v in scanner.banners.items()},
        "detected_services": {str(k): v for k, v in scanner.detected_services.items()}
    }
    write_scan_result(output_file, output_format, result_obj, append=True)

def main():
    parser = argparse.ArgumentParser(
        description="Simple and effective port scanner (IPv4 & IPv6)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -t 192.168.1.1                    # Scan common ports
  %(prog)s -t example.com -p 1-1000          # Scan ports 1-1000
  %(prog)s -t 192.168.1.1 -p 80,443,8080     # Scan specific ports
  %(prog)s --targets-file targets.txt -p 22  # Scan targets from file
  %(prog)s -t 192.168.1.0/28                 # Expand CIDR and scan (subject to --max-hosts)
  %(prog)s -t 2001:db8::1 -p 22              # IPv6 literal address or hostname resolving to IPv6
  %(prog)s -t 10.0.0.0/20 --max-hosts 1024   # Will prompt unless --force-network-scan is given
"""
    )

    parser.add_argument('-t', '--target', action='append',
                       help='Target IP address or hostname. May be provided multiple times or as comma-separated values.')
    parser.add_argument('--targets-file', help='File with one target per line (CIDR, IP or hostname)')
    parser.add_argument('-p', '--ports',
                       help='Port range (e.g., 1-1000) or specific ports (e.g., 80,443)')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Show all ports (open and closed)')
    parser.add_argument('--timeout', type=float, default=1.0,
                       help='Socket timeout in seconds (default: 1.0)')
    parser.add_argument('--threads', type=int, default=100,
                       help='Number of threads per-target (default: 100)')
    parser.add_argument('--max-hosts', type=int, default=256,
                       help='Max number of hosts to expand for a CIDR target before prompting (default: 256)')
    parser.add_argument('--force-network-scan', action='store_true',
                       help='Skip confirmation prompt and allow scanning networks larger than --max-hosts (USE WITH CAUTION)')
    parser.add_argument('--output-file', help='Write scan results to this file (append). For JSON use --output-format json')
    parser.add_argument('--output-format', choices=['text', 'json'], default='text',
                       help='Output format for --output-file: text or json (NDJSON). Default: text')
    parser.add_argument('--no-color', action='store_true',
                       help='Disable colored output (not used by default, placeholder for future)')
    parser.add_argument('--banner', action='store_true', help='Attempt banner grabbing on open ports')
    parser.add_argument('--service-detect', action='store_true', help='Attempt simple service detection from banners')
    args = parser.parse_args()

    # Banner
    print("=" * 60)
    print("Port Scanner v1.2")
    print("=" * 60)

    # Collect targets from args
    targets: List[str] = []
    if args.targets_file:
        targets.extend(load_targets_from_file(args.targets_file))

    if args.target:
        for entry in args.target:
            # allow comma-separated entries in a single -t
            parts = [p.strip() for p in entry.split(',') if p.strip()]
            targets.extend(parts)

    if not targets:
        print("[!] No targets specified. Use -t/--target or --targets-file.")
        sys.exit(1)

    ports_mode, ports_data = parse_ports_spec(args.ports)

    # Expand CIDRs into concrete host lists, with safety checks
    expanded_targets: List[str] = []
    for t in targets:
        if '/' in t:
            try:
                # Get size and potentially prompt
                net = ipaddress.ip_network(t, strict=False)
                num_hosts = net.num_addresses if net.version == 4 else net.num_addresses
                if num_hosts > args.max_hosts and not args.force_network_scan:
                    print(f"[!] Network {t} contains {num_hosts} addresses which exceeds --max-hosts ({args.max_hosts}).")
                    if not confirm_prompt("Do you want to continue scanning this network?"):
                        print(f"[*] Skipping {t}")
                        continue
                hosts = expand_cidr_if_needed(t)
                expanded_targets.extend(hosts)
            except Exception as e:
                print(f"[!] Skipping {t}: {e}")
        else:
            expanded_targets.append(t)

    if not expanded_targets:
        print("[!] No valid targets after expansion.")
        sys.exit(1)

    # Scan each target sequentially
    for host in expanded_targets:
        scan_one_target(
            target=host,
            ports_mode=ports_mode,
            ports_data=ports_data,
            verbose=args.verbose,
            timeout=args.timeout,
            threads=args.threads,
            output_file=args.output_file,
            output_format=args.output_format,
            do_banner=args.banner,
            do_service_detect=args.service_detect
        )

if __name__ == "__main__":
    main()
