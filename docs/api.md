# API Reference

This project currently exposes a **command-line interface (CLI)** rather than a stable importable class-based API.  
Use the CLI to discover, extract, and evaluate privacy policies, and consume the JSON it prints to stdout.

## 📋 Table of Contents

- [Command](#command)
- [Options](#options)
- [Output Schemas](#output-schemas)
- [Categories & Weights](#categories--weights)
- [Environment Variables](#environment-variables)
- [Exit Codes](#exit-codes)
- [Examples](#examples)

## Command

```bash
# Using uv
uv run python src/main.py [OPTIONS]

# Or module form
python -m src.main [OPTIONS]
```

**Required:** `--url` (site URL for auto-discovery or a direct privacy policy URL)

## Options

- `--url TEXT`  
  Input URL. If it’s a homepage or non-policy page, the tool will try to resolve a likely policy URL.

- `--model TEXT`  
  Override the OpenAI model (defaults to `OPENAI_MODEL` or `gpt-4o`).

- `--chunk-size INT` (default: `3500`)  
  Character-based chunk size for splitting long policies.

- `--chunk-overlap INT` (default: `350`)  
  Overlap between chunks.

- `--max-chunks INT` (default: `30`)  
  Hard cap for analyzed chunks; remaining tail chunks are merged.

- `--report {summary|detailed|full}` (default: `summary`)  
  Output verbosity level.

- `--fetch {auto|http|selenium}` (default: `auto`)  
  Extraction method. `auto` tries HTTP first and can fall back to Selenium.

- `--no-discover`  
  Analyze the given URL as-is (skip auto-discovery).

## Output Schemas

The CLI prints **JSON** to stdout.

### `summary`

```json
{
"status": "ok",
"url": "https://example.com",
"resolved_url": "https://example.com/privacy",
"model": "gpt-4o",
"chunks": 12,
"valid_chunks": 11,
"overall_score": 82.5,
"confidence": 0.9,
"top_strengths": [["user_rights_and_redress", 8.7], ["security_and_breach", 8.2], ["transparency_and_notice", 7.9]],
"top_risks": [["cross_border_transfers", 5.1], ["retention_and_deletion", 6.0], ["secondary_use_and_limits", 6.2]],
"red_flags_count": 2
}
```

### `detailed`
Adds:
- `category_scores`: `{ [category]: { "score": number (0–10), "weight": number, "rationale": string } }`
- `red_flags`: `string[]`
- `recommendations`: `string[]`

### `full`
Adds:
- `chunks`: raw per-chunk model outputs (including per-chunk `scores`, `rationales`, and optional `red_flags`/`notes`)

## Categories & Weights

Each category is scored **0–10** per chunk by the model; scores are averaged and combined with the weights below to form the **0–100 overall score**.

- **lawful_basis_and_purpose** — weight **12**  
  Clarity of purposes/justifications; purpose limitation; consent/choice clarity where relevant.

- **collection_and_minimization** — weight **10**  
  Specificity/necessity of collected data categories; proportionality/minimization.

- **secondary_use_and_limits** — weight **8**  
  Limits on additional/compatible uses; avoidance of vague blanket purposes.

- **retention_and_deletion** — weight **8**  
  Concrete periods or clear criteria; deletion/archiving language; avoiding indefinite retention without justification.

- **third_parties_and_processors** — weight **12**  
  Processors/third parties, categories & purposes, and role clarity (controller/processor/joint).

- **cross_border_transfers** — weight **8**  
  Destinations (if any) and plain-language safeguards for international transfers.

- **user_rights_and_redress** — weight **14**  
  How rights can be exercised (access/rectification/erasure/restriction/portability/objection), timelines, contacts, escalation paths.

- **security_and_breach** — weight **12**  
  Organizational/technical measures; breach handling language; security/DPO contact if applicable.

- **transparency_and_notice** — weight **8**  
  Plain language, structure, contact details, change/version notices, cookie/consent pointers where relevant.

- **sensitive_children_ads_profiling** — weight **8**  
  Handling of sensitive/special categories; children data statements/age gates; selling/sharing for ads and opt-out/limit choices; automated decisions/profiling.

## Environment Variables

- `OPENAI_API_KEY` (**required**)  
- `OPENAI_MODEL` (optional; default model if `--model` is not set)

## Exit Codes

- `0`: success (JSON printed)  
- non-zero: error (a JSON error payload is printed where possible)

## Examples

Analyze a homepage (auto-discovery):

```bash
uv run python src/main.py --url https://example.com
```

Analyze a known policy URL directly:

```bash
uv run python src/main.py --url https://example.com/privacy-policy --no-discover --report detailed
```

Force Selenium for a client-rendered page:

```bash
uv run python src/main.py --url https://example.com/privacy --fetch selenium
```

Tune chunking for very long policies:

```bash
uv run python src/main.py --url https://example.com --chunk-size 3000 --chunk-overlap 300 --max-chunks 25
```
