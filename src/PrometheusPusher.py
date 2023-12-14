from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
from prometheus_client.exposition import basic_auth_handler
from src.config_objs.PushgatewayConfig import PushgatewayConfig


class ExporterAuth:
    def __init__(self, _usr, _pass):
        self.username = _usr
        self.password = _pass

    def exec_auth_handler(self, url, method, timeout, headers, data):
        return basic_auth_handler(url, method, timeout, headers, data, self.username, self.password)


class PrometherusPusher:
    def __init__(self, push_config: PushgatewayConfig):
        self.push_config = push_config
        self.url_push = f"{self.push_config.ip_pushgateway}:{self.push_config.port_pushgateway}"
        self.auth = ExporterAuth(self.push_config.username_pushgateway, self.push_config.pass_pushgateway)

    def push(self, job, registry):
        push_to_gateway(self.url_push, job=job, registry=registry, handler=self.auth.exec_auth_handler)
