# Privacy Policy Analyzer

Analyze a website’s privacy policy end-to-end: **auto-discover** the policy URL, **fetch** clean text (HTTP first, Selenium fallback), **chunk** the content, **evaluate** it via an LLM with a structured rubric, and **aggregate** category scores into an overall score with strengths, risks, red flags, and recommendations.

## Features
- **Auto-discovery**: Common paths → robots.txt/sitemaps → footer links.
- **HTTP-first extraction**: `trafilatura` (clean text) or `BeautifulSoup` fallback; **Selenium** for dynamic pages.
- **Structured scoring (JSON)**: Per-category (0–10) scores + rationales; aggregated to 0–100 overall in `scoring.py`.
- **Configurable chunking**: Paragraph-aware recursive splitting; `--max-chunks` hard cap to control cost/latency.
- **Simple CLI**: Choose `summary`, `detailed`, or `full` reports.

## Project Layout
    privacy-policy/
    ├─ PrivacyPolicy.py
    ├─ requirements.txt
    ├─ .env.example
    ├─ .gitignore
    ├─ LICENSE
    └─ src/
       └─ privacy_policy_analyzer/
          ├─ prompts.py
          └─ scoring.py

## Requirements
- Python **3.10+**
- An **OpenAI API key**
- (Optional) **Chrome/Chromium** on the machine (Selenium fallback; driver auto-installs)

## Installation
```bash
python -m venv venv
# Windows
venv\\Scripts\\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

## Configuration
Copy `.env.example` → `.env` and set your credentials:

```
OPENAI_API_KEY=sk-************************
# Optional (overrides default):
OPENAI_MODEL=gpt-4o
```

## Usage

### Quick start (auto-discovery, summary report)
```bash
python PrivacyPolicy.py --url https://www.example.com/ --report summary
```

### Detailed JSON (category scores, rationales, red flags)
```bash
python PrivacyPolicy.py --url https://www.example.com/ --report detailed
```

### Force a specific fetch method
- HTTP only (faster/cleaner when available):
```bash
python PrivacyPolicy.py --url https://www.example.com/ --fetch http --report detailed
```

- Selenium only (for heavily dynamic pages):
```bash
python PrivacyPolicy.py --url https://www.example.com/ --fetch selenium --report detailed
```

### Skip auto-discovery (analyze a known policy URL as-is)
```bash
python PrivacyPolicy.py --url https://www.example.com/legal/privacy --no-discover --report detailed
```

### Tuning chunking and cost/latency
```bash
# Larger chunks = fewer requests (cheaper/faster), but slightly coarser analysis
python PrivacyPolicy.py --url https://example.com --chunk-size 3500 --chunk-overlap 350 --max-chunks 30 --report summary
```

## CLI Options (summary)
- `--url` **(required)**: Site homepage or direct privacy policy URL.
- `--model` *(default: env `OPENAI_MODEL` or `gpt-4o`)*: OpenAI chat model name.
- `--fetch` *(default: `auto`)*: `auto` | `http` | `selenium`.
- `--no-discover`: Analyze the given URL without discovery.
- `--chunk-size` *(default: 3500)* and `--chunk-overlap` *(default: 350)*.
- `--max-chunks` *(default: 30)*: Hard cap; tail chunks are merged to keep requests bounded.
- `--report` *(default: `summary`)*: `summary` | `detailed` | `full`.

## Output
- **summary**: overall score, confidence, top strengths/risks, red-flags count.
- **detailed**: adds per-category scores (0–10), rationales, deduped red flags, recommendations.
- **full**: includes all per-chunk JSON items along with the aggregated report.

## Notes & Tips
- **Determinism**: For consistent runs, pin `--fetch http` or `--fetch selenium` and/or use `--no-discover` with a fixed policy URL.
- **International sites**: The HTTP client sets `Accept-Language: en-US,en;q=0.9` to reduce locale variance.
- **Selenium**: Ensure Chrome/Chromium exists; `chromedriver-autoinstaller` will fetch a matching driver automatically.

## Troubleshooting
- **`ImportError: lxml.html.clean ...`**  
  Ensure `lxml[html_clean]` is installed (it’s included in `requirements.txt`).
- **Very low or inconsistent scores**  
  Try `--fetch selenium` or analyze the explicit policy URL with `--no-discover`. Some sites serve different content per region/session.

## Security & Ethics
This tool provides **automated analysis heuristics** and LLM-generated assessments. Treat results as decision support, not legal advice. Always review the original policy and consult qualified counsel for compliance-critical use cases.

## License
See `LICENSE` for details.
