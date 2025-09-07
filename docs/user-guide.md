# User Guide

This comprehensive guide will help you get started with the Privacy Policy Analyzer and make the most of its features.

## 📋 Table of Contents

- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [Configuration](#configuration)
- [Analysis Methods](#analysis-methods)
- [Understanding Results](#understanding-results)
- [Advanced Features](#advanced-features)
- [Troubleshooting](#troubleshooting)

## 🚀 Installation

### Prerequisites

- Python 3.13 or higher
- Internet connection for downloading models and accessing websites

### Install the Package

```bash
# Using uv (recommended)
uv add privacy-policy

# Using pip
pip install privacy-policy

# From source
git clone https://github.com/your-username/privacy-policy.git
cd privacy-policy
uv sync
```

### Verify Installation

```python
import privacy_policy
print(f"Privacy Policy Analyzer version: {privacy_policy.__version__}")
```

## 🔧 Basic Usage

### 1. Initialize the Analyzer

```python
from privacy_policy import PrivacyPolicyAnalyzer

# Basic initialization
analyzer = PrivacyPolicyAnalyzer()

# With custom configuration
analyzer = PrivacyPolicyAnalyzer(
    api_key="your-openai-api-key",
    cache_dir="./cache",
    timeout=30
)
```

### 2. Analyze a Privacy Policy

#### From URL

```python
# Analyze a privacy policy from a website
result = analyzer.analyze_url("https://example.com/privacy-policy")

print(f"Overall Score: {result.overall_score}")
print(f"Confidence: {result.confidence}")
print(f"Key Findings: {result.findings}")
```

#### From Text

```python
# Analyze privacy policy text directly
policy_text = """
Your privacy is important to us. We collect information...
"""

result = analyzer.analyze_text(policy_text)
```

#### From File

```python
# Analyze a privacy policy from a local file
result = analyzer.analyze_file("privacy_policy.txt")
```

### 3. Understanding the Results

```python
# Access detailed results
print("=== PRIVACY ANALYSIS RESULTS ===")
print(f"Overall Score: {result.overall_score}/100")
print(f"Confidence: {result.confidence}%")
print(f"Analysis Time: {result.analysis_time:.2f}s")

print("\n=== DIMENSION SCORES ===")
for dimension, score in result.dimension_scores.items():
    print(f"{dimension}: {score}/100")

print("\n=== KEY FINDINGS ===")
for finding in result.findings:
    print(f"- {finding}")

print("\n=== RECOMMENDATIONS ===")
for recommendation in result.recommendations:
    print(f"- {recommendation}")
```

## ⚙️ Configuration

### Environment Variables

Set up your API key and other configuration:

```bash
# .env file
OPENAI_API_KEY=your-api-key-here
CACHE_DIR=./cache
DEFAULT_TIMEOUT=30
LOG_LEVEL=INFO
```

### Configuration Options

```python
from privacy_policy import PrivacyPolicyAnalyzer

analyzer = PrivacyPolicyAnalyzer(
    # API Configuration
    api_key="your-api-key",
    model="gpt-4",
    temperature=0.1,

    # Caching
    cache_dir="./cache",
    cache_ttl=3600,  # 1 hour

    # Network
    timeout=30,
    max_retries=3,

    # Analysis
    include_recommendations=True,
    detailed_analysis=True,
    language="en"
)
```

## 🔍 Analysis Methods

### 1. URL Analysis

```python
# Basic URL analysis
result = analyzer.analyze_url("https://example.com/privacy")

# With custom options
result = analyzer.analyze_url(
    "https://example.com/privacy",
    extract_method="trafilatura",  # or "beautifulsoup"
    timeout=60,
    follow_redirects=True
)
```

### 2. Text Analysis

```python
# Analyze raw text
result = analyzer.analyze_text(policy_text)

# With custom prompts
result = analyzer.analyze_text(
    policy_text,
    custom_prompts={
        "data_collection": "Focus on data collection practices",
        "sharing": "Analyze data sharing policies"
    }
)
```

### 3. Batch Analysis

```python
# Analyze multiple URLs
urls = [
    "https://example1.com/privacy",
    "https://example2.com/privacy",
    "https://example3.com/privacy"
]

results = analyzer.analyze_batch(urls)

# Compare results
comparison = analyzer.compare_results(results)
print(comparison.summary)
```

## 📊 Understanding Results

### Score Interpretation

- **90-100**: Excellent privacy practices
- **80-89**: Good privacy practices with minor issues
- **70-79**: Fair privacy practices with some concerns
- **60-69**: Poor privacy practices with significant issues
- **Below 60**: Very poor privacy practices

### Dimension Scores

The analyzer evaluates several key dimensions:

- **Data Collection** (0-100): How much and what type of data is collected
- **Data Sharing** (0-100): How data is shared with third parties
- **User Rights** (0-100): What rights users have over their data
- **Transparency** (0-100): How clear and understandable the policy is
- **Compliance** (0-100): Adherence to privacy regulations

### Confidence Levels

- **High (80-100%)**: Very confident in the analysis
- **Medium (60-79%)**: Moderately confident
- **Low (Below 60%)**: Low confidence, manual review recommended

## 🚀 Advanced Features

### Custom Prompts

```python
# Define custom analysis prompts
custom_prompts = {
    "data_collection": """
    Analyze the data collection practices in this privacy policy.
    Focus on:
    - What data is collected
    - How it's collected
    - Legal basis for collection
    """,

    "user_rights": """
    Identify user rights mentioned in this privacy policy.
    Look for:
    - Access rights
    - Deletion rights
    - Portability rights
    - Opt-out options
    """
}

result = analyzer.analyze_text(policy_text, custom_prompts=custom_prompts)
```

### Caching

```python
# Enable caching for better performance
analyzer = PrivacyPolicyAnalyzer(
    cache_dir="./cache",
    cache_ttl=3600  # Cache for 1 hour
)

# Clear cache when needed
analyzer.clear_cache()
```

### Export Results

```python
# Export to JSON
result.export_json("analysis_results.json")

# Export to CSV
result.export_csv("analysis_results.csv")

# Export to HTML report
result.export_html("privacy_report.html")
```

## 🔧 Troubleshooting

### Common Issues

#### 1. API Key Issues

```python
# Check if API key is set
import os
print(f"API Key set: {bool(os.getenv('OPENAI_API_KEY'))}")

# Set API key programmatically
analyzer = PrivacyPolicyAnalyzer(api_key="your-key-here")
```

#### 2. Network Issues

```python
# Increase timeout for slow websites
result = analyzer.analyze_url(
    "https://slow-website.com/privacy",
    timeout=120
)

# Use different extraction method
result = analyzer.analyze_url(
    "https://example.com/privacy",
    extract_method="beautifulsoup"  # Try different method
)
```

#### 3. Content Extraction Issues

```python
# Check if content was extracted
result = analyzer.analyze_url("https://example.com/privacy")
print(f"Content extracted: {len(result.raw_content) > 0}")
print(f"Content length: {len(result.raw_content)} characters")

# Try manual extraction
from privacy_policy.extractors import WebExtractor
extractor = WebExtractor()
content = extractor.extract("https://example.com/privacy")
```

### Debug Mode

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

analyzer = PrivacyPolicyAnalyzer(debug=True)
result = analyzer.analyze_url("https://example.com/privacy")
```

## 📚 Examples

### Example 1: Basic Analysis

```python
from privacy_policy import PrivacyPolicyAnalyzer

# Initialize
analyzer = PrivacyPolicyAnalyzer()

# Analyze
result = analyzer.analyze_url("https://example.com/privacy")

# Display results
print(f"Privacy Score: {result.overall_score}/100")
print(f"Key Issues: {result.findings}")
```

### Example 2: Comparative Analysis

```python
# Analyze multiple policies
urls = [
    "https://company1.com/privacy",
    "https://company2.com/privacy"
]

results = []
for url in urls:
    result = analyzer.analyze_url(url)
    results.append(result)

# Compare
comparison = analyzer.compare_results(results)
print(comparison.summary)
```

### Example 3: Custom Analysis

```python
# Custom analysis with specific focus
custom_prompts = {
    "gdpr_compliance": "Analyze GDPR compliance aspects",
    "data_minimization": "Check data minimization practices"
}

result = analyzer.analyze_text(
    policy_text,
    custom_prompts=custom_prompts
)

print("GDPR Compliance:", result.custom_scores["gdpr_compliance"])
print("Data Minimization:", result.custom_scores["data_minimization"])
```

## 🆘 Getting Help

- **Documentation**: Check the [API Reference](api.md) for detailed API documentation
- **Issues**: Report bugs on [GitHub Issues](https://github.com/HappyHackingSpace/privacy-policy/issues)
- **Discussions**: Join community discussions on [GitHub Discussions](https://github.com/HappyHackingSpace/privacy-policy/discussions)
- **Discord**: Join our [Happy Hacking Space Discord](https://discord.gg/happyhackingspace)

---

*Happy analyzing! 🔍✨*
