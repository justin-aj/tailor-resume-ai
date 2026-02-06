import asyncio
from scraper import AsyncWebCrawler, CrawlerRunConfig

async def test_cloudflare():
    url = 'https://job-boards.greenhouse.io/cloudflare/jobs/7589903'
    
    async with AsyncWebCrawler(verbose=True) as crawler:
        # Test with minimal filtering
        config = CrawlerRunConfig(
            excluded_tags=['script', 'style'],
            remove_overlay_elements=True,
            word_count_threshold=5
        )
        result = await crawler.arun(url, config=config)
        
        print(f"\n{'='*80}")
        print(f"Raw markdown length: {len(result.markdown)} chars")
        print(f"{'='*80}")
        print("\nFirst 2000 characters:")
        print(result.markdown[:2000])
        print(f"\n{'='*80}")

asyncio.run(test_cloudflare())
