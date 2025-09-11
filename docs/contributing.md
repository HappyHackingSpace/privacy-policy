# Contributing

Thank you for your interest in contributing to the Privacy Policy Analyzer! This document
provides guidelines and information for contributors.

## 📋 Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Code Style](#code-style)
- [Testing](#testing)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)

## 🚀 Getting Started

### Prerequisites

- Python 3.13 or higher
- Git
- uv (recommended) or pip
- OpenAI API key (for testing)

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:

```bash
git clone https://github.com/your-username/privacy-policy-analyzer.git
cd privacy-policy-analyzer
```

3. Add the upstream repository:

```bash
git remote add upstream https://github.com/HappyHackingSpace/privacy-policy-analyzer.git
```

## 🔧 Development Setup

### 1. Install Dependencies

```bash
# Using uv (recommended)
uv sync --dev

# Using pip
pip install -e .
```

### 2. Install Pre-commit Hooks

```bash
uv run pre-commit install
```

### 3. Set Up Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
# OPENAI_API_KEY=your-api-key-here
# Optional:
# OPENAI_MODEL=gpt-4o
```

### 4. Verify Setup

```bash
# Run tests
uv run pytest

# Run linting
uv run ruff check

# Run type checking (if configured)
uv run mypy src/
```

## 📝 Contributing Guidelines

### Types of Contributions

We welcome various types of contributions:

- **Bug Reports**: Report bugs and issues
- **Feature Requests**: Suggest new features
- **Code Contributions**: Fix bugs, add features
- **Documentation**: Improve documentation
- **Testing**: Add or improve tests
- **Examples**: Add usage examples

### Before Contributing

1. **Check Issues**: Look for existing issues or discussions
2. **Create Issue**: For significant changes, create an issue first
3. **Discuss**: Engage in discussions before starting work
4. **Fork**: Fork the repository and create a feature branch

### Workflow

1. **Create Branch**: Create a feature branch from `main`

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**: Implement your changes
3. **Test**: Ensure all tests pass
4. **Document**: Update documentation if needed
5. **Commit**: Write clear commit messages
6. **Push**: Push your branch to your fork
7. **Pull Request**: Create a pull request

## 🎨 Code Style

### Python Style

We follow PEP 8 with some modifications:

- **Line Length**: 88 characters (Black default)
- **Import Sorting**: isort with Black profile
- **Type Hints**: Required for all functions and methods
- **Docstrings**: Google style docstrings

### Formatting

We use automated formatting tools:

```bash
# Format code (choose either)
uv run black src/ tests/
uv run isort src/ tests/

# Or run both
uv run ruff format src/ tests/
```

### Linting

```bash
# Check code quality
uv run ruff check src/ tests/

# Fix auto-fixable issues
uv run ruff check --fix src/ tests/
```

### Type Checking

```bash
# Run type checker (if configured)
uv run mypy src/
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=html

# Run specific test file
uv run pytest tests/test_analyzer.py

# Run with verbose output
uv run pytest -v
```

### Writing Tests

- **Test Files**: Place tests in `tests/` directory
- **Naming**: Test files should start with `test_`
- **Functions**: Test functions should start with `test_`
- **Fixtures**: Use pytest fixtures for common setup
- **Coverage**: Aim for high test coverage

### Example Unit Test (project-realistic)

```python
import pytest
from src.analyzer.scoring import aggregate_chunk_results

ALL_CATEGORIES = [
    "lawful_basis_and_purpose",
    "collection_and_minimization",
    "secondary_use_and_limits",
    "retention_and_deletion",
    "third_parties_and_processors",
    "cross_border_transfers",
    "user_rights_and_redress",
    "security_and_breach",
    "transparency_and_notice",
    "sensitive_children_ads_profiling",
]

def test_aggregate_chunk_results_basic():
    # Minimal valid per-chunk payload matching the prompt schema (0–10 per category)
    scores = {k: 7 for k in ALL_CATEGORIES}
    rationales = {k: "ok" for k in ALL_CATEGORIES}
    chunk_json_list = [{
        "scores": scores,
        "rationales": rationales,
        "red_flags": [],
        "notes": [],
    }]

    agg = aggregate_chunk_results(chunk_json_list)
    assert 0 <= agg["overall_score"] <= 100
    assert "category_scores" in agg and isinstance(agg["category_scores"], dict)
    assert 0 <= agg["confidence"] <= 1
```

## 📚 Documentation

### Code Documentation

- **Docstrings**: All public functions and classes need docstrings
- **Type Hints**: Use type hints for all parameters and return values
- **Comments**: Add comments for complex logic

### Example Docstring (for an existing function)

```python
from typing import Optional, Tuple

def resolve_privacy_url(input_url: str) -> Tuple[str, Optional[str]]:
    """Resolve a likely privacy policy URL starting from any given page.

    The function checks common policy paths, verifies candidates with a lightweight
    content probe, inspects robots.txt and sitemaps, and finally scans in-page links
    for privacy-related anchors.

    Args:
        input_url: A site page or a direct policy URL.

    Returns:
        A tuple (resolved_url, original_input_if_discovery_used).
        If discovery is skipped or unnecessary, the second item may be None.
    """
    ...
```

### Documentation Updates

When adding features or changing behavior:

1. **Update Docstrings**: Update relevant docstrings
2. **Update README**: Update README if needed
3. **Update User Guide**: Update user guide for new features
4. **Update API Docs**: Update CLI reference as needed
5. **Add Examples**: Add usage examples

## 🔄 Submitting Changes

### Commit Messages

Use clear, descriptive commit messages:

```
feat: add batch analysis functionality

- Add analyze_batch method to PrivacyPolicyAnalyzer
- Add progress callback support
- Add concurrent processing with configurable limits
- Update documentation and examples

Closes #123
```

### Pull Request Process

1. **Title**: Use clear, descriptive title
2. **Description**: Provide detailed description
3. **Reference Issues**: Link to related issues
4. **Screenshots**: Include screenshots for UI changes
5. **Testing**: Mention testing done
6. **Breaking Changes**: Note any breaking changes

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)

## Related Issues
Closes #123
```

## 🏷️ Release Process

### Version Bumping

We use semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Changelog

Update `CHANGELOG.md` with:

- **Added**: New features
- **Changed**: Changes to existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security improvements

## 🤝 Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Help others learn and grow

### Getting Help

- **GitHub Discussions**: For questions and discussions
- **GitHub Issues**: For bug reports and feature requests
- **Email**: Contact maintainers directly
- **Discord**: Join our community Discord

### Recognition

Contributors will be recognized in:

- **CONTRIBUTORS.md**: List of all contributors
- **Release Notes**: Mentioned in release notes
- **GitHub**: Listed as contributors

## 📞 Contact

- **Organization**: [Happy Hacking Space](https://github.com/HappyHackingSpace)
- **Repository**: [@HappyHackingSpace/privacy-policy-analyzer](https://github.com/HappyHackingSpace/privacy-policy-analyzer)
- **Discord**: [Join our server](https://discord.gg/happyhackingspace)

---

Thank you for contributing to the Privacy Policy Analyzer! 🎉
