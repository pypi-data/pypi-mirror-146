import ddg_scraper

__all__ = ["Scraper"]


class Scraper(ddg_scraper.abc.CoroutineHandler):
    def __init__(self, duck_scraper: ddg_scraper.DuckScraper, query: str):
        self.duck_scraper = duck_scraper
        self.query = query

    @property
    def search_url(self):
        return str(self.duck_scraper.http.BASE_URL.with_query(q=self.query))

    def sync_method(self):
        with self.duck_scraper.http.get(self.search_url) as response:
            return ddg_scraper.Parser(self.duck_scraper, response.text)

    async def async_method(self):
        async with self.duck_scraper.http.get(self.search_url) as response:
            return ddg_scraper.Parser(self.duck_scraper, response.text)

    def __enter__(self) -> ddg_scraper.Parser:
        return super().__enter__()

    async def __aenter__(self) -> ddg_scraper.Parser:
        return await super().__aenter__()
