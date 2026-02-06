import asyncio
from scraper import AsyncWebCrawler, CrawlerRunConfig

async def test_boehringer():
    url = 'https://jobs.boehringer-ingelheim.com/job/Ridgefield%2C-CT-Data-Science-Internship-Unit/1244347301/'
    
    async with AsyncWebCrawler(verbose=True) as crawler:
        config = CrawlerRunConfig(
            excluded_tags=['script', 'style'],
            remove_overlay_elements=True,
            word_count_threshold=5,
            wait_until="networkidle",
            page_timeout=60000
        )
        result = await crawler.arun(url, config=config)
        
        print(f"\n{'='*80}")
        print(f"Success: {result.success}")
        print(f"Raw markdown length: {len(result.markdown)} chars")
        print(f"{'='*80}")
        
        # Search for job-related keywords in content
        keywords = ['responsibilities', 'qualifications', 'requirements', 'description', 'internship', 'data science']
        print("\nKeyword search:")
        for kw in keywords:
            count = result.markdown.lower().count(kw)
            print(f"  '{kw}': {count} occurrences")
        
        print(f"\n{'='*80}")
        print("\nSearching for job content:")
        idx = result.markdown.find('Data Science Internship')
        print(f"Job title found at character: {idx}")
        
        if idx > 0:
            print(f"\n{'='*80}")
            print("=== ACTUAL JOB CONTENT ===")
            print(result.markdown[idx:idx+4000])
        print(f"\n{'='*80}")

asyncio.run(test_boehringer())
