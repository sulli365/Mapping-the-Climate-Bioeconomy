import re
import asyncio
from crawl4ai import AsyncWebCrawler


async def crawl_with_load_more():
    url = "https://www.breakthroughenergy.org/lookbook/"

    # from https://colab.research.google.com/drive/1zODYjhemJ5bUmYceWpVoBMVpd0ofzNBZ?usp=sharing

    # js_steps = [
    #     """
    #     const loadMoreButton = Array.from(document.querySelectorAll('button')).
    #     find(button => button.textContent.includes('Load More'));
    #     loadMoreButton && loadMoreButton.click();
    # """
    # ]

    # Also from crawl4ai assistant, only hits the button once
    # js_steps = [
    #     '''
    #     function wait(ms) {
    #         const start = Date.now();
    #         while (Date.now() - start < ms) {
    #         // Busy-wait loop
    #     }

    #     while (true) {
    #     // Identify the "Load More" button
    #         window.scrollTo(0, document.body.scrollHeight);
    #         const loadMoreButton = document.querySelector('.load-more'); // Replace with the actual selector for your button
        
    #         if (!loadMoreButton) {
    #             console.log("No 'Load More' button found. Exiting the loop.");
    #             break; // Exit the loop if the button doesn't exist
    #         }

    #         console.log("Found 'Load More' button. Clicking it...");
    #         loadMoreButton.click(); // Click the button

    #         console.log("Waiting for 2 seconds...");
    #         wait(2000); // Synchronous 2-second pause
    #     }
    # '''
    # ]

# doesnt work
    # js_steps = [
    #             '''
    #             try {
    #                 window.scrollTo(0, document.body.scrollHeight);
    #                 const loadMore = document.querySelector('a.load-more');
    #                 if (loadMore) loadMore.click();
    #             } catch {
    #                 console.log('No load more button found');
    #             }
    #             ''' 
    #         ]

  
    # from https://crawl4ai.com/mkdocs/tutorial/episode_05_JavaScript_Execution_and_Dynamic_Content_Handling/

    js_steps = [
        "window.scrollTo(0, document.body.scrollHeight);",
        "const currentCount = document.querySelectorAll('.logo-parent').length;",
        "previousCount = currentCount;",
        "const loadMore = document.querySelector('.load-more'); if (loadMore) loadMore.click();"
    ]
    # wait_for="js:() => document.querySelectorAll('.item').length > 10"  # Wait until 10 items are loaded

    # js_steps = [
    #     "window.scrollTo(0, document.body.scrollHeight);",
    #     "const loadMore = document.querySelector('.load-more'); if (loadMore) loadMore.click();"
    # ]
    # # wait_for="js:() => document.querySelectorAll('.item').length > 10"  # Wait until 10 items are loaded


    # from Crawl4ai GPT assistant
    # js_steps = [
    #             "window.scrollTo(0, document.body.scrollHeight);",  # Scroll to the bottom
    #             f"""
    #             const loadMoreButton = document.querySelector('a.load-more');
    #             if (loadMoreButton) {{
    #                 console.log('Load More button clicked.');
    #                 console.log('Load More button attributes:', loadMoreButton.outerHTML);
    #                 loadMoreButton.click();
    #             }} else {{
    #                 console.log('No more Load More button found.');
    #             }}
    #             """
    # ]  
    
    async with AsyncWebCrawler(headless=True, verbose=True) as crawler:
        # load_more_selector = ".load-more"  # Confirm this matches the correct CSS selector for the "Load More" button
        # company_card_selector = ".company-card"  # Selector for loaded content (update as needed)
        # has_more = True
        session_id = "breakthrough_scraping"

        # while has_more:
        print("Scrolling and attempting to load more content...")

        # Scroll to the bottom and click the "Load More" button
        result = await crawler.arun(
            url= url,  #"https://www.breakthroughenergy.org/lookbook/",
            session_id = session_id,
            js_code=js_steps,
            # wait_for="js:() => document.querySelectorAll('.item').length > previousCount",
            wait_for="js:() => document.querySelectorAll('.logo-parent').length > previousCount",
            # wait_for="js:() => document.querySelectorAll('table.partial > tbody:nth-child(2)').length > previousCount",
            # wait_for = "tbody:nth-child(2)",
            # wait_for = "css:.load-more",
            # wait_for="js:() => document.querySelectorAll('.item').length > 10",  # Wait until 10 items are loaded,
            
            # tr.logo-parent:nth-child(87)
            # tr.logo-parent:nth-child(88)

            delay_before_return_html=2.0,  # Wait for new content to load
            bypass_cache=True,
            magic=True,
            # word_count_threshold=10,
        )

        print(result.fit_markdown)
    
    # Clean up when done
    await crawler.crawler_strategy.kill_session(session_id)


asyncio.run(crawl_with_load_more())


############################################

import re
import asyncio
from crawl4ai import AsyncWebCrawler

async def crawl_with_load_more():
    url = "https://www.breakthroughenergy.org/lookbook/"
    
    async with AsyncWebCrawler(headless=True, verbose=True) as crawler:
        load_more_selector = ".load-more"  # Confirm this matches the correct CSS selector for the "Load More" button
        # company_card_selector = ".company-card"  # Selector for loaded content (update as needed)
        has_more = True
        session_id = "breakthrough_scraping"

        while has_more:
            print("Scrolling and attempting to load more content...")

            # Scroll to the bottom and click the "Load More" button
            result = await crawler.arun(
                url=url,
                session_id = session_id,
                js_code=[
                    "window.scrollTo(0, document.body.scrollHeight);",  # Scroll to the bottom
                    f"""
                    const loadMoreButton = document.querySelector('{load_more_selector}');
                    if (loadMoreButton) {{
                        console.log('Load More button clicked.');
                        console.log('Load More button attributes:', loadMoreButton.outerHTML);
                        loadMoreButton.click();
                    }} else {{
                        console.log('No more Load More button found.');
                    }}
                    """
                ],
                wait_for = "css:.load-more",
                #delay_before_return_html=2.0,  # Wait for new content to load
                bypass_cache=True,
                magic=True
            )

            if not result.success:
                print(f"Error: {result.error_message}")
                break

            # Pause briefly to ensure new content loads
            # await asyncio.sleep(4)

            # Check if the "Load More" button still exists
            button_check_result = await crawler.arun(
                url=url,
                session_id = session_id,
                # js_code=f"""
                # const button = document.querySelector('{load_more_selector}');
                # console.log('Load More button presence:', !!button);
                # return !!button;
                # """,
                css_selector= ".load-more",
                bypass_cache=False,
                magic=True
            )

            # Log the state of the DOM for debugging
            print(f"Load More button exists: {button_check_result.extracted_content.strip()}")

            # Update the `has_more` flag
            has_more = False # button_check_result.extracted_content.strip().lower() == "true"

        print("Finished loading all content. Now scraping the page...")

        # # Finally scrape the full content
        # final_result = await crawler.arun(
        #     url=url,
        #     session_id = session_id,
        #     bypass_cache=True,
        #     magic=True
        # )

        # if final_result.success:
        #     markdown_content = final_result.markdown

        #     # Regex to extract only company names
        #     company_pattern = r"!\[.*?\]\(.*?\)\s(.*?)\s\|"

        #     matches = re.findall(company_pattern, markdown_content)

        #     # Clean up duplicates and unwanted entries
        #     company_names = [match.strip() for match in matches]

        #     print(f"Extracted Company Names: {company_names}")
        # else:
        #     print(f"Failed to fetch content: {final_result.error_message}")

# Run the asynchronous function
asyncio.run(crawl_with_load_more())




#####################

# import re
# import asyncio
# from crawl4ai import AsyncWebCrawler


# # This JS code successfully clicks the load-more button until eventually document.querySelector(...) is null
# # window.scrollTo(0, document.body.scrollHeight),
# # document.querySelector('{load_more_selector}').click(),

# while (true) {
    
#     try {
#         document.querySelector('.load-more').click(); // Replace with the actual selector for your button
        
#     } catch (error) {
#         console.error("An error occurred:", error);
#         break
#     }
# };



# while (true) {
    
#     try {
#         document.querySelector('.load-more').click(); // Replace with the actual selector for your button
#         const start = Date.now();
#         while (Date.now() - start < 2000) {
#         // Busy-wait loop
#         }
#     } catch (error) {
#         console.error("An error occurred:", error);
#         break
#     }
# }

# while (document.querySelector('.load-more') !== null) {

#     document.querySelector('.load-more').click(); // Replace with the actual selector for your button
    
#     while (Date.now() < (Date.now() + 2000)) {
#         // Busy-wait loop
#     }
# }

# while (document.querySelector('.load-more') !== null) {

#     document.querySelector('.load-more').click(); // Replace with the actual selector for your button

# }

#     try {
#         document.querySelector('.load-more').click(); // Replace with the actual selector for your button
#         const start = Date.now();
#         while (Date.now() - start < 2000) {
#         // Busy-wait loop
#         }
#     } catch (error) {
#         console.error("An error occurred:", error);
#         break
#     }
# }

    
#     try {
#         document.querySelector('.load-more').click(); // Replace with the actual selector for your button
#         const start = Date.now();
#         while (Date.now() - start < 2000) {
#         // Busy-wait loop
#         }
#     } catch (error) {
#         console.error("An error occurred:", error);
#         break
#     }
# }
    

    


# '''
#             function clickLoadMoreButton() {
#                 // Synchronous wait function
#                 function wait(ms) {
#                     const start = Date.now();
#                     while (Date.now() - start < ms) {
#                         // Busy-wait loop
#                     }
#                 }
                
#                 while (true) {
                    
#                     // Identify the "Load More" button
#                     const loadMoreButton = document.querySelector('.load-more'); // Replace with the actual selector for your button
                    
#                     if (!loadMoreButton) {
#                         console.log("No 'Load More' button found. Exiting the loop.");
#                         break; // Exit the loop if the button doesn't exist
#                     }

#                     console.log("Found 'Load More' button. Clicking it...");
#                     loadMoreButton.click(); // Click the button

#                    const start = Date.now();
#                     while (Date.now() - start < 2000) {
#                         // Busy-wait loop
#                     }
#                 }
#             }

#             // Call the function to start the process
#             clickLoadMoreButton();
#             '''

# async def crawl_with_load_more():
#     url = "https://www.breakthroughenergy.org/lookbook/"
    
#     async with AsyncWebCrawler(headless=True, verbose=True, browser_type = "firefox") as crawler:
#         load_more_selector = ".load-more"  # Confirm this matches the correct CSS selector for the "Load More" button
#         company_card_selector = ".company-card"  # Selector for loaded content (update as needed)

#         # Scroll to the bottom and click the "Load More" button
#         result = await crawler.arun(
#             url=url,
#             js_code=[

#             '''
#             function clickLoadMoreButton() {
#                 // Synchronous wait function
#                 function wait(ms) {
#                     const start = Date.now();
#                     while (Date.now() - start < ms) {
#                         // Busy-wait loop
#                     }
#                 }
                
#                 while (true) {
                    
#                     // Identify the "Load More" button
#                     const loadMoreButton = document.querySelector('.load-more'); // Replace with the actual selector for your button
                    
#                     if (!loadMoreButton) {
#                         console.log("No 'Load More' button found. Exiting the loop.");
#                         break; // Exit the loop if the button doesn't exist
#                     }

#                     console.log("Found 'Load More' button. Clicking it...");
#                     loadMoreButton.click(); // Click the button

#                     console.log("Waiting for 2 seconds...");

#                     wait(2000); // Synchronous 2-second pause
#                 }
#             }

#             // Call the function to start the process
#             clickLoadMoreButton();
#             '''
#             ],
#             bypass_cache=True,
#             magic=True
#         )

#         if not result.success:
#             print(f"Error: {result.error_message}")

#         print("Finished loading all content. Now scraping the page...")

#         # Finally scrape the full content
#         final_result = await crawler.arun(
#             url=url,
#             bypass_cache=False,
#             magic=True
#         )

#         if final_result.success:
#             markdown_content = final_result.markdown

#             # Regex to extract only company names
#             company_pattern = r"!\[.*?\]\(.*?\)\s(.*?)\s\|"

#             matches = re.findall(company_pattern, markdown_content)

#             # Clean up duplicates and unwanted entries
#             company_names = [match.strip() for match in matches]

#             print(f"Extracted Company Names: {company_names}")
#         else:
#             print(f"Failed to fetch content: {final_result.error_message}")

# # Run the asynchronous function
# asyncio.run(crawl_with_load_more())



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

#             # Regex to extract only company names
#             company_pattern = r"!\[.*?\]\(.*?\)\s(.*?)\s\|"

#             matches = re.findall(company_pattern, markdown_content)

#             # Clean up duplicates and unwanted entries
#             company_names = [match.strip() for match in matches]

#             print(f"Extracted Company Names: {company_names}")
#         else:
#             print(f"Failed to fetch content: {final_result.error_message}")

# # Run the asynchronous function
# asyncio.run(crawl_with_load_more())


######################################################

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



######################################################
# # didnt work
# import asyncio
# from crawl4ai import AsyncWebCrawler

# async def crawl_dynamic_content():
#     # You can use wait_for to wait for a condition to be met before returning the result
#     wait_for = """() => {
#     #     return Array.from(document.querySelectorAll('article.tease-card')).length > 10;
#     # }"""

#     # wait_for can be also just a css selector
#     # wait_for = "article.tease-card:nth-child(10)"

#     url = "https://www.breakthroughenergy.org/lookbook/"

#     async with AsyncWebCrawler(verbose=True) as crawler:
#         js_code = [
#             "const loadMoreButton = Array.from(document.querySelectorAll('button')).find(button => button.textContent.includes('Load More')); loadMoreButton && loadMoreButton.click();"
#         ]
#         result = await crawler.arun(
#             url=url,
#             js_code=js_code,
#             wait_for=wait_for,
#             bypass_cache=True,
#         )
#         print(result.markdown)  # Print first 500 characters

# asyncio.run(crawl_dynamic_content())

######################################################

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
#             bypass_cache=True,
#             magic=True
#         )

#         if final_result.success:
#             markdown_content = final_result.markdown

#             # Regex to extract only company names
#             company_pattern = r"!\[.*?\]\(.*?\)\s(.*?)\s\|"

#             matches = re.findall(company_pattern, markdown_content)

#             # Clean up duplicates and unwanted entries
#             company_names = [match.strip() for match in matches]

#             print(f"Extracted Company Names: {company_names}")
#         else:
#             print(f"Failed to fetch content: {final_result.error_message}")

# # Run the asynchronous function
# asyncio.run(crawl_with_load_more())


#################################################

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

