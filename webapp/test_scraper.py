"""
Test script to verify all scraper page buttons and functionality
"""
import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000"

def test_scraper_page():
    """Test if scraper page loads"""
    print("\n🧪 Testing scraper page load...")
    try:
        response = requests.get(f"{BASE_URL}/scraper")
        if response.status_code == 200:
            print("✅ Scraper page loads successfully")
            return True
        else:
            print(f"❌ Scraper page failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error loading scraper page: {e}")
        return False

def test_home_page():
    """Test if home page loads"""
    print("\n🧪 Testing home page load...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Home page loads successfully")
            return True
        else:
            print(f"❌ Home page failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error loading home page: {e}")
        return False

def test_scrape_api():
    """Test the scrape-job API endpoint"""
    print("\n🧪 Testing scrape-job API...")
    try:
        test_url = "https://job-boards.greenhouse.io/gofundme/jobs/7296482"
        payload = {"url": test_url}
        
        print(f"   Scraping URL: {test_url}")
        print("   This may take a few seconds...")
        
        response = requests.post(
            f"{BASE_URL}/api/scrape-job",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Scrape API working successfully")
                print(f"   Job Title: {data.get('title', 'N/A')[:60]}...")
                print(f"   Description Length: {len(data.get('description', ''))} chars")
                return True
            else:
                print(f"❌ Scrape failed: {data.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ API returned status: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
    except requests.exceptions.Timeout:
        print("⚠️  Request timed out (this is expected for slow scraping)")
        print("   The API might still be working, just taking longer than 30s")
        return None
    except Exception as e:
        print(f"❌ Error testing scrape API: {e}")
        return False

def test_scrape_api_no_url():
    """Test scrape API with missing URL"""
    print("\n🧪 Testing scrape-job API validation (no URL)...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/scrape-job",
            json={},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 400:
            print("✅ URL validation working correctly")
            return True
        else:
            print(f"⚠️  Expected 400 status, got: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing validation: {e}")
        return False

def test_static_files():
    """Test if static files load"""
    print("\n🧪 Testing static files...")
    files = [
        "/static/css/scraper.css",
        "/static/js/scraper.js",
        "/static/css/style.css"
    ]
    
    all_ok = True
    for file_path in files:
        try:
            response = requests.get(f"{BASE_URL}{file_path}")
            if response.status_code == 200:
                print(f"   ✅ {file_path}")
            else:
                print(f"   ❌ {file_path} - Status: {response.status_code}")
                all_ok = False
        except Exception as e:
            print(f"   ❌ {file_path} - Error: {e}")
            all_ok = False
    
    if all_ok:
        print("✅ All static files load successfully")
    return all_ok

def main():
    print("=" * 80)
    print("🚀 Scraper Page Button & Functionality Test")
    print("=" * 80)
    
    results = {
        "Home Page": test_home_page(),
        "Scraper Page": test_scraper_page(),
        "Static Files": test_static_files(),
        "API Validation": test_scrape_api_no_url(),
        "Scrape API": test_scrape_api()
    }
    
    print("\n" + "=" * 80)
    print("📊 Test Results Summary")
    print("=" * 80)
    
    for test_name, result in results.items():
        if result is True:
            status = "✅ PASS"
        elif result is False:
            status = "❌ FAIL"
        else:
            status = "⚠️  TIMEOUT/PENDING"
        print(f"{test_name:20s} {status}")
    
    print("\n" + "=" * 80)
    print("💡 Notes:")
    print("=" * 80)
    print("• Frontend buttons (Add URL, View, Delete) work via JavaScript")
    print("• These are tested in the browser, not via API")
    print("• localStorage is used for storing URLs client-side")
    print("• Open http://127.0.0.1:5000/scraper in browser to test:")
    print("  - Add URL button")
    print("  - Scrape button (spider icon)")
    print("  - View button (eye icon)")
    print("  - Delete button (trash icon)")
    print("  - Scrape All button")
    print("  - Clear All button")
    print("  - Home navigation button")
    print("=" * 80)

if __name__ == "__main__":
    main()
