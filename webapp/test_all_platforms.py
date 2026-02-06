"""
Comprehensive test: Verify scraper works on all job board platforms
"""
import asyncio
from scraper import JobDescriptionScraper

async def test_all_platforms():
    scraper = JobDescriptionScraper()
    
    test_urls = [
        ("Greenhouse (GoFundMe)", "https://job-boards.greenhouse.io/gofundme/jobs/7296482"),
        ("Greenhouse (Cloudflare)", "https://job-boards.greenhouse.io/cloudflare/jobs/7589903"),
        ("Oracle Cloud (Wave Life)", "https://ectf.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/437"),
        ("Boehringer-Ingelheim", "https://jobs.boehringer-ingelheim.com/job/Ridgefield,-CT-Data-Science-Internship-Unit/1244347301/")
    ]
    
    print("="*80)
    print("🧪 COMPREHENSIVE SCRAPER TEST")
    print("="*80)
    
    results = []
    
    for platform_name, url in test_urls:
        print(f"\n📝 Testing: {platform_name}")
        print(f"   URL: {url}")
        
        result = await scraper.scrape_job_url(url, use_llm=False)
        
        if result.get("success", True):
            formatted = scraper.format_for_resume_tailoring(result)
            
            # Check if navigation menu patterns are present
            nav_patterns = [
                'skip to main content',
                'employee login',
                'language selector',
                'view profile',
                'explore our company',
                'deutsch (deutschland)',
                'français (france)'
            ]
            
            nav_found = sum(1 for pattern in nav_patterns if pattern in formatted.lower())
            
            # Check if job content is present
            job_patterns = [
                'responsibilities',
                'qualifications',
                'requirements',
                'description'
            ]
            
            job_content_found = sum(1 for pattern in job_patterns if pattern in formatted.lower())
            
            has_navigation = nav_found > 2
            has_job_content = job_content_found >= 2
            
            results.append({
                'platform': platform_name,
                'success': True,
                'length': len(formatted),
                'has_navigation': has_navigation,
                'has_job_content': has_job_content,
                'nav_count': nav_found,
                'job_count': job_content_found
            })
            
            status = "✅ PASS" if (not has_navigation and has_job_content) else "❌ FAIL"
            print(f"   {status}")
            print(f"   - Content length: {len(formatted)} chars")
            print(f"   - Navigation elements: {nav_found}")
            print(f"   - Job content sections: {job_content_found}")
            
        else:
            results.append({
                'platform': platform_name,
                'success': False,
                'error': result.get('error')
            })
            print(f"   ❌ FAIL: {result.get('error')}")
    
    print("\n" + "="*80)
    print("📊 FINAL RESULTS")
    print("="*80)
    
    all_passed = all(
        r['success'] and not r.get('has_navigation', True) and r.get('has_job_content', False)
        for r in results
    )
    
    for r in results:
        if r['success']:
            status = "✅" if (not r.get('has_navigation') and r.get('has_job_content')) else "❌"
            print(f"{status} {r['platform']:25s} - {r['length']:5d} chars, Nav: {r['nav_count']}, Job: {r['job_count']}")
        else:
            print(f"❌ {r['platform']:25s} - ERROR: {r.get('error')}")
    
    print("\n" + "="*80)
    if all_passed:
        print("🎉 ALL TESTS PASSED! Scraper works perfectly across all platforms!")
    else:
        print("⚠️  Some tests failed. Review results above.")
    print("="*80)

if __name__ == "__main__":
    asyncio.run(test_all_platforms())
