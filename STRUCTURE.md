# Repository Structure

```
port-scanner/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md          # Bug report template
│   │   └── feature_request.md     # Feature request template
│   ├── workflows/
│   │   └── test.yml               # GitHub Actions CI/CD
│   └── PULL_REQUEST_TEMPLATE.md   # PR template
│
├── docs/
│   ├── INSTALL.md                 # Installation guide
│   └── USAGE.md                   # Detailed usage guide
│
├── examples/
│   └── run_examples.py            # Interactive examples script
│
├── port_scanner.py                # Main scanner script
├── setup.sh                       # Quick setup script
│
├── README.md                      # Main documentation
├── LICENSE                        # MIT License
├── CHANGELOG.md                   # Version history
├── CONTRIBUTING.md                # Contribution guidelines
├── CODE_OF_CONDUCT.md             # Code of conduct
├── SECURITY.md                    # Security policy
├── requirements.txt               # Python dependencies (none!)
└── .gitignore                     # Git ignore rules
```

## File Descriptions

### Root Files

- **port_scanner.py**: The main port scanner application
- **setup.sh**: Automated setup and testing script
- **README.md**: Project overview and quick start guide
- **LICENSE**: MIT License text
- **requirements.txt**: Python dependencies (empty - uses stdlib only)
- **.gitignore**: Git ignore patterns

### Documentation (docs/)

- **INSTALL.md**: Complete installation instructions
- **USAGE.md**: Comprehensive usage guide with examples

### Examples (examples/)

- **run_examples.py**: Interactive script demonstrating various scan modes

### GitHub Configuration (.github/)

#### Issue Templates
- **bug_report.md**: Template for bug reports
- **feature_request.md**: Template for feature requests

#### Workflows
- **test.yml**: GitHub Actions workflow for CI/CD

#### Pull Requests
- **PULL_REQUEST_TEMPLATE.md**: Template for pull requests

### Community Files

- **CONTRIBUTING.md**: Guidelines for contributors
- **CODE_OF_CONDUCT.md**: Community code of conduct
- **SECURITY.md**: Security policy and responsible disclosure
- **CHANGELOG.md**: Version history and release notes

## Getting Started

1. Clone the repository
2. Run `./setup.sh` for quick setup
3. Read [README.md](README.md) for basic usage
4. Check [docs/USAGE.md](docs/USAGE.md) for advanced features
5. See [examples/](examples/) for practical examples

## For Contributors

1. Read [CONTRIBUTING.md](CONTRIBUTING.md)
2. Check existing issues and PRs
3. Follow the code style guidelines
4. Use the provided templates
5. Test thoroughly before submitting
