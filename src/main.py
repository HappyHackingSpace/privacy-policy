import argparse
import gzip
import io
import json
import os
import pathlib
import sys
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urljoin, urlparse
from src.analyzer.prompts import SYSTEM_SCORER, build_user_prompt
from src.analyzer.scoring import aggregate_chunk_results
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import OpenAI

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import chromedriver_autoinstaller

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

try:
    import trafilatura

    _HAS_TRAFILATURA = True
except Exception:
    trafilatura = None  # type: ignore[assignment]
    _HAS_TRAFILATURA = False


load_dotenv()

_PRIVACY_CUES = (
    "privacy",
    "privacy-policy",
    "privacy_notice",
    "privacy-notice",
    "gizlilik",
    "gizlilik-politik",
    "veri koruma",
    "privacidad",
    "politica de privacidad",
    "privacidade",
    "politica de privacidade",
    "datenschutz",
    "confidentialité",
    "politique de confidentialité",
    "informativa privacy",
    "informativa sulla privacy",
    "個人情報",
    "プライバシー",
    "隐私",
    "隱私",
    "개인정보",
    "privatsphäre",
)

_COMMON_PATHS = [
    "/privacy",
    "/privacy-policy",
    "/privacy_policy",
    "/legal/privacy",
    "/legal/privacy-policy",
    "/policies/privacy",
    "/en/privacy",
    "/en/privacy-policy",
    "/tr/gizlilik",
    "/tr/gizlilik-politikasi",
]


def _is_privacy_like(s: str) -> bool:
    """Heuristic check for privacy-related terms in a string."""
    s = (s or "").lower()
    return any(k in s for k in _PRIVACY_CUES)


def _http_get(url: str, timeout: int = 15) -> Optional[requests.Response]:
    """HTTP GET with basic headers and redirects allowed."""
    try:
        r = requests.get(
            url,
            timeout=timeout,
            allow_redirects=True,
            headers={
                "User-Agent": "PrivacyPolicyAnalyzer/0.2 (+https://example.org)",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
            },
        )
        return r if (r.status_code < 400 and r.text) else None
    except Exception:
        return None


def _fetch_text(url: str, timeout: int = 12) -> Optional[str]:
    """Fetch raw text content via GET."""
    r = _http_get(url, timeout=timeout)
    return r.text if r else None


def _head_ok(url: str, timeout: int = 8) -> bool:
    """Lightweight existence probe using HEAD; redirects considered OK."""
    try:
        r = requests.head(
            url,
            timeout=timeout,
            allow_redirects=True,
            headers={
                "User-Agent": "PrivacyPolicyAnalyzer/0.2 (+https://example.org)",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
            },
        )
        if 200 <= r.status_code < 300:
            return True
        if r.status_code in (301, 302, 303, 307, 308):
            return True
        return False
    except Exception:
        return False


def _extract_text_http(url: str) -> Optional[str]:
    if _HAS_TRAFILATURA:
        try:
            downloaded = trafilatura.fetch_url(url)
            if downloaded:
                text = trafilatura.extract(downloaded, include_formatting=False) or ""
                t = text.strip()
                return t if len(t) >= 400 else None
        except Exception:
            pass
    r = _http_get(url)
    if not r:
        return None
    soup = BeautifulSoup(r.text, "html.parser")
    body = soup.find("body")
    t = body.get_text("\n").strip() if body else ""
    return t if len(t) >= 400 else None


def fetch_content_with_selenium(url: str) -> Optional[str]:
    """Return visible text using headless Chrome; robust for dynamic pages."""
    chromedriver_autoinstaller.install()
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-extensions")
    opts.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    )
    driver = webdriver.Chrome(options=opts)
    try:
        driver.get(url)
        WebDriverWait(driver, 12).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        return driver.find_element(By.TAG_NAME, "body").get_attribute("innerText")
    except Exception:
        return None
    finally:
        driver.quit()


def fetch_policy_text(url: str, prefer: str = "auto") -> Optional[str]:
    """Fetch policy text using HTTP first; fallback to Selenium if needed."""
    if prefer in ("auto", "http"):
        t = _extract_text_http(url)
        if t:
            return t
        if prefer == "http":
            return None
    return fetch_content_with_selenium(url)


def _light_verify(url: str) -> bool:
    """Low-cost check that a URL likely points to a privacy policy page."""
    t = _extract_text_http(url)
    if not t:
        return False
    low = t[:3000].lower()
    return any(k in low for k in _PRIVACY_CUES) and len(t) >= 500


def _get_sitemaps_from_robots(base_url: str) -> List[str]:
    """Extract sitemap URLs from robots.txt; also try the default /sitemap.xml."""
    parsed = urlparse(base_url)
    robots = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    out: List[str] = []
    txt = _fetch_text(robots)
    if txt:
        for line in txt.splitlines():
            line = line.strip()
            if line.lower().startswith("sitemap:"):
                sm = line.split(":", 1)[1].strip()
                if sm:
                    out.append(sm)
    default_sm = f"{parsed.scheme}://{parsed.netloc}/sitemap.xml"
    if default_sm not in out:
        out.append(default_sm)
    seen, uniq = set(), []
    for u in out:
        if u not in seen:
            seen.add(u)
            uniq.append(u)
    return uniq


def _fetch_sitemap_urls(url: str, max_urls: int = 50) -> List[str]:
    """Return privacy-like URLs found in the sitemap (gz and index supported)."""
    r = _http_get(url)
    if not r:
        return []
    data = r.content
    if url.endswith(".gz"):
        try:
            data = gzip.GzipFile(fileobj=io.BytesIO(data)).read()
        except Exception:
            return []
    try:
        root = ET.fromstring(data)
    except Exception:
        return []
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls: List[str] = []
    if root.tag.endswith("sitemapindex"):
        for i, loc in enumerate(root.findall(".//sm:loc", ns)):
            if i >= 5:
                break
            child = (loc.text or "").strip()
            urls.extend(_fetch_sitemap_urls(child, max_urls=max_urls))
            if len(urls) >= max_urls:
                break
    else:
        for loc in root.findall(".//sm:loc", ns):
            u = (loc.text or "").strip()
            if u and _is_privacy_like(u):
                urls.append(u)
                if len(urls) >= max_urls:
                    break
    seen, uniq = set(), []
    for u in urls:
        if u not in seen:
            seen.add(u)
            uniq.append(u)
    return uniq


def _discover_candidates_from_html(start_url: str) -> List[str]:
    """Collect privacy-like links from the HTML of the given page."""
    r = _http_get(start_url)
    if not r:
        return []
    soup = BeautifulSoup(r.text, "html.parser")
    links: List[str] = []
    for a in soup.find_all("a", href=True):
        text = (a.get_text(" ") or "") + " " + a["href"]  # type: ignore[operator, index]
        if _is_privacy_like(text):
            links.append(urljoin(r.url, a["href"]))  # type: ignore[index]
    seen, uniq = set(), []
    for u in links:
        if u not in seen:
            seen.add(u)
            uniq.append(u)
    return uniq


def _extract_text_quality(url: str) -> Tuple[Optional[str], Optional[str]]:
    """Extract and sanity-check text content for policy-ness."""
    if _HAS_TRAFILATURA:
        try:
            downloaded = trafilatura.fetch_url(url)
            if not downloaded:
                return None, None
            text = trafilatura.extract(downloaded, include_formatting=False) or ""
            t = text.strip()
            if len(t) >= 500 and _is_privacy_like(t[:2000]):
                return t, url
            return None, url
        except Exception:
            return None, None
    r = _http_get(url)
    if not r:
        return None, None
    soup = BeautifulSoup(r.text, "html.parser")
    body = soup.find("body")
    t = (body.get_text("\n").strip() if body else "")[:4000]
    if len(t) >= 500 and _is_privacy_like(t):
        return t, r.url
    return None, r.url


def resolve_privacy_url(input_url: str) -> Tuple[str, Optional[str]]:
    """Resolve a likely privacy policy URL starting from any given page."""
    if _is_privacy_like(input_url):
        return input_url, None

    parsed = urlparse(input_url)
    base = f"{parsed.scheme}://{parsed.netloc}".rstrip("/")

    path_heads: List[str] = []
    for p in _COMMON_PATHS:
        cand = base + p
        if _head_ok(cand) or _light_verify(cand):
            if _light_verify(cand):
                return cand, input_url
            path_heads.append(cand)

    for cand in path_heads:
        if _light_verify(cand):
            return cand, input_url

    for sm in _get_sitemaps_from_robots(base):
        for cand in _fetch_sitemap_urls(sm, max_urls=50):
            if _light_verify(cand):
                return cand, input_url

    for cand in _discover_candidates_from_html(input_url):
        text, _ = _extract_text_quality(cand)
        if text:
            return cand, input_url

    return input_url, None


def split_text_into_chunks(
    text: str, chunk_size: int = 3500, chunk_overlap: int = 350
) -> List[str]:
    """Split text into chunks using paragraph-first recursive boundaries."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return splitter.split_text(text or "")


def analyze_chunk_json(text_chunk: str, model: str) -> Optional[Dict[str, Any]]:
    """Analyze a text chunk with the LLM and return one JSON object."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set. Configure your .env file.")
    client = OpenAI(api_key=api_key)
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_SCORER},
            {"role": "user", "content": build_user_prompt(text_chunk)},
        ],
        temperature=0,
        max_tokens=600,
        response_format={"type": "json_object"},
    )
    content = (resp.choices[0].message.content or "").strip()
    try:
        return json.loads(content)  # type: ignore[no-any-return]
    except Exception:
        return None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Privacy Policy Analyzer (auto-discovery + JSON scoring)"
    )
    parser.add_argument("--url", type=str, help="Site or policy URL to analyze")
    parser.add_argument(
        "--model",
        type=str,
        default=os.getenv("OPENAI_MODEL", "gpt-4o"),
        help="OpenAI chat model, e.g., gpt-4o",
    )
    parser.add_argument(
        "--chunk-size", type=int, default=3500, help="Character-based chunk size"
    )
    parser.add_argument(
        "--chunk-overlap", type=int, default=350, help="Overlap between chunks"
    )
    parser.add_argument(
        "--max-chunks",
        type=int,
        default=30,
        help="Hard cap for analyzed chunks (tail chunks are merged).",
    )
    parser.add_argument(
        "--report",
        type=str,
        choices=["summary", "detailed", "full"],
        default="summary",
        help="Report detail level",
    )
    parser.add_argument(
        "--fetch",
        type=str,
        choices=["auto", "http", "selenium"],
        default="auto",
        help="Fetch method preference",
    )
    parser.add_argument(
        "--no-discover",
        action="store_true",
        help="Skip auto-discovery and analyze the given URL as-is",
    )

    args = parser.parse_args()
    input_url = args.url or input("Enter a site (or privacy policy) URL: ").strip()

    resolved_url, _ = (
        (input_url, None) if args.no_discover else resolve_privacy_url(input_url)
    )

    content = fetch_policy_text(resolved_url, prefer=args.fetch)
    if not content:
        print(
            json.dumps(
                {
                    "status": "error",
                    "reason": "fetch_failed",
                    "url": input_url,
                    "resolved_url": resolved_url,
                }
            )
        )
        return

    chunks = split_text_into_chunks(
        content, chunk_size=args.chunk_size, chunk_overlap=args.chunk_overlap
    )
    if not chunks:
        print(
            json.dumps(
                {
                    "status": "error",
                    "reason": "no_chunks",
                    "url": input_url,
                    "resolved_url": resolved_url,
                }
            )
        )
        return

    if len(chunks) > args.max_chunks:
        head = chunks[: args.max_chunks - 1]
        tail = " ".join(chunks[args.max_chunks - 1 :])
        chunks = head + [tail]

    results: List[Dict[str, Any]] = []
    for i, chunk in enumerate(chunks, 1):
        print(f"Analyzing chunk {i}/{len(chunks)}...")
        j = analyze_chunk_json(chunk, model=args.model)
        if isinstance(j, dict) and "scores" in j:
            j["index"] = i
            results.append(j)

    if not results:
        print(
            json.dumps(
                {
                    "status": "error",
                    "reason": "no_valid_scores",
                    "url": input_url,
                    "resolved_url": resolved_url,
                }
            )
        )
        return

    agg = aggregate_chunk_results(results)
    base = {
        "status": "ok",
        "url": input_url,
        "resolved_url": resolved_url,
        "model": args.model,
        "chunks": len(chunks),
        "valid_chunks": len(results),
    }

    if args.report == "summary":
        out = {
            **base,
            "overall_score": agg["overall_score"],
            "confidence": agg["confidence"],
            "top_strengths": agg["top_strengths"],
            "top_risks": agg["top_risks"],
            "red_flags_count": len(agg["red_flags"]),
        }
    elif args.report == "detailed":
        out = {**base, **agg}
    else:
        out = {**base, **agg, "chunks": results}

    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
