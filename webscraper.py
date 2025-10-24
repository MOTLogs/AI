import re
import urllib.request
import modal

app = modal.App(name="example-webscraper")
playwright_image = modal.Image.debian_slim(python_version="3.10").run_commands(
    "apt-get update",
    "apt-get install -y software-properties-common",
    "apt-add-repository non-free",
    "apt-add-repository contrib",
    "pip install playwright==1.42.0",
    "playwright install-deps chromium",
    "playwright install chromium",
)

@app.function(image=playwright_image)
async def get_links(cur_url: str) -> list[str]:
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(cur_url)
        links = await page.eval_on_selector_all(
            "a[href]", "elements => elements.map(element => element.href)"
        )
        await browser.close()

    print("Links", links)
    return list(set(links))

'''
    @app.local_entrypoint()
    def daily_scrape():
        urls = ["http://modal.com", "http://github.com"]
        for links in get_links.map(urls):
            for link in links:
                print(link)
'''

@app.function(schedule=modal.Period(days=1))
def daily_scrape():
    urls = ["http://modal.com", "http://github.com"]
    for links in get_links.map(urls):
        for link in links:
            print(link)