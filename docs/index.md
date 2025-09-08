# Privacy Policy Analyzer

Welcome to the **Privacy Policy Analyzer** - an AI-powered tool designed to help you understand
and analyze privacy policies with ease.

## 🚀 Features

- **AI-Powered Analysis**: Uses advanced language models to extract key information from privacy policies
- **Comprehensive Scoring**: Evaluates privacy policies across multiple dimensions
- **Easy Integration**: Simple Python API for seamless integration into your workflow
- **Web Scraping**: Automatically extracts privacy policy content from websites
- **Caching**: Intelligent caching system for improved performance

## 🎯 What It Does

The Privacy Policy Analyzer helps you:

- **Extract Key Information**: Automatically identify data collection practices, sharing policies,
  and user rights
- **Score Privacy Policies**: Get quantitative scores on various privacy aspects
- **Compare Policies**: Analyze multiple privacy policies side by side
- **Generate Reports**: Create detailed analysis reports for stakeholders

## 🏃‍♂️ Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/HappyHackingSpace/privacy-policy.git
cd privacy-policy

# Using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

### Basic Usage

```python
# Analyze a homepage URL — auto-discovery will attempt to resolve a policy page
python -m src.main --url "https://example.com"

# Analyze a known policy URL directly
python -m src.main --url "https://example.com/privacy-policy" --no-discover
```

## 📊 Analysis Dimensions

The analyzer evaluates privacy policies across ten key dimensions.  
Each dimension is scored on a **0–10 scale**, then combined with weights to produce a final **0–100 overall score**.

- **Lawful Basis & Purpose**: Whether the policy explains clear purposes for processing and, where relevant, the legal basis or justification.  
- **Collection & Minimization**: How clearly the policy describes the types of data collected and whether collection is limited to what is necessary.  
- **Secondary Use & Limits**: Whether the policy restricts or explains additional uses beyond the original purpose.  
- **Retention & Deletion**: Clarity on how long data is kept, deletion practices, or criteria for determining retention.  
- **Third Parties & Processors**: Disclosure of processors, vendors, or third parties with whom data is shared, and their roles.  
- **Cross-Border Transfers**: Information on transfers outside the user’s country/region and safeguards in place.  
- **User Rights & Redress**: How users can exercise rights such as access, correction, deletion, or complaint, and available escalation channels.  
- **Security & Breach**: Security measures described and any statements about breach notification or handling.  
- **Transparency & Notice**: Overall clarity, structure, contact details, and how users are informed of updates or changes.  
- **Sensitive Data, Children, Ads & Profiling**: How sensitive categories are handled, rules for children’s data, use of data for advertising, and automated decision-making/profiling.

## 🔧 Advanced Features

- **Flexible Fetching**: Choose between `auto`, `http`, or `selenium` modes.  
- **Configurable Chunking**: Control `--chunk-size`, `--chunk-overlap`, and `--max-chunks` for long policies.  
- **Multiple Report Levels**: Select `summary`, `detailed`, or `full` output.  
- **Model Override**: Use `--model` or the `OPENAI_MODEL` environment variable to select your OpenAI model.  

## 📚 Documentation

- [User Guide](user-guide.md) - Complete guide to using the analyzer
- [API Reference](api.md) - Detailed API documentation
- [Contributing](contributing.md) - How to contribute to the project

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](contributing.md) for details on how to get started.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## 🆘 Support

- **Issues**: Report bugs or request features on [GitHub Issues](https://github.com/HappyHackingSpace/privacy-policy/issues)
- **Discussions**: Join our community discussions on [GitHub Discussions](https://github.com/HappyHackingSpace/privacy-policy/discussions)
- **Discord**: Join our [Happy Hacking Space Discord](https://discord.gg/happyhackingspace)

---

*Built with ❤️ for privacy-conscious developers and organizations*
