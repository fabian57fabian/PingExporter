from unittest import TestCase

from prometheus_client import Gauge, CollectorRegistry

from src.PrometheusPusher import PrometherusPusher, PushgatewayConfig


class TestPrometherusPusher(TestCase):
    def test_push(self):
        push_config = PushgatewayConfig("127.0.0.1", 9000, "aaa", "bbb")

        pusher = PrometherusPusher(push_config)
        registry = CollectorRegistry()
        g = Gauge("g_name", "g_doc", registry=registry)
        g.set(0.3)
        try:
            pusher.push("1", registry)
            assert False, "pushed even if no Pushgateway instance in that ip:port"
        except:
            assert True
