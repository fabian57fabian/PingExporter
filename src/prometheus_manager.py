from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
from prometheus_client.exposition import basic_auth_handler


class ExporterAuth:
    def __init__(self, _usr, _pass):
        self.username = _usr
        self.password = _pass

    def exec_auth_handler(self, url, method, timeout, headers, data):
        return basic_auth_handler(url, method, timeout, headers, data, self.username, self.password)
