"""
Robust Job Description Scraper
Uses Playwright for JS-rendered pages + BeautifulSoup for parsing + markdownify for clean output.
No crawl4ai dependency. Handles Greenhouse, Lever, Workday, Ashby, LinkedIn, Indeed, and generic ATS pages.
"""

import asyncio
import re
import json
import hashlib
from dataclasses import dataclass, field, asdict
from typing import Optional
from urllib.parse import urlparse

from playwright.async_api import async_playwright, Page, Browser, TimeoutError as PlaywrightTimeout
from bs4 import BeautifulSoup, Tag
from markdownify import markdownify as md


# ---------------------------------------------------------------------------
# Data Model
# ---------------------------------------------------------------------------

@dataclass
class JobDescription:
    """Structured representation of a scraped job posting."""
    url: str
    job_title: str = ""
    company_name: str = ""
    location: str = ""
    job_type: str = ""
    salary_range: str = ""
    description: str = ""          # cleaned markdown of the core JD
    raw_html: str = ""             # raw HTML of extracted content block
    success: bool = True
    error: Optional[str] = None
    scraper_notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        d = asdict(self)
        d.pop("raw_html")  # usually too large for JSON output
        return d

    def to_resume_prompt(self) -> str:
        """Format for feeding into a resume-tailoring LLM prompt."""
        parts = [
            f"## {self.job_title}" if self.job_title else "",
            f"**Company:** {self.company_name}" if self.company_name else "",
            f"**Location:** {self.location}" if self.location else "",
            f"**Type:** {self.job_type}" if self.job_type else "",
            f"**Salary:** {self.salary_range}" if self.salary_range else "",
            "",
            self.description,
        ]
        return "\n".join(p for p in parts if p is not None).strip()


# ---------------------------------------------------------------------------
# ATS-Specific Selectors  (the secret sauce)
# ---------------------------------------------------------------------------
# Each ATS has known DOM structures. We define CSS selectors for the main
# content container so we skip nav/footer/cookie junk entirely instead of
# trying to filter it out after the fact.

ATS_PROFILES: dict[str, dict] = {
    "greenhouse": {
        "hosts": ["boards.greenhouse.io", "boards.eu.greenhouse.io"],
        "content_selector": "#content, #app_body, .app-body",
        "title_selector": ".app-title, .company-name + h1, h1.heading",
        "company_selector": ".company-name, span.company-name",
        "location_selector": ".location, .body--metadata",
        "wait_selector": "#content",
    },
    "lever": {
        "hosts": ["jobs.lever.co"],
        "content_selector": ".content, .section-wrapper, .posting-page",
        "title_selector": "h2, .posting-headline h2",
        "company_selector": ".main-header-logo img[alt]",
        "location_selector": ".location, .sort-by-time",
        "wait_selector": ".posting-headline",
    },
    "ashby": {
        "hosts": ["jobs.ashbyhq.com"],
        "content_selector": '[data-testid="job-posting"], .ashby-job-posting-brief-description, main',
        "title_selector": "h1, h2",
        "company_selector": 'a[data-testid="org-name"], .ashby-job-posting-org-name',
        "location_selector": '[data-testid="job-location"], .ashby-job-posting-location',
        "wait_selector": "main",
    },
    "workday": {
        "hosts": ["myworkdayjobs.com", "wd5.myworkdayjobs.com"],
        "host_pattern": r".*\.myworkdayjobs\.com",
        "content_selector": '[data-automation-id="jobPostingDescription"], .css-cygeeu, main',
        "title_selector": '[data-automation-id="jobPostingHeader"] h2, h2',
        "company_selector": '[data-automation-id="jobPostingCompanyName"]',
        "location_selector": '[data-automation-id="locations"], .css-129m7dg',
        "wait_selector": '[data-automation-id="jobPostingDescription"]',
        "extra_wait_ms": 3000,  # Workday is notoriously slow
    },
    "linkedin": {
        "hosts": ["linkedin.com", "www.linkedin.com"],
        "content_selector": ".description__text, .show-more-less-html, .jobs-description, article",
        "title_selector": "h1, .top-card-layout__title, .jobs-unified-top-card__job-title",
        "company_selector": ".topcard__org-name-link, .jobs-unified-top-card__company-name a",
        "location_selector": ".topcard__flavor--bullet, .jobs-unified-top-card__bullet",
        "wait_selector": ".description__text, .show-more-less-html, article",
    },
    "indeed": {
        "hosts": ["indeed.com", "www.indeed.com"],
        "content_selector": "#jobDescriptionText, .jobsearch-JobComponent-description",
        "title_selector": "h1.jobsearch-JobInfoHeader-title, h1",
        "company_selector": '[data-company-name], .jobsearch-InlineCompanyRating a',
        "location_selector": '[data-testid="job-location"], .jobsearch-JobInfoHeader-subtitle div:nth-child(2)',
        "wait_selector": "#jobDescriptionText",
    },
    "smartrecruiters": {
        "hosts": ["jobs.smartrecruiters.com"],
        "content_selector": ".job-sections, .description, main",
        "title_selector": "h1, .job-title",
        "company_selector": ".company-name",
        "location_selector": ".job-location",
        "wait_selector": ".job-sections, main",
    },
    "icims": {
        "hosts": ["careers-"],
        "host_pattern": r".*\.icims\.com",
        "content_selector": ".iCIMS_JobContent, .iCIMS_MainWrapper, main",
        "title_selector": "h1, .iCIMS_Header",
        "company_selector": ".iCIMS_CompanyName",
        "location_selector": ".iCIMS_JobHeaderData",
        "wait_selector": ".iCIMS_JobContent, main",
    },
}

# Generic fallback selectors (ordered by specificity)
GENERIC_CONTENT_SELECTORS = [
    # Role/article containers
    'article[class*="job"]',
    'div[class*="job-description"]',
    'div[class*="jobDescription"]',
    'div[class*="job_description"]',
    'div[class*="posting-"]',
    'div[id*="job-description"]',
    'div[id*="jobDescription"]',
    'section[class*="job"]',
    # Generic content wrappers
    "main",
    'article',
    '[role="main"]',
    "#content",
    ".content",
]

# Tags to always strip from extracted content
STRIP_TAGS = {"nav", "footer", "header", "aside", "script", "style", "noscript", "iframe", "form", "svg"}

# Sections that are almost never part of the core JD requirements/responsibilities
NOISE_SECTION_PATTERNS = re.compile(
    r"(?i)^#{1,4}\s*("
    r"equal\s+opportunity|eeo\b|e\.e\.o|"
    r"our\s+(culture|values|mission|vision|story|team)|"
    r"about\s+(us|the\s+company|our\s+company)|"
    r"why\s+(join|you.ll\s+love|work\s+here)|"
    r"what\s+we\s+offer|"
    r"benefits\b|perks\b|"
    r"compensation\s*(and|&)\s*benefits|"
    r"how\s+to\s+apply|"
    r"privacy\s+(policy|notice)|"
    r"cookie|disclaimer|"
    r"accommodation|"
    r"diversity.{0,20}(equity|inclusion)|"
    r"additional\s+information"
    r")"
)


# ---------------------------------------------------------------------------
# Scraper
# ---------------------------------------------------------------------------

class JobScraper:
    """
    Robust async job description scraper.

    Usage:
        async with JobScraper() as scraper:
            jd = await scraper.scrape("https://boards.greenhouse.io/...")
            print(jd.to_resume_prompt())
    """

    def __init__(
        self,
        headless: bool = True,
        timeout_ms: int = 30_000,
        trim_noise_sections: bool = True,
        max_description_chars: int = 15_000,
    ):
        self.headless = headless
        self.timeout_ms = timeout_ms
        self.trim_noise = trim_noise_sections
        self.max_chars = max_description_chars
        self._browser: Optional[Browser] = None
        self._pw = None

    # -- Context manager --------------------------------------------------

    async def __aenter__(self):
        self._pw = await async_playwright().start()
        self._browser = await self._pw.chromium.launch(
            headless=self.headless,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
            ],
        )
        return self

    async def __aexit__(self, *exc):
        if self._browser:
            await self._browser.close()
        if self._pw:
            await self._pw.stop()

    # -- Public API -------------------------------------------------------

    async def scrape(self, url: str) -> JobDescription:
        """Scrape a single job URL and return structured JobDescription."""
        jd = JobDescription(url=url)
        try:
            page = await self._new_page()
            await self._navigate(page, url, jd)
            html = await page.content()
            soup = BeautifulSoup(html, "lxml")

            # Detect ATS
            profile = self._detect_ats(url)
            if profile:
                jd.scraper_notes.append(f"Detected ATS: {profile['_name']}")

            # Remove junk tags globally
            for tag_name in STRIP_TAGS:
                for tag in soup.find_all(tag_name):
                    tag.decompose()

            # Extract metadata (title, company, location)
            self._extract_metadata(soup, profile, jd)

            # Extract the main content container
            content_el = self._find_content_container(soup, profile)
            if content_el:
                jd.raw_html = str(content_el)
                raw_md = md(str(content_el), heading_style="ATX", strip=["img", "a"])
            else:
                jd.scraper_notes.append("No specific content container found; using <body>")
                body = soup.find("body")
                jd.raw_html = str(body) if body else str(soup)
                raw_md = md(jd.raw_html, heading_style="ATX", strip=["img", "a"])

            # Clean the markdown
            jd.description = self._clean_markdown(raw_md)

            # Truncate if absurdly long
            if len(jd.description) > self.max_chars:
                jd.description = jd.description[: self.max_chars] + "\n\n[...truncated]"
                jd.scraper_notes.append(f"Truncated to {self.max_chars} chars")

            await page.close()

        except PlaywrightTimeout:
            jd.success = False
            jd.error = f"Page load timed out after {self.timeout_ms}ms"
        except Exception as e:
            jd.success = False
            jd.error = f"{type(e).__name__}: {e}"

        return jd

    async def scrape_many(self, urls: list[str], concurrency: int = 3) -> list[JobDescription]:
        """Scrape multiple URLs with bounded concurrency."""
        sem = asyncio.Semaphore(concurrency)

        async def _bounded(url: str) -> JobDescription:
            async with sem:
                return await self.scrape(url)

        return await asyncio.gather(*[_bounded(u) for u in urls])

    # -- Private: navigation ----------------------------------------------

    async def _new_page(self) -> Page:
        ctx = await self._browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/125.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 900},
            java_script_enabled=True,
        )
        page = await ctx.new_page()
        # Block heavy resources to speed up loading
        await page.route(
            re.compile(r"\.(png|jpg|jpeg|gif|svg|woff2?|ttf|eot|ico|mp4|webm)$", re.I),
            lambda route: route.abort(),
        )
        return page

    async def _navigate(self, page: Page, url: str, jd: JobDescription):
        """Navigate to URL, handling dynamic content loading."""
        profile = self._detect_ats(url)
        wait_selector = profile.get("wait_selector") if profile else None
        extra_wait = profile.get("extra_wait_ms", 0) if profile else 0

        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=self.timeout_ms)
        except PlaywrightTimeout:
            # Retry with longer timeout and networkidle
            jd.scraper_notes.append("First load timed out, retrying with networkidle")
            await page.goto(url, wait_until="networkidle", timeout=self.timeout_ms * 2)

        # Wait for ATS-specific content element
        if wait_selector:
            try:
                await page.wait_for_selector(wait_selector, timeout=10_000)
            except PlaywrightTimeout:
                jd.scraper_notes.append(f"ATS wait selector '{wait_selector}' not found; continuing")

        # Some ATS platforms need extra time for JS rendering
        if extra_wait:
            await asyncio.sleep(extra_wait / 1000)

        # Dismiss common overlays/modals
        await self._dismiss_overlays(page)

        # Scroll to trigger lazy-loaded content
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await asyncio.sleep(0.5)

    async def _dismiss_overlays(self, page: Page):
        """Click away cookie banners and modals that obscure content."""
        dismiss_selectors = [
            'button[id*="cookie" i]',
            'button[class*="cookie" i]',
            'button[id*="accept" i]',
            'button[class*="consent" i]',
            'button[aria-label*="close" i]',
            'button[aria-label*="dismiss" i]',
            'button[class*="close-modal" i]',
            '[data-testid="close-button"]',
        ]
        for sel in dismiss_selectors:
            try:
                btn = page.locator(sel).first
                if await btn.is_visible(timeout=500):
                    await btn.click(timeout=1000)
                    await asyncio.sleep(0.3)
            except Exception:
                continue

    # -- Private: ATS detection -------------------------------------------

    def _detect_ats(self, url: str) -> Optional[dict]:
        """Match URL to a known ATS profile."""
        parsed = urlparse(url)
        host = parsed.hostname or ""

        for name, profile in ATS_PROFILES.items():
            # Check explicit host list
            if any(h in host for h in profile.get("hosts", [])):
                return {**profile, "_name": name}
            # Check regex pattern
            pattern = profile.get("host_pattern")
            if pattern and re.match(pattern, host):
                return {**profile, "_name": name}

        return None

    # -- Private: metadata extraction -------------------------------------

    def _extract_metadata(self, soup: BeautifulSoup, profile: Optional[dict], jd: JobDescription):
        """Extract job title, company, location from known selectors or heuristics."""

        def _first_text(selector: str) -> str:
            if not selector:
                return ""
            for sel in selector.split(","):
                el = soup.select_one(sel.strip())
                if el:
                    text = el.get_text(strip=True)
                    if text:
                        return text
                    # For img alt text (e.g. Lever company logo)
                    if el.name == "img" and el.get("alt"):
                        return el["alt"]
            return ""

        if profile:
            jd.job_title = jd.job_title or _first_text(profile.get("title_selector", ""))
            jd.company_name = jd.company_name or _first_text(profile.get("company_selector", ""))
            jd.location = jd.location or _first_text(profile.get("location_selector", ""))

        # Generic fallbacks
        if not jd.job_title:
            # Try og:title, then <title>, then first <h1>
            og = soup.find("meta", property="og:title")
            if og and og.get("content"):
                jd.job_title = og["content"].split("|")[0].split("–")[0].split("-")[0].strip()
            elif soup.title and soup.title.string:
                jd.job_title = soup.title.string.split("|")[0].split("–")[0].split("-")[0].strip()
            else:
                h1 = soup.find("h1")
                if h1:
                    jd.job_title = h1.get_text(strip=True)

        if not jd.company_name:
            og = soup.find("meta", property="og:site_name")
            if og and og.get("content"):
                jd.company_name = og["content"]

        # Try to extract salary from common patterns in the page text
        if not jd.salary_range:
            text = soup.get_text(" ", strip=True)
            salary_match = re.search(
                r"\$[\d,]+(?:\.\d{2})?\s*[-–—to]+\s*\$[\d,]+(?:\.\d{2})?(?:\s*(?:per\s+)?(?:year|yr|annually|hour|hr))?",
                text,
                re.IGNORECASE,
            )
            if salary_match:
                jd.salary_range = salary_match.group(0).strip()

    # -- Private: content extraction --------------------------------------

    def _find_content_container(self, soup: BeautifulSoup, profile: Optional[dict]) -> Optional[Tag]:
        """Find the best DOM element containing the job description."""

        # 1. Try ATS-specific selectors
        if profile:
            selector = profile.get("content_selector", "")
            for sel in selector.split(","):
                el = soup.select_one(sel.strip())
                if el and len(el.get_text(strip=True)) > 100:
                    return el

        # 2. Try generic selectors
        for sel in GENERIC_CONTENT_SELECTORS:
            el = soup.select_one(sel)
            if el and len(el.get_text(strip=True)) > 200:
                return el

        # 3. Heuristic: find the div with the most text that contains
        #    job-related keywords
        job_keywords = re.compile(
            r"(?i)(responsibilit|qualificat|requirement|experience|skill|"
            r"you\s+will|what\s+you|about\s+the\s+role|the\s+role|"
            r"minimum\s+qualif|preferred\s+qualif|nice\s+to\s+have|"
            r"must\s+have|years?\s+of\s+experience)"
        )
        best_el = None
        best_score = 0

        for div in soup.find_all(["div", "section", "article"]):
            text = div.get_text(" ", strip=True)
            text_len = len(text)
            if text_len < 200:
                continue

            # Score: text length + keyword bonus
            keyword_hits = len(job_keywords.findall(text))
            # Penalize overly large containers (likely <body> wrappers)
            if text_len > 20_000:
                continue
            score = text_len + (keyword_hits * 500)

            if score > best_score:
                best_score = score
                best_el = div

        return best_el

    # -- Private: markdown cleanup ----------------------------------------

    def _clean_markdown(self, raw_md: str) -> str:
        """Clean up extracted markdown into a focused job description."""

        # Normalize whitespace
        lines = raw_md.split("\n")
        cleaned = []
        prev_blank = False

        for line in lines:
            stripped = line.rstrip()

            # Collapse multiple blank lines
            if not stripped:
                if not prev_blank:
                    cleaned.append("")
                prev_blank = True
                continue
            prev_blank = False

            # Skip image/link-only lines
            if re.match(r"^\s*!\[.*\]\(.*\)\s*$", stripped):
                continue

            # Skip very short non-heading lines (nav remnants)
            if len(stripped) < 4 and not stripped.startswith("#"):
                continue

            # Skip common UI text
            lower = stripped.lower().strip()
            if lower in {
                "apply now", "apply for this job", "share", "save job",
                "sign in", "log in", "create account", "back to jobs",
                "share this job", "print", "email", "copy link",
            }:
                continue

            cleaned.append(stripped)

        text = "\n".join(cleaned).strip()

        # Trim noise sections at the end (benefits, EEO, etc.)
        if self.trim_noise:
            text = self._trim_noise_sections(text)

        # Final cleanup of excessive blank lines
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text

    def _trim_noise_sections(self, text: str) -> str:
        """
        Remove trailing sections that are typically boilerplate
        (EEO, benefits, company culture, etc.) while keeping
        the core JD content intact.
        """
        lines = text.split("\n")
        cut_index = len(lines)

        # Walk backwards to find the last noise section header
        # and cut everything from the first noise header onward
        first_noise_idx = None
        for i, line in enumerate(lines):
            if NOISE_SECTION_PATTERNS.match(line.strip()):
                if first_noise_idx is None:
                    first_noise_idx = i
            else:
                # If we see a non-noise heading after noise, it might be
                # interleaved — only cut if noise continues to the end
                if first_noise_idx is not None and line.strip().startswith("#"):
                    # Check if this heading is substantive JD content
                    if re.search(
                        r"(?i)(responsibilit|qualificat|requirement|skill|"
                        r"what\s+you|about\s+the\s+role|the\s+role|"
                        r"key\s+duties|experience)",
                        line,
                    ):
                        first_noise_idx = None  # Reset — this is real content

        if first_noise_idx is not None:
            cut_index = first_noise_idx

        result = "\n".join(lines[:cut_index]).strip()

        # Safety: don't trim more than 60% of content
        if len(result) < len(text) * 0.4:
            return text

        return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

async def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: python scraper.py <url> [url2 ...] [--json] [--resume]")
        print()
        print("Options:")
        print("  --json     Output raw JSON")
        print("  --resume   Output formatted for resume tailoring")
        print("  --full     Don't trim boilerplate sections")
        print()
        print("Examples:")
        print("  python scraper.py https://boards.greenhouse.io/company/jobs/123456")
        print("  python scraper.py https://jobs.lever.co/company/abc-def --resume")
        print("  python scraper.py url1 url2 url3 --json")
        return

    urls = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
    output_json = "--json" in sys.argv
    output_resume = "--resume" in sys.argv
    trim_noise = "--full" not in sys.argv

    async with JobScraper(trim_noise_sections=trim_noise) as scraper:
        results = await scraper.scrape_many(urls)

        for jd in results:
            if output_json:
                print(json.dumps(jd.to_dict(), indent=2))
            elif output_resume:
                print(jd.to_resume_prompt())
            else:
                print(f"\n{'='*80}")
                print(f"URL:     {jd.url}")
                print(f"Title:   {jd.job_title}")
                print(f"Company: {jd.company_name}")
                print(f"Location:{jd.location}")
                if jd.salary_range:
                    print(f"Salary:  {jd.salary_range}")
                print(f"Success: {jd.success}")
                if jd.scraper_notes:
                    print(f"Notes:   {', '.join(jd.scraper_notes)}")
                if jd.error:
                    print(f"Error:   {jd.error}")
                print(f"{'='*80}")
                print(jd.description[:3000] if jd.description else "[No content extracted]")
                print(f"{'='*80}\n")


if __name__ == "__main__":
    asyncio.run(main())