import asyncio
from scraper import AsyncWebCrawler, CrawlerRunConfig

async def test_oracle():
    url = 'https://ectf.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/437'
    
    async with AsyncWebCrawler(verbose=True) as crawler:
        # Try with JavaScript execution and longer wait
        config = CrawlerRunConfig(
            excluded_tags=['script', 'style'],
            remove_overlay_elements=True,
            word_count_threshold=5,
            wait_until="networkidle",  # Wait for page to fully load
            page_timeout=60000  # 60 seconds
        )
        result = await crawler.arun(url, config=config)
        
        print(f"\n{'='*80}")
        print(f"Success: {result.success}")
        print(f"Raw markdown length: {len(result.markdown)} chars")
        print(f"{'='*80}")
        print("\nContent preview (first 3000 characters):")
        print(result.markdown[:3000])
        print(f"\n{'='*80}")

asyncio.run(test_oracle())
