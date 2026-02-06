"""
Example usage of the Crawl4AI scraper for tailor-resume-ai project

This demonstrates how to:
1. Scrape job descriptions from URLs
2. Extract specific information
3. Use scraped data in resume tailoring
"""
import asyncio
from scraper import JobDescriptionScraper, SimpleScraper, scrape_job_description, scrape_webpage


async def example_1_basic_scraping():
    """Example 1: Basic job description scraping"""
    print("\n" + "="*80)
    print("Example 1: Basic Job Description Scraping (No LLM)")
    print("="*80)
    
    url = "https://www.linkedin.com/jobs/view/3825529843"  # Example LinkedIn job
    
    # Simple way - using convenience function
    result = await scrape_job_description(url, use_llm=False)
    
    if result.get("success", True):
        print(f"\n✅ Successfully scraped: {result.get('title', 'N/A')}")
        print(f"\nContent preview (first 300 chars):")
        print(result.get('description', '')[:300])
    else:
        print(f"\n❌ Error: {result.get('error')}")


async def example_2_structured_extraction():
    """Example 2: LLM-based structured extraction (requires API key)"""
    print("\n" + "="*80)
    print("Example 2: Structured Extraction with LLM")
    print("="*80)
    
    # Note: This requires setting up API key for OpenAI or using Ollama
    # Set environment variable: OPENAI_API_KEY or use Ollama locally
    
    url = "https://www.linkedin.com/jobs/view/3825529843"
    
    scraper = JobDescriptionScraper()
    
    # Uncomment below to test with LLM (requires API key setup)
    # result = await scraper.scrape_job_url(url, use_llm=True)
    # 
    # if result.get("success", True):
    #     print(f"\n✅ Job Title: {result.get('job_title', 'N/A')}")
    #     print(f"Company: {result.get('company_name', 'N/A')}")
    #     print(f"Required Skills: {', '.join(result.get('required_skills', []))}")
    # else:
    #     print(f"\n❌ Error: {result.get('error')}")
    
    print("\n⚠️  LLM extraction requires API key setup (OPENAI_API_KEY)")
    print("Alternatively, use Ollama locally with: provider='ollama/llama3.2'")


async def example_3_multiple_urls():
    """Example 3: Scrape multiple job URLs concurrently"""
    print("\n" + "="*80)
    print("Example 3: Scraping Multiple URLs Concurrently")
    print("="*80)
    
    urls = [
        "https://www.linkedin.com/jobs/view/3825529843",
        "https://www.indeed.com/viewjob?jk=example123",
        "https://jobs.github.com/positions/example456"
    ]
    
    scraper = JobDescriptionScraper()
    results = await scraper.scrape_multiple_urls(urls, use_llm=False)
    
    print(f"\n✅ Scraped {len(results)} URLs:")
    for i, result in enumerate(results, 1):
        status = "✓" if result.get("success", True) else "✗"
        title = result.get("title", "No title")
        print(f"  {status} Job {i}: {title[:60]}")


async def example_4_format_for_tailoring():
    """Example 4: Format scraped data for resume tailoring"""
    print("\n" + "="*80)
    print("Example 4: Format Job Data for Resume Tailoring")
    print("="*80)
    
    url = "https://www.linkedin.com/jobs/view/3825529843"
    
    scraper = JobDescriptionScraper()
    result = await scraper.scrape_job_url(url, use_llm=False)
    
    if result.get("success", True):
        formatted = scraper.format_for_resume_tailoring(result)
        print("\n✅ Formatted Job Description for Resume Tailoring:")
        print("-" * 80)
        print(formatted[:500])  # First 500 chars
        print("-" * 80)
        print("\nThis formatted text can be used as job description input")
        print("for the resume tailoring AI prompts.")


async def example_5_general_webpage():
    """Example 5: Scrape any webpage (not just jobs)"""
    print("\n" + "="*80)
    print("Example 5: General Webpage Scraping")
    print("="*80)
    
    url = "https://docs.crawl4ai.com/"
    
    result = await scrape_webpage(url)
    
    if result.get("success"):
        print(f"\n✅ Successfully scraped: {result.get('title', 'N/A')}")
        print(f"Found {result.get('media', 0)} images")
        print(f"Found {len(result.get('links', []))} internal links")
        print(f"\nContent preview (first 200 chars):")
        print(result.get('markdown', '')[:200])


async def example_6_integration_with_flask():
    """Example 6: How to integrate with Flask webapp"""
    print("\n" + "="*80)
    print("Example 6: Flask Integration Example")
    print("="*80)
    
    print("""
To integrate with your Flask app (api/index.py), add this route:

```python
from scraper import scrape_job_description
import asyncio

@app.route('/scrape-job', methods=['POST'])
def scrape_job():
    data = request.json
    url = data.get('url', '')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    # Run async scraper
    result = asyncio.run(scrape_job_description(url, use_llm=False))
    
    if result.get('success', True):
        # Format for job description textarea
        formatted = JobDescriptionScraper().format_for_resume_tailoring(result)
        return jsonify({
            'success': True,
            'job_description': formatted,
            'title': result.get('title', '')
        })
    else:
        return jsonify({
            'success': False,
            'error': result.get('error', 'Unknown error')
        }), 500
```

And add a button in your HTML template:
```html
<button onclick="scrapeJobUrl()">🕷️ Scrape from URL</button>
<input type="url" id="jobUrl" placeholder="https://example.com/job">

<script>
async function scrapeJobUrl() {
    const url = document.getElementById('jobUrl').value;
    const response = await fetch('/scrape-job', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({url: url})
    });
    const data = await response.json();
    if (data.success) {
        document.getElementById('job_description').value = data.job_description;
    }
}
</script>
```
    """)


async def main():
    """Run all examples"""
    print("\n🕷️  Crawl4AI Scraper Examples for Tailor Resume AI")
    print("=" * 80)
    
    # Run examples
    await example_1_basic_scraping()
    await example_2_structured_extraction()
    await example_3_multiple_urls()
    await example_4_format_for_tailoring()
    await example_5_general_webpage()
    await example_6_integration_with_flask()
    
    print("\n" + "="*80)
    print("✅ All examples completed!")
    print("="*80)


if __name__ == "__main__":
    asyncio.run(main())
