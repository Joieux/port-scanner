# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-27

### Added
- Initial release
- Multithreaded port scanning
- Support for port ranges and specific ports
- Common ports quick scan mode
- Service name detection
- Progress tracking for large scans
- Verbose output mode
- Customizable timeout and thread count
- Command-line interface with argparse
- Comprehensive error handling
- Support for both IP addresses and hostnames

### Features
- Fast concurrent scanning using ThreadPoolExecutor
- Clean, readable output format
- Cross-platform compatibility (Linux, macOS, Windows)
- No external dependencies

## [Unreleased]

### Planned Features
- UDP port scanning
- OS fingerprinting
- Banner grabbing
- Output to JSON/CSV formats
- Scan result saving
- Configuration file support
- Stealth scanning modes
- Network range scanning
