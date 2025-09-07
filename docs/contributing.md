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
git clone https://github.com/your-username/privacy-policy.git
cd privacy-policy
```

3. Add the upstream repository:

```bash
git remote add upstream https://github.com/original-username/privacy-policy.git
```

## 🔧 Development Setup

### 1. Install Dependencies

```bash
# Using uv (recommended)
uv sync --dev

# Using pip
pip install -e ".[dev]"
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
# CACHE_DIR=./cache
# LOG_LEVEL=DEBUG
```

### 4. Verify Setup

```bash
# Run tests
uv run pytest

# Run linting
uv run ruff check

# Run type checking
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
# Format code
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
# Run type checker
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

### Test Structure

```python
import pytest
from privacy_policy import PrivacyPolicyAnalyzer

class TestPrivacyPolicyAnalyzer:
    def test_initialization(self):
        """Test analyzer initialization."""
        analyzer = PrivacyPolicyAnalyzer()
        assert analyzer is not None

    def test_analyze_text(self):
        """Test text analysis."""
        analyzer = PrivacyPolicyAnalyzer()
        result = analyzer.analyze_text("Test privacy policy text")
        assert result.overall_score >= 0
        assert result.overall_score <= 100
```

## 📚 Documentation

### Code Documentation

- **Docstrings**: All public functions and classes need docstrings
- **Type Hints**: Use type hints for all parameters and return values
- **Comments**: Add comments for complex logic

### Example Docstring

```python
def analyze_url(
    self,
    url: str,
    extract_method: str = "auto",
    timeout: Optional[int] = None,
    follow_redirects: bool = True,
    custom_prompts: Optional[Dict[str, str]] = None
) -> AnalysisResult:
    """Analyze a privacy policy from a URL.

    Args:
        url: URL of the privacy policy page
        extract_method: Method for extracting content
        timeout: Override default timeout for this request
        follow_redirects: Whether to follow redirects
        custom_prompts: Custom prompts for analysis

    Returns:
        AnalysisResult object with analysis results

    Raises:
        ExtractionError: If content extraction fails
        AnalysisError: If analysis fails
        NetworkError: If network request fails
    """
```

### Documentation Updates

When adding features or changing APIs:

1. **Update Docstrings**: Update relevant docstrings
2. **Update README**: Update README if needed
3. **Update User Guide**: Update user guide for new features
4. **Update API Docs**: Update API documentation
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
- **Repository**: [@HappyHackingSpace/privacy-policy](https://github.com/HappyHackingSpace/privacy-policy)
- **Discord**: [Join our server](https://discord.gg/happyhackingspace)

---

Thank you for contributing to the Privacy Policy Analyzer! 🎉
