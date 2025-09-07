# API Reference

Complete API documentation for the Privacy Policy Analyzer.

## 📋 Table of Contents

- [PrivacyPolicyAnalyzer](#privacypolicyanalyzer)
- [AnalysisResult](#analysisresult)
- [WebExtractor](#webextractor)
- [ScoringEngine](#scoringengine)
- [Exceptions](#exceptions)
- [Utilities](#utilities)

## PrivacyPolicyAnalyzer

The main class for analyzing privacy policies.

### Constructor

```python
PrivacyPolicyAnalyzer(
    api_key: Optional[str] = None,
    model: str = "gpt-4",
    temperature: float = 0.1,
    cache_dir: Optional[str] = None,
    cache_ttl: int = 3600,
    timeout: int = 30,
    max_retries: int = 3,
    include_recommendations: bool = True,
    detailed_analysis: bool = True,
    language: str = "en",
    debug: bool = False
)
```

#### Parameters

- **api_key** (`Optional[str]`): OpenAI API key. If not provided, will look for `OPENAI_API_KEY` environment variable.
- **model** (`str`): OpenAI model to use for analysis. Default: `"gpt-4"`.
- **temperature** (`float`): Temperature for text generation. Default: `0.1`.
- **cache_dir** (`Optional[str]`): Directory for caching results. Default: `None` (no caching).
- **cache_ttl** (`int`): Cache time-to-live in seconds. Default: `3600` (1 hour).
- **timeout** (`int`): Request timeout in seconds. Default: `30`.
- **max_retries** (`int`): Maximum number of retries for failed requests. Default: `3`.
- **include_recommendations** (`bool`): Whether to include recommendations in results. Default: `True`.
- **detailed_analysis** (`bool`): Whether to perform detailed analysis. Default: `True`.
- **language** (`str`): Language for analysis. Default: `"en"`.
- **debug** (`bool`): Enable debug logging. Default: `False`.

### Methods

#### analyze_url

```python
analyze_url(
    url: str,
    extract_method: str = "auto",
    timeout: Optional[int] = None,
    follow_redirects: bool = True,
    custom_prompts: Optional[Dict[str, str]] = None
) -> AnalysisResult
```

Analyze a privacy policy from a URL.

**Parameters:**
- **url** (`str`): URL of the privacy policy page.
- **extract_method** (`str`): Method for extracting content. Options: `"auto"`, `"trafilatura"`,
  `"beautifulsoup"`. Default: `"auto"`.
- **timeout** (`Optional[int]`): Override default timeout for this request.
- **follow_redirects** (`bool`): Whether to follow redirects. Default: `True`.
- **custom_prompts** (`Optional[Dict[str, str]]`): Custom prompts for analysis.

**Returns:** `AnalysisResult` object with analysis results.

**Raises:**
- `ExtractionError`: If content extraction fails.
- `AnalysisError`: If analysis fails.
- `NetworkError`: If network request fails.

#### analyze_text

```python
analyze_text(
    text: str,
    custom_prompts: Optional[Dict[str, str]] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> AnalysisResult
```

Analyze privacy policy text directly.

**Parameters:**
- **text** (`str`): Privacy policy text to analyze.
- **custom_prompts** (`Optional[Dict[str, str]]`): Custom prompts for analysis.
- **metadata** (`Optional[Dict[str, Any]]`): Additional metadata for the analysis.

**Returns:** `AnalysisResult` object with analysis results.

**Raises:**
- `AnalysisError`: If analysis fails.

#### analyze_file

```python
analyze_file(
    file_path: str,
    encoding: str = "utf-8",
    custom_prompts: Optional[Dict[str, str]] = None
) -> AnalysisResult
```

Analyze a privacy policy from a local file.

**Parameters:**
- **file_path** (`str`): Path to the privacy policy file.
- **encoding** (`str`): File encoding. Default: `"utf-8"`.
- **custom_prompts** (`Optional[Dict[str, str]]`): Custom prompts for analysis.

**Returns:** `AnalysisResult` object with analysis results.

**Raises:**
- `FileNotFoundError`: If file doesn't exist.
- `AnalysisError`: If analysis fails.

#### analyze_batch

```python
analyze_batch(
    inputs: List[Union[str, Dict[str, Any]]],
    max_concurrent: int = 5,
    progress_callback: Optional[Callable[[int, int], None]] = None
) -> List[AnalysisResult]
```

Analyze multiple privacy policies in batch.

**Parameters:**
- **inputs** (`List[Union[str, Dict[str, Any]]]`): List of URLs, text, or file paths to analyze.
- **max_concurrent** (`int`): Maximum concurrent analyses. Default: `5`.
- **progress_callback** (`Optional[Callable[[int, int], None]]`): Callback for progress updates.

**Returns:** List of `AnalysisResult` objects.

#### compare_results

```python
compare_results(results: List[AnalysisResult]) -> ComparisonResult
```

Compare multiple analysis results.

**Parameters:**
- **results** (`List[AnalysisResult]`): List of analysis results to compare.

**Returns:** `ComparisonResult` object with comparison data.

#### clear_cache

```python
clear_cache() -> None
```

Clear the analysis cache.

## AnalysisResult

Represents the result of a privacy policy analysis.

### Properties

- **overall_score** (`float`): Overall privacy score (0-100).
- **dimension_scores** (`Dict[str, float]`): Scores for each dimension.
- **confidence** (`float`): Analysis confidence (0-100).
- **findings** (`List[str]`): Key findings from the analysis.
- **recommendations** (`List[str]`): Recommendations for improvement.
- **raw_content** (`str`): Raw extracted content.
- **analysis_time** (`float`): Time taken for analysis in seconds.
- **metadata** (`Dict[str, Any]`): Additional metadata.
- **custom_scores** (`Dict[str, float]`): Custom analysis scores.

### Methods

#### export_json

```python
export_json(file_path: str) -> None
```

Export results to JSON file.

#### export_csv

```python
export_csv(file_path: str) -> None
```

Export results to CSV file.

#### export_html

```python
export_html(file_path: str, template: Optional[str] = None) -> None
```

Export results to HTML report.

## WebExtractor

Utility class for extracting content from web pages.

### Constructor

```python
WebExtractor(
    timeout: int = 30,
    max_retries: int = 3,
    user_agent: str = "PrivacyPolicyAnalyzer/1.0"
)
```

### Methods

#### extract

```python
extract(
    url: str,
    method: str = "auto",
    follow_redirects: bool = True
) -> str
```

Extract content from a URL.

**Parameters:**
- **url** (`str`): URL to extract content from.
- **method** (`str`): Extraction method. Options: `"auto"`, `"trafilatura"`, `"beautifulsoup"`.
- **follow_redirects** (`bool`): Whether to follow redirects.

**Returns:** Extracted text content.

**Raises:**
- `ExtractionError`: If extraction fails.

## ScoringEngine

Engine for scoring privacy policies.

### Constructor

```python
ScoringEngine(
    model: str = "gpt-4",
    temperature: float = 0.1,
    custom_prompts: Optional[Dict[str, str]] = None
)
```

### Methods

#### score_policy

```python
score_policy(
    content: str,
    dimensions: Optional[List[str]] = None
) -> Dict[str, float]
```

Score a privacy policy across different dimensions.

**Parameters:**
- **content** (`str`): Privacy policy content.
- **dimensions** (`Optional[List[str]]`): List of dimensions to score.

**Returns:** Dictionary mapping dimensions to scores.

## Exceptions

### PrivacyPolicyError

Base exception for all privacy policy analyzer errors.

```python
class PrivacyPolicyError(Exception):
    pass
```

### ExtractionError

Raised when content extraction fails.

```python
class ExtractionError(PrivacyPolicyError):
    def __init__(self, message: str, url: Optional[str] = None):
        self.url = url
        super().__init__(message)
```

### AnalysisError

Raised when analysis fails.

```python
class AnalysisError(PrivacyPolicyError):
    def __init__(self, message: str, content: Optional[str] = None):
        self.content = content
        super().__init__(message)
```

### NetworkError

Raised when network requests fail.

```python
class NetworkError(PrivacyPolicyError):
    def __init__(self, message: str, url: Optional[str] = None, status_code: Optional[int] = None):
        self.url = url
        self.status_code = status_code
        super().__init__(message)
```

## Utilities

### Configuration

```python
from privacy_policy.config import Config

# Load configuration from environment
config = Config.from_env()

# Load configuration from file
config = Config.from_file("config.yaml")

# Create configuration programmatically
config = Config(
    api_key="your-key",
    model="gpt-4",
    timeout=30
)
```

### Logging

```python
from privacy_policy.logging import setup_logging

# Setup logging
setup_logging(level="INFO", log_file="analyzer.log")

# Use logger
import logging
logger = logging.getLogger("privacy_policy")
logger.info("Analysis started")
```

### Caching

```python
from privacy_policy.cache import Cache

# Create cache
cache = Cache(cache_dir="./cache", ttl=3600)

# Store result
cache.store("key", result)

# Retrieve result
result = cache.retrieve("key")

# Clear cache
cache.clear()
```

## Examples

### Basic Usage

```python
from privacy_policy import PrivacyPolicyAnalyzer

# Initialize analyzer
analyzer = PrivacyPolicyAnalyzer(api_key="your-key")

# Analyze URL
result = analyzer.analyze_url("https://example.com/privacy")

# Access results
print(f"Score: {result.overall_score}")
print(f"Findings: {result.findings}")
```

### Custom Analysis

```python
# Custom prompts
custom_prompts = {
    "data_collection": "Focus on data collection practices",
    "user_rights": "Analyze user rights and controls"
}

# Analyze with custom prompts
result = analyzer.analyze_text(
    policy_text,
    custom_prompts=custom_prompts
)

# Access custom scores
print(f"Data Collection Score: {result.custom_scores['data_collection']}")
```

### Batch Processing

```python
# Analyze multiple policies
urls = [
    "https://company1.com/privacy",
    "https://company2.com/privacy"
]

results = analyzer.analyze_batch(urls)

# Compare results
comparison = analyzer.compare_results(results)
print(comparison.summary)
```

### Error Handling

```python
from privacy_policy.exceptions import ExtractionError, AnalysisError

try:
    result = analyzer.analyze_url("https://example.com/privacy")
except ExtractionError as e:
    print(f"Failed to extract content: {e}")
    print(f"URL: {e.url}")
except AnalysisError as e:
    print(f"Analysis failed: {e}")
    print(f"Content length: {len(e.content) if e.content else 0}")
```

---

*For more examples and advanced usage, see the [User Guide](user-guide.md).*
