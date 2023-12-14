from unittest import TestCase
from src.scrapers.AbstractScraper import AbstractScraper


class TestScraper1(AbstractScraper):
    def __init__(self):
        super().__init__("Scraper1")

class TestAbstractScraper(TestCase):
    def test_get_name(self):
        assert TestScraper1().get_name() == "Scraper1"

    def test_no_implemented_build_metrics(self):
        self.assertRaises(NotImplementedError, TestScraper1().build_metrics)

    def test_no_implemented_execute_once(self):
        self.assertRaises(NotImplementedError, TestScraper1().execute_once)

