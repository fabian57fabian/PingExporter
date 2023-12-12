from typing import Optional

from .AbstractScraper import AbstractScraper

from src.scrapers.PingScraper import PingScraper


def create_scraper(name: str) -> Optional[AbstractScraper]:
    if name == 'ping':
        return PingScraper()
    # TODO: add more metric when needed
    return None
