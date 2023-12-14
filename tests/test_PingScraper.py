from unittest import TestCase

from src.scrapers.PingScraper import PingScraper

class TestPingScraper(TestCase):
    scraper = PingScraper()
    scraper.host = "127.0.0.1"
    res = scraper.execute_once()
    # Every scraper returns a list of metrics
    assert type(res) is list
    assert len(res) == 1
    assert type(res[0]) is float
    assert 0 <= res[0] < 1000, "local ping should be positive but less than 1000."
