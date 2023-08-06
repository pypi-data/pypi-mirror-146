import ddg_scraper

__all__ = ["DuckScraper"]


class DuckScraper:
    def __init__(self):
        self.http = ddg_scraper.HTTP()

    def search(self, query: str):
        return ddg_scraper.Scraper(self, query)
