from dataclasses import dataclass
from typing import Union

__all__ = ["SearchResult"]


@dataclass
class SearchResult:
    """A dataclass to represent a search result.

    Attributes
    ----------
    `title`: `str`
        The title of the search result.
    `url`: `str`
        The URL of the search result.
    `favicon`: `str`
        The favicon of the search result.
    `snippet`: `str`
        The snippet of the search result.
    """

    title: str
    url: str
    favicon: Union[str, None]
    snippet: str
