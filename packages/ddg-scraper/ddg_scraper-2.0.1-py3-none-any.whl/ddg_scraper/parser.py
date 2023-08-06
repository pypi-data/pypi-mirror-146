import contextlib

import trio
import yarl
from selectolax.parser import HTMLParser, Node

import ddg_scraper

__all__ = ["Parser"]


class Parser:
    def __init__(self, duck_scraper: ddg_scraper.DuckScraper, html: str):
        self.duck_scraper = duck_scraper
        self.parser = HTMLParser(html)
        self.result_nodes: list[Node] = self.parser.css(".result")

    def __iter__(self):
        return self

    def __aiter__(self):
        return self

    def __next__(self) -> ddg_scraper.structs.SearchResult:
        if self.result_nodes:
            result = self.result_nodes.pop(0)
            return self.parse(result)
        else:
            raise StopIteration

    def __anext__(self) -> ddg_scraper.structs.SearchResult:
        if self.result_nodes:
            result = self.result_nodes.pop(0)
            return trio.to_thread.run_sync(self.parse, result)
        else:
            raise StopAsyncIteration

    def parse(self, result: Node) -> ddg_scraper.structs.SearchResult:
        title_a = result.css_first(".result__a")
        title_text = title_a.text()
        title_href = yarl.URL(title_a.attributes.get("href").lstrip("/")).query["uddg"]

        favicon = None
        with contextlib.suppress(AttributeError):
            favicon = "https://" + result.css_first(".result__icon__img").attributes.get("src").lstrip("/")

        snippet = result.css_first(".result__snippet").text()

        return ddg_scraper.structs.SearchResult(
            title=title_text, url=title_href, favicon=favicon, snippet=snippet
        )
