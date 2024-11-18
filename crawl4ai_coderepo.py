
# Bringing together code chunks from Crawl4ai to piece together


#############################################################

# Advanced Session-Based Crawling with Dynamic Content 🔄

import os, sys
# append parent directory to system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))); os.environ['FIRECRAWL_API_KEY'] = "fc-84b370ccfad44beabc686b38f1769692";

import asyncio
# import nest_asyncio
# nest_asyncio.apply()

import time
import json
import os
import re
from typing import Dict, List
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import (
    JsonCssExtractionStrategy,
    LLMExtractionStrategy,
)


async def crawl_dynamic_content_pages_method_1():
    print("\n--- Advanced Multi-Page Crawling with JavaScript Execution ---")
    first_commit = ""

    async def on_execution_started(page):
        nonlocal first_commit
        try:
            while True:
                await page.wait_for_selector("li.Box-sc-g0xbh4-0 h4")
                commit = await page.query_selector("li.Box-sc-g0xbh4-0 h4")
                commit = await commit.evaluate("(element) => element.textContent")
                commit = re.sub(r"\s+", "", commit)
                if commit and commit != first_commit:
                    first_commit = commit
                    break
                await asyncio.sleep(0.5)
        except Exception as e:
            print(f"Warning: New content didn't appear after JavaScript execution: {e}")

    async with AsyncWebCrawler(verbose=True) as crawler:
        crawler.crawler_strategy.set_hook("on_execution_started", on_execution_started)

        url = "https://github.com/microsoft/TypeScript/commits/main"
        session_id = "typescript_commits_session"
        all_commits = []

        js_next_page = """
        const button = document.querySelector('a[data-testid="pagination-next-button"]');
        if (button) button.click();
        """

        for page in range(3):  # Crawl 3 pages
            result = await crawler.arun(
                url=url,
                session_id=session_id,
                css_selector="li.Box-sc-g0xbh4-0",
                js=js_next_page if page > 0 else None,
                bypass_cache=True,
                js_only=page > 0,
                headless=False,
            )

            assert result.success, f"Failed to crawl page {page + 1}"

            soup = BeautifulSoup(result.cleaned_html, "html.parser")
            commits = soup.select("li")
            all_commits.extend(commits)

            print(f"Page {page + 1}: Found {len(commits)} commits")

        await crawler.crawler_strategy.kill_session(session_id)
        print(f"Successfully crawled {len(all_commits)} commits across 3 pages")


#####

async def crawl_dynamic_content_pages_method_2():
    print("\n--- Advanced Multi-Page Crawling with JavaScript Execution ---")

    async with AsyncWebCrawler(verbose=True) as crawler:
        url = "https://github.com/microsoft/TypeScript/commits/main"
        session_id = "typescript_commits_session"
        all_commits = []
        last_commit = ""

        js_next_page_and_wait = """
        (async () => {
            const getCurrentCommit = () => {
                const commits = document.querySelectorAll('li.Box-sc-g0xbh4-0 h4');
                return commits.length > 0 ? commits[0].textContent.trim() : null;
            };

            const initialCommit = getCurrentCommit();
            const button = document.querySelector('a[data-testid="pagination-next-button"]');
            if (button) button.click();

            // Poll for changes
            while (true) {
                await new Promise(resolve => setTimeout(resolve, 100)); // Wait 100ms
                const newCommit = getCurrentCommit();
                if (newCommit && newCommit !== initialCommit) {
                    break;
                }
            }
        })();
        """

        schema = {
            "name": "Commit Extractor",
            "baseSelector": "li.Box-sc-g0xbh4-0",
            "fields": [
                {
                    "name": "title",
                    "selector": "h4.markdown-title",
                    "type": "text",
                    "transform": "strip",
                },
            ],
        }
        extraction_strategy = JsonCssExtractionStrategy(schema, verbose=True)

        for page in range(3):  # Crawl 3 pages
            result = await crawler.arun(
                url=url,
                session_id=session_id,
                css_selector="li.Box-sc-g0xbh4-0",
                extraction_strategy=extraction_strategy,
                js_code=js_next_page_and_wait if page > 0 else None,
                js_only=page > 0,
                bypass_cache=True,
                headless=False,
            )

            assert result.success, f"Failed to crawl page {page + 1}"

            commits = json.loads(result.extracted_content)
            all_commits.extend(commits)

            print(f"Page {page + 1}: Found {len(commits)} commits")

        await crawler.crawler_strategy.kill_session(session_id)
        print(f"Successfully crawled {len(all_commits)} commits across 3 pages")

async def crawl_dynamic_content_pages_method_3():
    print("\n--- Advanced Multi-Page Crawling with JavaScript Execution using `wait_for` ---")

    async with AsyncWebCrawler(verbose=True) as crawler:
        url = "https://github.com/microsoft/TypeScript/commits/main"
        session_id = "typescript_commits_session"
        all_commits = []

        js_next_page = """
        const commits = document.querySelectorAll('li.Box-sc-g0xbh4-0 h4');
        if (commits.length > 0) {
            window.firstCommit = commits[0].textContent.trim();
        }
        const button = document.querySelector('a[data-testid="pagination-next-button"]');
        if (button) button.click();
        """

        wait_for = """() => {
            const commits = document.querySelectorAll('li.Box-sc-g0xbh4-0 h4');
            if (commits.length === 0) return false;
            const firstCommit = commits[0].textContent.trim();
            return firstCommit !== window.firstCommit;
        }"""
        
        schema = {
            "name": "Commit Extractor",
            "baseSelector": "li.Box-sc-g0xbh4-0",
            "fields": [
                {
                    "name": "title",
                    "selector": "h4.markdown-title",
                    "type": "text",
                    "transform": "strip",
                },
            ],
        }
        extraction_strategy = JsonCssExtractionStrategy(schema, verbose=True)

        for page in range(3):  # Crawl 3 pages
            result = await crawler.arun(
                url=url,
                session_id=session_id,
                css_selector="li.Box-sc-g0xbh4-0",
                extraction_strategy=extraction_strategy,
                js_code=js_next_page if page > 0 else None,
                wait_for=wait_for if page > 0 else None,
                js_only=page > 0,
                bypass_cache=True,
                headless=False,
            )

            assert result.success, f"Failed to crawl page {page + 1}"

            commits = json.loads(result.extracted_content)
            all_commits.extend(commits)

            print(f"Page {page + 1}: Found {len(commits)} commits")

        await crawler.crawler_strategy.kill_session(session_id)
        print(f"Successfully crawled {len(all_commits)} commits across 3 pages")



#############################################################

# Dynamic Content Handling


# import asyncio
# from crawl4ai import AsyncWebCrawler

# async def crawl_dynamic_content():
#     # You can use wait_for to wait for a condition to be met before returning the result
#     # wait_for = """() => {
#     #     return Array.from(document.querySelectorAll('article.tease-card')).length > 10;
#     # }"""

#     # wait_for can be also just a css selector
#     # wait_for = "article.tease-card:nth-child(10)"

#     async with AsyncWebCrawler(verbose=True) as crawler:
#         js_code = [
#             "const loadMoreButton = Array.from(document.querySelectorAll('button')).find(button => button.textContent.includes('Load More')); loadMoreButton && loadMoreButton.click();"
#         ]
#         result = await crawler.arun(
#             url="https://www.nbcnews.com/business",
#             js_code=js_code,
#             # wait_for=wait_for,
#             bypass_cache=True,
#         )
#         print(result.markdown[:500])  # Print first 500 characters

# asyncio.run(crawl_dynamic_content())


# # Another example

# import asyncio
# from crawl4ai import AsyncWebCrawler

# async def main():
#     async with AsyncWebCrawler(verbose=True) as crawler:
#         js_code = ["const loadMoreButton = Array.from(document.querySelectorAll('button')).find(button => button.textContent.includes('Load More')); loadMoreButton && loadMoreButton.click();"]
#         result = await crawler.arun(
#             url="https://www.nbcnews.com/business",
#             js_code=js_code,
#             css_selector=".wide-tease-item__description",
#             bypass_cache=True
#         )
#         print(result.extracted_content)

# if __name__ == "__main__":
#     asyncio.run(main())


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