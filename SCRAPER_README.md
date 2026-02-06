# Crawl4AI Scraper for Tailor Resume AI

This module adds web scraping capabilities to the Tailor Resume AI project using [Crawl4AI](https://github.com/unclecode/crawl4ai), allowing you to automatically extract job descriptions from URLs.

## 🚀 Features

- **Job Description Scraping**: Extract job postings from any career website
- **Smart Extraction**: Two modes - simple markdown or LLM-powered structured extraction
- **Batch Processing**: Scrape multiple URLs concurrently
- **Resume Integration**: Formatted output ready for resume tailoring
- **Universal Scraping**: Works with LinkedIn, Indeed, GitHub Jobs, and more

## 📦 Installation

### 1. Install Dependencies

```bash
cd webapp
pip install -r scraper_requirements.txt
```

### 2. Setup Playwright Browsers

```bash
# Install Chromium browser for scraping
crawl4ai-setup

# Or manually
python -m playwright install --with-deps chromium

# Verify installation
crawl4ai-doctor
```

## 🎯 Quick Start

### Basic Usage

```python
import asyncio
from scraper import scrape_job_description

async def main():
    url = "https://www.linkedin.com/jobs/view/1234567890"
    result = await scrape_job_description(url)
    
    print(f"Job Title: {result['title']}")
    print(f"Description: {result['description'][:200]}...")

asyncio.run(main())
```

### Command Line

```bash
# Scrape a job posting
python scraper.py https://www.linkedin.com/jobs/view/1234567890

# Use LLM extraction (requires API key)
python scraper.py https://www.linkedin.com/jobs/view/1234567890 --llm
```

## 🔧 Usage Examples

### Example 1: Simple Job Scraping

```python
from scraper import JobDescriptionScraper
import asyncio

async def scrape_job():
    scraper = JobDescriptionScraper()
    
    url = "https://www.indeed.com/viewjob?jk=abc123"
    result = await scraper.scrape_job_url(url, use_llm=False)
    
    if result.get("success", True):
        formatted = scraper.format_for_resume_tailoring(result)
        print(formatted)

asyncio.run(scrape_job())
```

### Example 2: LLM-Powered Extraction

For more accurate structured extraction (requires OpenAI API key or Ollama):

```python
from scraper import JobDescriptionScraper
import asyncio
import os

# Set API key
os.environ['OPENAI_API_KEY'] = 'your-api-key'

async def scrape_with_llm():
    scraper = JobDescriptionScraper()
    result = await scraper.scrape_job_url(url, use_llm=True)
    
    print(f"Job Title: {result['job_title']}")
    print(f"Company: {result['company_name']}")
    print(f"Skills: {', '.join(result['required_skills'])}")

asyncio.run(scrape_with_llm())
```

### Example 3: Batch Scraping

```python
from scraper import JobDescriptionScraper
import asyncio

async def scrape_multiple():
    scraper = JobDescriptionScraper()
    
    urls = [
        "https://www.linkedin.com/jobs/view/1234567890",
        "https://www.indeed.com/viewjob?jk=abc123",
        "https://jobs.github.com/positions/xyz789"
    ]
    
    results = await scraper.scrape_multiple_urls(urls)
    
    for i, result in enumerate(results, 1):
        if result.get("success", True):
            print(f"\nJob {i}: {result.get('title', 'N/A')}")

asyncio.run(scrape_multiple())
```

### Example 4: General Web Scraping

```python
from scraper import SimpleScraper
import asyncio

async def scrape_any_page():
    scraper = SimpleScraper()
    result = await scraper.scrape_url("https://docs.python.org")
    
    print(f"Title: {result['title']}")
    print(f"Content: {result['markdown'][:500]}")

asyncio.run(scrape_any_page())
```

## 🔌 Flask Integration

Add this to your `webapp/api/index.py`:

```python
from scraper import JobDescriptionScraper
import asyncio

@app.route('/scrape-job', methods=['POST'])
def scrape_job():
    """API endpoint to scrape job descriptions from URLs"""
    data = request.json
    url = data.get('url', '')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        # Run async scraper
        scraper = JobDescriptionScraper()
        result = asyncio.run(scraper.scrape_job_url(url, use_llm=False))
        
        if result.get('success', True):
            formatted = scraper.format_for_resume_tailoring(result)
            return jsonify({
                'success': True,
                'job_description': formatted,
                'title': result.get('title', ''),
                'url': url
            })
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'Unknown error')
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
```

### Frontend Integration (templates/index.html)

```html
<!-- Add to your form -->
<div class="form-group">
    <label>🕷️ Or Scrape from Job URL:</label>
    <div style="display: flex; gap: 10px;">
        <input type="url" id="jobUrl" class="form-control" 
               placeholder="https://example.com/job-posting">
        <button type="button" class="btn btn-secondary" onclick="scrapeJobUrl()">
            Scrape
        </button>
    </div>
</div>

<script>
async function scrapeJobUrl() {
    const url = document.getElementById('jobUrl').value;
    
    if (!url) {
        alert('Please enter a job URL');
        return;
    }
    
    // Show loading state
    const button = event.target;
    button.textContent = '⏳ Scraping...';
    button.disabled = true;
    
    try {
        const response = await fetch('/scrape-job', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({url: url})
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Fill the job description textarea
            document.getElementById('job_description').value = data.job_description;
            alert('✅ Job description scraped successfully!');
        } else {
            alert('❌ Error: ' + data.error);
        }
    } catch (error) {
        alert('❌ Error: ' + error.message);
    } finally {
        button.textContent = 'Scrape';
        button.disabled = false;
    }
}
</script>
```

## 🔑 LLM Configuration

### Option 1: OpenAI (Recommended)

```bash
# Set environment variable
export OPENAI_API_KEY="your-api-key-here"

# Or in Python
import os
os.environ['OPENAI_API_KEY'] = 'your-api-key'
```

### Option 2: Ollama (Free, Local)

1. Install Ollama: https://ollama.ai
2. Pull a model: `ollama pull llama3.2`
3. Update scraper.py:

```python
extraction_strategy = LLMExtractionStrategy(
    provider="ollama/llama3.2",  # Use local model
    schema=self.extraction_schema,
    instruction="Extract job posting details"
)
```

## 📊 Scraper Classes

### JobDescriptionScraper

Specialized for job postings with structured extraction.

**Methods:**
- `scrape_job_url(url, use_llm)` - Scrape single job URL
- `scrape_multiple_urls(urls, use_llm)` - Batch scrape jobs
- `format_for_resume_tailoring(data)` - Format for resume use

### SimpleScraper

General-purpose web scraper for any content.

**Methods:**
- `scrape_url(url, only_text)` - Scrape any webpage

## 🎨 Extracted Data Schema

When using LLM extraction, you get structured data:

```json
{
    "job_title": "Senior Python Developer",
    "company_name": "Tech Corp",
    "location": "Remote",
    "job_type": "Full-time",
    "required_skills": ["Python", "Django", "PostgreSQL"],
    "preferred_skills": ["Docker", "AWS", "React"],
    "responsibilities": [
        "Develop backend APIs",
        "Mentor junior developers"
    ],
    "requirements": [
        "5+ years Python experience",
        "BS in Computer Science"
    ],
    "benefits": ["Health insurance", "401k"],
    "salary_range": "$120k - $150k",
    "description": "Full job description text..."
}
```

## 🧪 Testing

Run the examples:

```bash
python scraper_example.py
```

This will demonstrate:
1. Basic scraping
2. LLM extraction
3. Multiple URLs
4. Formatting for resume tailoring
5. General webpage scraping
6. Flask integration patterns

## 🛠️ Troubleshooting

### Browser Installation Issues

```bash
# Reinstall browsers
python -m playwright install --with-deps chromium

# Verify
crawl4ai-doctor
```

### Rate Limiting

If you encounter rate limiting, add delays:

```python
import asyncio

async def scrape_with_delay(urls):
    results = []
    for url in urls:
        result = await scraper.scrape_job_url(url)
        results.append(result)
        await asyncio.sleep(2)  # 2 second delay
    return results
```

### API Key Errors

For LLM extraction without API key:

```python
# Use Ollama instead (free, local)
extraction_strategy = LLMExtractionStrategy(
    provider="ollama/llama3.2",
    schema=schema
)
```

## 📚 Additional Resources

- [Crawl4AI Documentation](https://docs.crawl4ai.com/)
- [Crawl4AI GitHub](https://github.com/unclecode/crawl4ai)
- [Example Notebooks](https://colab.research.google.com/drive/1SgRPrByQLzjRfwoRNq1wSGE9nYY_EE8C)

## 🎯 Common Use Cases

1. **Auto-fill Job Description**: Scrape job URLs and populate the textarea
2. **Batch Analysis**: Scrape multiple jobs to analyze trends
3. **Resume Matching**: Extract requirements and match with resume
4. **Competitive Analysis**: Track job postings from competitors
5. **Skill Extraction**: Identify trending skills from multiple postings

## 💡 Tips

- Use simple mode first (faster, no API key needed)
- Enable LLM mode for structured data extraction
- Cache results to avoid re-scraping
- Respect robots.txt and rate limits
- Add error handling for failed scrapes
- Use batch scraping for efficiency

## 🔐 Security Notes

- Never commit API keys to version control
- Use environment variables for credentials
- Validate and sanitize scraped content
- Be aware of website terms of service
- Respect rate limits and robots.txt

---

Made with ❤️ using [Crawl4AI](https://github.com/unclecode/crawl4ai)
