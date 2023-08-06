
# Asynchronous and Synchronous DuckDuckGo Search Engine Scraper

Scrapes the [duckduckgo](https://duck.com) search engine.

# Asynchronous Example
```py
from ddg_scraper import DuckScraper
import trio


duck_scraper = DuckScraper()

async def main():
    async with duck_scraper.search("python") as results:
        async for result in results:
            ...

trio.run(main)
```

# Synchronous Example
```py
from ddg_scraper import DuckScraper


duck_scraper = DuckScraper()

with duck_scraper.search("python") as results:
    for result in results:
        ...
```

In both examples, `result` is [`ddg_scraper.SearchResult`](ddg_scraper/structs.py)

# Attributes and Methods of [`ddg_scraper.SearchResult`](ddg_scraper/structs.py)

Attributes

- `title`
- `url`
- `favicon`
- `snippet`

# How To Install

- **Using pip:** `pip install ddg-scraper`
- **Manual:**
  - Clone the folder somewhere
  - CD to the location
  - Install the packages listed in [`requirements.txt`](/requirements.txt) (`pip install -r requirements.txt`)
  - Copy the folder, [ddg_scraper](/ddg_scraper) where you want to use it.