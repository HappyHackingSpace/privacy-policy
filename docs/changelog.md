# Changelog

All notable changes to the Privacy Policy Analyzer project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Auto-discovery of likely privacy policy URLs (common paths, robots/sitemaps, in-page links)
- Web content extraction via requests + BeautifulSoup; optional Trafilatura; Selenium fallback for dynamic pages
- OpenAI-powered analysis (Chat Completions) with a fixed JSON scoring schema
- Weighted scoring across ten dimensions aggregated to a 0–100 overall score
- CLI (argparse) with `summary`, `detailed`, and `full` report modes
- Tunable chunking (`--chunk-size`, `--chunk-overlap`, `--max-chunks`) and fetch strategy (`--fetch auto|http|selenium`)
- Comprehensive documentation with MkDocs and Material theme
- JSON output suitable for pipelines, dashboards, or audits
- Pre-commit hooks configuration
- CI workflows (GitHub Actions) and automated release pipeline
- Project metadata and tooling via `pyproject.toml`
- Integration with the Happy Hacking Space organization

### Changed
- Nothing yet

### Deprecated
- Nothing yet

### Removed
- Nothing yet

### Fixed
- Nothing yet

### Security
- Nothing yet

---

## Legend

- **Added** for new features
- **Changed** for changes in existing functionality
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** for vulnerability fixes
