
import re
import asyncio
from crawl4ai import AsyncWebCrawler


async def crawl_with_load_more():
    url = "https://www.breakthroughenergy.org/lookbook/"
    
    async with AsyncWebCrawler(headless=True, verbose=True) as crawler:
        load_more_selector = ".load-more"  # Confirm this matches the correct CSS selector for the "Load More" button
        company_card_selector = ".company-card"  # Selector for loaded content (update as needed)

        print("Scrolling and attempting to load more content...")

        # Scroll to the bottom and click the "Load More" button
        result = await crawler.arun(
            url=url,
            js_code=[
                # Scroll to bottom
                "window.scrollTo(0, document.body.scrollHeight);",
                    # Click load more if exists
                "const loadMore = document.querySelector('.load-more'); if(loadMore) loadMore.click();"
            ],
            # Wait for new content
            wait_for="js:() => document.querySelectorAll('.item').length > previousCount"
        )
        #     bypass_cache=True,
        #     magic=True
        # )

        if not result.success:
            print(f"Error: {result.error_message}")


        # Pause briefly to ensure new content loads
        await asyncio.sleep(6)

            # # Check if the "Load More" button still exists
            # button_check_result = await crawler.arun(
            #     url=url,
            #     js_code=f"""
            #     const button = document.querySelector('{load_more_selector}');
            #     console.log('Load More button presence:', !!button);
            #     return !!button;
            #     """,
            #     magic=True
            # )

            # Log the state of the DOM for debugging
            # print(f"Load More button exists: {button_check_result.extracted_content.strip()}")

            # # Update the `has_more` flag
            # has_more = button_check_result.extracted_content.strip().lower() == "true"

        print("Finished loading all content. Now scraping the page...")

        # Finally scrape the full content
        final_result = await crawler.arun(
            url=url,
            bypass_cache=False,
            magic=True
        )

        if final_result.success:
            markdown_content = final_result.markdown

            # Refined regex to match only company names
            company_pattern = r"!\[.*?\]\(.*?\)\s(.*?)\s\|"

            matches = re.findall(company_pattern, markdown_content)

            # Clean up duplicates and unwanted entries
            company_names = [match.strip() for match in matches]

            print(f"Extracted Company Names: {company_names}")
        else:
            print(f"Failed to fetch content: {final_result.error_message}")

# Run the asynchronous function
asyncio.run(crawl_with_load_more())



# import re
# import asyncio
# from crawl4ai import AsyncWebCrawler


# async def crawl_with_load_more():
#     url = "https://www.breakthroughenergy.org/lookbook/"
    
#     async with AsyncWebCrawler(headless=True, verbose=True) as crawler:
#         load_more_selector = ".load-more"  # Confirm this matches the correct CSS selector for the "Load More" button
#         company_card_selector = ".company-card"  # Selector for loaded content (update as needed)
#         has_more = True

#         while has_more:
#             print("Scrolling and attempting to load more content...")

#             # Scroll to the bottom and click the "Load More" button
#             result = await crawler.arun(
#                 url=url,
#                 js_code=[
#                     "window.scrollTo(0, document.body.scrollHeight);",  # Scroll to the bottom
#                     f"""
#                     const loadMoreButton = document.querySelector('{load_more_selector}');
#                     if (loadMoreButton) {{
#                         console.log('Load More button clicked.');
#                         console.log('Load More button attributes:', loadMoreButton.outerHTML);
#                         loadMoreButton.click();
#                     }} else {{
#                         console.log('No more Load More button found.');
#                     }}
#                     """
#                 ],
#                 delay_before_return_html=4.0,  # Wait for new content to load
#                 bypass_cache=True,
#                 magic=True
#             )

#             if not result.success:
#                 print(f"Error: {result.error_message}")
#                 break

#             # Pause briefly to ensure new content loads
#             await asyncio.sleep(4)

#             # Check if the "Load More" button still exists
#             button_check_result = await crawler.arun(
#                 url=url,
#                 js_code=f"""
#                 const button = document.querySelector('{load_more_selector}');
#                 console.log('Load More button presence:', !!button);
#                 return !!button;
#                 """,
#                 magic=True
#             )

#             # Log the state of the DOM for debugging
#             print(f"Load More button exists: {button_check_result.extracted_content.strip()}")

#             # Update the `has_more` flag
#             has_more = button_check_result.extracted_content.strip().lower() == "true"

#         print("Finished loading all content. Now scraping the page...")

#         # Finally scrape the full content
#         final_result = await crawler.arun(
#             url=url,
#             bypass_cache=False,
#             magic=True
#         )

#         if final_result.success:
#             markdown_content = final_result.markdown

#             # Refined regex to match only company names
#             company_pattern = r"!\[.*?\]\(.*?\)\s(.*?)\s\|"

#             matches = re.findall(company_pattern, markdown_content)

#             # Clean up duplicates and unwanted entries
#             company_names = [match.strip() for match in matches]

#             print(f"Extracted Company Names: {company_names}")
#         else:
#             print(f"Failed to fetch content: {final_result.error_message}")

# # Run the asynchronous function
# asyncio.run(crawl_with_load_more())






#################################################################

# import re
# import asyncio
# from crawl4ai import AsyncWebCrawler


# async def crawl_with_load_more():
#     url = "https://www.breakthroughenergy.org/lookbook/"
    
#     async with AsyncWebCrawler(headless=True, verbose=True) as crawler:
#         load_more_selector = ".load-more"  # Replace with the actual CSS selector of the "Load More" button
#         has_more = True

#         while has_more:
#             print("Scrolling and attempting to load more content...")

#             # Click the "Load More" button and wait
#             result = await crawler.arun(
#                 url=url,
#                 js_code=[
#                     # Scroll to the bottom of the page
#                     "window.scrollTo(0, document.body.scrollHeight);",
#                     # Click the "Load More" button if it exists
#                     f"""
#                     const loadMoreButton = document.querySelector('{load_more_selector}');
#                     if (loadMoreButton) {{
#                         loadMoreButton.click();
#                     }} else {{
#                         console.log('No more Load More button found');
#                     }}
#                     """
#                 ],
#                 wait_for=f"js:() => !document.querySelector('{load_more_selector}') || document.readyState === 'complete'",
#                 delay_before_return_html=4.0,  # Give the page time to load more content
#                 bypass_cache=True,
#                 magic=True
#             )

#             if not result.success:
#                 print(f"Error: {result.error_message}")
#                 break

#             # Check if the "Load More" button is still present
#             has_more = f"document.querySelector('{load_more_selector}')" in result.markdown

#         print("Finished loading all content. Now scraping the page...")

#         # Finally scrape the full content
#         final_result = await crawler.arun(
#             url=url,
#             bypass_cache=False,
#             magic=True
#         )

#         if final_result.success:
#             markdown_content = final_result.markdown

#             # Refined regex to match only company names
#             company_pattern = r"!\[.*?\]\(.*?\)\s(.*?)\s\|"

#             matches = re.findall(company_pattern, markdown_content)
            
   
#             # Clean up duplicates and unwanted entries
#             # cleaned_names = list(set(name.strip() for name in company_names))
#             company_names = [match.strip() for match in matches]

#             print(f"Extracted Company Names: {company_names}")
#             # print(f"Extracted Company Names: {cleaned_names}")
#         else:
#             print(f"Failed to fetch content: {final_result.error_message}")

# # Run the asynchronous function
# asyncio.run(crawl_with_load_more())




#########################################################################################

# import re
# import asyncio
# from crawl4ai import AsyncWebCrawler
# from crawl4ai.chunking_strategy import RegexChunking

# async def crawl_with_load_more():
#     url = "https://www.breakthroughenergy.org/lookbook/"
    
#     async with AsyncWebCrawler(headless=True, verbose=True) as crawler:
#         load_more_selector = ".load-more-button"  # Replace with the actual CSS selector of the "Load More" button
#         has_more = True

#         while has_more:
#             print("Scrolling and attempting to load more content...")

#             # Click the "Load More" button and wait
#             result = await crawler.arun(
#                 url=url,
#                 js_code=[
#                     # Scroll to the bottom of the page
#                     "window.scrollTo(0, document.body.scrollHeight);",
#                     # Click the "Load More" button if it exists
#                     f"""
#                     const loadMoreButton = document.querySelector('{load_more_selector}');
#                     if (loadMoreButton) {{
#                         loadMoreButton.click();
#                     }} else {{
#                         console.log('No more Load More button found');
#                     }}
#                     """
#                 ],
#                 wait_for=f"js:() => !document.querySelector('{load_more_selector}') || document.readyState === 'complete'",
#                 delay_before_return_html=2.0,  # Give the page time to load more content
#                 bypass_cache=True,
#                 magic=True
#             )

#             if not result.success:
#                 print(f"Error: {result.error_message}")
#                 break

#             # Check if the "Load More" button is still present
#             has_more = f"document.querySelector('{load_more_selector}')" in result.markdown

#         print("Finished loading all content. Now scraping the page...")

#         # Finally scrape the full content
#         final_result = await crawler.arun(
#             url=url,
#             bypass_cache=True,
#             magic=True
#         )

#         if final_result.success:
#             markdown_content = result.markdown

#             # Regex to extract company names
#             company_pattern = r"(?<=\)\s).*?\|"
#             company_names = re.findall(company_pattern, markdown_content)

#             # Clean up the extracted names
#             cleaned_names = [name.strip().strip('|') for name in company_names]

#             print(f"Extracted Company Names: {cleaned_names}")
#         else:
#             print(f"Failed to fetch content: {final_result.error_message}")


# # Run the asynchronous function
# asyncio.run(crawl_with_load_more())



#########################################################################################

# async def extract_company_names():
#     # Define the URL
#     url = "https://www.breakthroughenergy.org/lookbook/"
    
#     # Use a CSS selector to target the elements containing company names
#     css_selector = "tr.logo-parent:nth-child(94) > th:nth-child(1) > span:nth-child(2)"  # Replace with the actual selector after inspecting the page structure

#     async with AsyncWebCrawler(
#         browser_type="chromium",  # Use Chromium browser
#         headless=True,           # Headless mode for efficiency
#         verbose=True             # Enable verbose logging
#     ) as crawler:
#         # Crawl the page
#         result = await crawler.arun(
#             url=url,
#             # css_selector=css_selector,    # Extract specific content using the selector
#             js_code=[
#                 # Scroll to bottom
#                 "window.scrollTo(0, document.body.scrollHeight);",
#                 # Click load more if exists
#                 "const loadMore = document.querySelector('.load-more'); if(loadMore) loadMore.click();"
#             ],
#         # Wait for new content
#             wait_for="js:() => document.querySelectorAll('.item').length > previousCount",        # Always bypass cache to fetch fresh data
#             magic=True,                   # Enable anti-detection features
#             bypass_cache=True,
#         )
        
#         if result.success:
#             markdown_content = result.markdown

#             # Regex to extract company names
#             company_pattern = r"(?<=\)\s).*?\|"
#             company_names = re.findall(company_pattern, markdown_content)

#             # Clean up the extracted names
#             cleaned_names = [name.strip().strip('|') for name in company_names]

#             print(f"Extracted Company Names: {cleaned_names}")
#         else:
#             print(f"Failed to fetch content: {result.error_message}")

#         # # Print the extracted content
#         # print(result.extracted_content)

# # Run the asynchronous function
# asyncio.run(extract_company_names())

