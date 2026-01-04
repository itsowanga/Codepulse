# Contributing to CodePulse

Thank you for your interest in contributing to CodePulse! We welcome contributions from everyone. Here's how you can help:

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/codepulse.git
   cd codepulse
   ```
3. **Create a new branch** for your feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

### C++ Development
```bash
cd src
make clean
make
```

### Python Development
```bash
# Create a virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# or source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

## Code Style

- **C++**: Follow modern C++ (C++17) standards
- **Python**: Follow PEP 8 style guide
  - Use 4 spaces for indentation
  - Use meaningful variable and function names
  - Add docstrings to functions

## Submitting Changes

1. **Commit your changes** with clear, descriptive messages:
   ```bash
   git commit -m "Add feature: description of what you added"
   ```
2. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
3. **Create a Pull Request** on GitHub with a clear description of your changes

## Testing

Before submitting a PR, please:
- Test your changes locally
- Ensure all existing functionality still works
- Add tests for new features if applicable

## Bug Reports

If you find a bug, please create an issue with:
- A clear description of the bug
- Steps to reproduce it
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)

## Feature Requests

We'd love to hear your ideas! Please create an issue describing:
- The feature you'd like to see
- Why it would be useful
- Any examples or mockups if applicable

## Questions?

Feel free to open a discussion or reach out on GitHub Issues.

---

Thank you for contributing to CodePulse! 🚀
