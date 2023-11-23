from src.metrics.scrapers.ping import get_ping_time_ping


def create_crawler(name: str):
    if name == 'ping':
        return get_ping_time_ping
    # TODO: add more metric when needed
    return None
