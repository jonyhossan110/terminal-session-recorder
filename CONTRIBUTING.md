# Contributing to Terminal Session Recorder

Thank you for your interest in contributing to TSR! 🎉

## How to Contribute

### Reporting Bugs

1. Check existing issues first
2. Create a new issue with:
   - Clear title
   - Detailed description
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (OS, Python version, TSR version)

### Suggesting Features

1. Check existing feature requests
2. Open an issue with:
   - Clear description of the feature
   - Use cases
   - Benefits
   - Implementation ideas (optional)

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Commit with clear messages
7. Push to your fork
8. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/terminal-session-recorder.git
cd terminal-session-recorder

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run linting
flake8 tsr/
black tsr/ --check
```

### Code Style

- Follow PEP 8
- Use type hints where appropriate
- Write docstrings for public functions
- Keep functions focused and small
- Add comments for complex logic

### Testing

- Write tests for new features
- Ensure existing tests pass
- Aim for good test coverage

### Documentation

- Update README.md for new features
- Add docstrings to new functions
- Update CHANGELOG.md

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Help others learn and grow

## Questions?

- Open an issue
- Email: jonyhossan110@gmail.com
- GitHub Discussions

Thank you for contributing! 🙏
