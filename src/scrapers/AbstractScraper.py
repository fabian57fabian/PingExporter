class AbstractScraper:
    def __init__(self, name: str):
        self.name = name

    def get_name(self):
        return self.name

    def build_metrics(self) -> list:
        raise NotImplementedError()

    def execute_once(self) -> list:
        raise NotImplementedError()
