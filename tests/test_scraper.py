from unittest import TestCase
from src.ExporterLauncher import start_engine


class Test(TestCase):
    def test_start_engine_path_no_exists(self):
        res = start_engine("aaaaaaaaaaaaaaaaaaaaaaa", "bbbbbbbbbbbbbbbbbbbb")
        assert res == 1, "Engine started even with wrong paths"
