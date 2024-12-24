import asyncio
from crawl4ai import AsyncWebCrawler, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
import json

async def main():
    schema = {
        "name": "Breakthrough Energy Companies",
        "baseSelector": "tr.logo-parent",
        "fields": [
            {
                "name": "company_name",
                "selector": "th.name span.title",
                "type": "text",
            },
            {
                "name": "company_extra",
                "selector": "th.name span.extra",
                "type": "text", 
            },
            {
                "name": "description",
                "selector": "td.description",
                "type": "text",
            },
            {
                "name": "sector",
                "selector": "td.detail-1 span[role='tooltip']",
                "type": "text", 
            },
            {
                "name": "program",
                "selector": "td.detail-2",
                "type": "text",
            },
            {
                "name": "technology", 
                "selector": "td.detail-3",
                "type": "text",
            },
            {
                "name": "logo_url",
                "selector": "th.name img.logo",
                "type": "attribute",
                "attribute": "src"
            }
        ],
    }

    extraction_strategy = JsonCssExtractionStrategy(schema, verbose=True)

    async with AsyncWebCrawler(
        headless=False,
        verbose=True
    ) as crawler:
        
        # Create the JavaScript that handles clicking multiple times
        js_click_load = """
        (async () => {
            for(let i = 0; i < 6; i++) {
                const loadButton = document.querySelector('.load-more');
                if (!loadButton) {
                    console.log('No more load button found');
                    break;
                }
                
                loadButton.scrollIntoView();
                loadButton.click();
                await new Promise(r => setTimeout(r, 1000));
            }
        })();
        """        

        result = await crawler.arun(
            url="https://www.breakthroughenergy.org/lookbook/",
            extraction_strategy=extraction_strategy,
            cache_mode=CacheMode.BYPASS,
            js_code=js_click_load,
        )

        companies = json.loads(result.extracted_content)
        print(f"Successfully extracted {len(companies)} companies")
         
        # Print the first item
        print(json.dumps(companies[0], indent=2))


if __name__ == "__main__":
    asyncio.run(main())
