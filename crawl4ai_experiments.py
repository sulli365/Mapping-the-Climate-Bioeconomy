
import asyncio
from crawl4ai import AsyncWebCrawler


async def extract_company_names():
    # Define the URL
    url = "https://www.breakthroughenergy.org/lookbook/"
    
    # Use a CSS selector to target the elements containing company names
    css_selector = "tr.logo-parent:nth-child(94) > th:nth-child(1) > span:nth-child(2)"  # Replace with the actual selector after inspecting the page structure

    async with AsyncWebCrawler(
        browser_type="chromium",  # Use Chromium browser
        headless=True,           # Headless mode for efficiency
        verbose=True             # Enable verbose logging
    ) as crawler:
        # Crawl the page
        result = await crawler.arun(
            url=url,
            # css_selector=css_selector,    # Extract specific content using the selector
            magic=True,                   # Enable anti-detection features
            bypass_cache=True     ,
        #     js_code=[
        #         # Scroll to bottom
        #         "window.scrollTo(0, document.body.scrollHeight);",
        #         # Click load more if exists
        #         "const loadMore = document.querySelector('.load-more'); if(loadMore) loadMore.click();"
        #     ],
        # # Wait for new content
        # wait_for="js:() => document.querySelectorAll('.item').length > previousCount"        # Always bypass cache to fetch fresh data
        )
        
        # Print the extracted content
        print(result.extracted_content)

# Run the asynchronous function
asyncio.run(extract_company_names())

