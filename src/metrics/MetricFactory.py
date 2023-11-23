from src.metrics.Metricdescriptor import Metricdescriptor
from src.metrics.scrapers.ping import build_ping_metrics

def create_metrics(name:str) -> list:
    if name=='ping':
        return build_ping_metrics()
    # TODO: add more metric when needed
    return []