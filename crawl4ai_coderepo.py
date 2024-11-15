
# Bringing together code chunks from Crawl4ai to piece together
#############################################################

# https://crawl4ai.com/mkdocs/basic/quickstart/

import asyncio
from crawl4ai import AsyncWebCrawler



async def main():
    async with AsyncWebCrawler(verbose=True) as crawler:
        # We'll add our crawling code here
        pass

if __name__ == "__main__":
    asyncio.run(main())


# Desired url to scrape as a test:

test_url = https://www.breakthroughenergy.org/lookbook/


###############################################
# from crawl4ai GPT Assistant

import asyncio
from crawl4ai import AsyncWebCrawler

async def extract_company_names():
    # Define the URL
    url = "https://www.breakthroughenergy.org/our-work/breakthrough-energy-ventures/bev-portfolio/"
    
    # Use a CSS selector to target the elements containing company names
    css_selector = ".company-icon .name"  # Replace with the actual selector after inspecting the page structure

    async with AsyncWebCrawler(
        browser_type="chromium",  # Use Chromium browser
        headless=True,           # Headless mode for efficiency
        verbose=True             # Enable verbose logging
    ) as crawler:
        # Crawl the page
        result = await crawler.arun(
            url=url,
            css_selector=css_selector,    # Extract specific content using the selector
            magic=True,                   # Enable anti-detection features
            bypass_cache=True             # Always bypass cache to fetch fresh data
        )
        
        # Print the extracted content
        print(result.extracted_content)

# Run the asynchronous function
asyncio.run(extract_company_names())

#########################################

# https://crawl4ai.com/mkdocs/basic/page-interaction/

# Scroll and wait pattern
result = await crawler.arun(
    url="https://example.com",
    js_code=[
        # Scroll to bottom
        "window.scrollTo(0, document.body.scrollHeight);",
        # Click load more if exists
        "const loadMore = document.querySelector('.load-more'); if(loadMore) loadMore.click();"
    ],
    # Wait for new content
    wait_for="js:() => document.querySelectorAll('.item').length > previousCount"
)