# User Guide

This guide explains how to install, run, and interpret results from **Privacy Policy Analyzer**. The tool is currently **CLI-first** (no stable class-based API).

## 📋 Table of Contents

- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [Configuration](#configuration)
- [Analysis Methods](#analysis-methods)
- [Understanding Results](#understanding-results)
- [Advanced Features](#advanced-features)
- [Troubleshooting](#troubleshooting)
- [Examples](#examples)
- [Getting Help](#getting-help)

## 🚀 Installation

### Prerequisites

- Python 3.13+  
- An OpenAI API key available in your environment (or `.env`)  
- Google Chrome (required only if you plan to use Selenium fallback)  
- Optional: `trafilatura` for enhanced extraction

### Using uv (recommended)

```bash
git clone https://github.com/HappyHackingSpace/privacy-policy.git
cd privacy-policy
uv sync
# optional: activate .venv if you prefer a shell-activated workflow
# macOS/Linux: source .venv/bin/activate
# Windows: .venv\Scripts\activate
```

### Using Poetry

```bash
git clone https://github.com/HappyHackingSpace/privacy-policy.git
cd privacy-policy
poetry install
# run commands with: poetry run <command>
```

### Using pip

```bash
git clone https://github.com/HappyHackingSpace/privacy-policy.git
cd privacy-policy
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate
pip install -e .
```

Create a `.env` file if desired:


Verify that your API key is visible to the process:

```bash
python -c "import os; print('API key set:', bool(os.getenv('OPENAI_API_KEY')))"
```

## 🔧 Basic Usage

Run the CLI with a site URL (auto-discovery will try to resolve a likely privacy policy page):

```bash
# uv
uv run python src/main.py --url https://example.com
# or module form
python -m src.main --url https://example.com
```

Analyze a known policy URL directly (skip auto-discovery):

```bash
uv run python src/main.py --url https://example.com/privacy-policy --no-discover
```

Choose a fetch method:

```bash
uv run python src/main.py --url https://example.com/privacy --fetch selenium
```

Control output detail:

```bash
uv run python src/main.py --url https://example.com --report detailed
```

## ⚙️ Configuration

### Environment Variables

You can configure the model and environment via variables or flags.

- **Required**
  - `OPENAI_API_KEY`: your OpenAI key

- **Optional**
  - `OPENAI_MODEL`: default model if `--model` is not provided (defaults to `gpt-4o`)

CLI flags that control analysis:

- `--model TEXT`  
  Override the OpenAI model for this run.

- `--report {summary|detailed|full}`  
  Select output verbosity.  
  - `summary`: overall score, confidence, top strengths/risks, red-flag count  
  - `detailed`: includes per-category details, red flags, recommendations  
  - `full`: includes raw per-chunk results

- `--chunk-size INT`, `--chunk-overlap INT`, `--max-chunks INT`  
  Tune chunking for very long policies (tail chunks may be merged when `--max-chunks` is exceeded).

- `--fetch {auto|http|selenium}`  
  Extraction mode (auto uses HTTP first and can fall back to Selenium).

- `--no-discover`  
  Analyze the provided URL as-is (no policy URL resolution).

## 🔍 Analysis Methods

- **URL analysis with auto-discovery**  
  Provide a site homepage or any page; the tool attempts to find a likely policy path (e.g., `/privacy`, `/privacy-policy`, robots/sitemap hints, or in-page links).

- **Direct policy URL**  
  If you already know the exact policy page, use `--no-discover` to skip discovery.

- **Extraction**  
  Content is fetched via HTTP/BeautifulSoup by default, optionally through Trafilatura when available, and can fall back to Selenium for client-rendered pages.

- **Chunking & scoring**  
  Extracted text is split into overlapping chunks; each chunk is scored by the model with a fixed schema. Category scores (each **0–10**) are aggregated with weights into a **0–100** overall score.

## 📊 Understanding Results

The CLI prints **JSON** to stdout.

Common fields:

- `status`: `"ok"` or `"error"`
- `url`: the input URL you provided
- `resolved_url`: the discovered/verified policy URL (if discovery was used)
- `model`: OpenAI model used (e.g., `gpt-4o`)
- `chunks` / `valid_chunks`: number of chunks analyzed and number that produced valid scores
- `overall_score`: weighted 0–100 score across all categories
- `confidence`: coverage ratio (0–1), based on how many categories received valid scores
- `category_scores`: per-category `{score (0–10), weight, rationale}`
- `top_strengths` / `top_risks`: strongest/weakest categories
- `red_flags`: unique risk indicators extracted from chunk results
- `recommendations`: short, actionable notes
- (`full` only) `chunks`: raw per-chunk outputs

### Dimensions (what they mean)

Each dimension is scored **0–10**; weights are applied to compute the overall score:

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

## 🚀 Advanced Features

- **Flexible fetching** with `--fetch auto|http|selenium`  
- **Configurable chunking** via `--chunk-size`, `--chunk-overlap`, `--max-chunks`  
- **Report levels** with `--report summary|detailed|full`  
- **Model override** with `--model` or `OPENAI_MODEL`

> Note: Caching, batch processing, CSV/HTML exports, and a stable importable Python API are not part of the current CLI release. See the roadmap in the contributing guide.

## 🔧 Troubleshooting

- **`OPENAI_API_KEY is not set`**  
  Set the key in your environment or a `.env` file.

- **Empty or insufficient text**  
  Allow auto-discovery (avoid `--no-discover`) or provide a better URL. Some pages may require Selenium (`--fetch selenium`) to render content.

- **Very long policies**  
  Increase `--max-chunks`, or adjust `--chunk-size`/`--chunk-overlap`. The tool merges tail chunks to stay within limits.

- **Model issues**  
  Ensure the selected model supports JSON-style responses. The tool uses `temperature=0` for consistent scoring.

## 📚 Examples

Analyze a homepage with default settings:

```bash
uv run python src/main.py --url https://example.com
```

Analyze a known policy URL with detailed output:

```bash
uv run python src/main.py --url https://example.com/privacy-policy --no-discover --report detailed
```

Force Selenium for a client-rendered policy:

```bash
uv run python src/main.py --url https://example.com/privacy --fetch selenium
```

Tune chunking for very long policies:

```bash
uv run python src/main.py --url https://example.com --chunk-size 3000 --chunk-overlap 300 --max-chunks 25
```
## 🆘 Getting Help

- **Documentation**: Check the [API Reference](api.md) for detailed API documentation
- **Issues**: Report bugs on [GitHub Issues](https://github.com/HappyHackingSpace/privacy-policy/issues)
- **Discussions**: Join community discussions on [GitHub Discussions](https://github.com/HappyHackingSpace/privacy-policy/discussions)
- **Discord**: Join our [Happy Hacking Space Discord](https://discord.gg/happyhackingspace)

---

*Happy analyzing! 🔍✨*
