import json
import os.path
import shutil
import threading
import time
from unittest import TestCase
from unittest.mock import Mock

from src.ExporterLauncher import ExportersLauncher
from prometheus_client.registry import CollectorRegistry


def write_json(path, js):
    with open(path, "w") as file:
        json.dump(js, file)

class Test(TestCase):
    def setUp(self):
        self.pushgateway_config_fn = "push_config.json"
        self.configs_dir = "_confs_"

        self.push_config = {
            "ip_pushgateway": "100.200.150.250",
            "port_pushgateway": "9091",
            "username_pushgateway": "uuuuuu",
            "pass_pushgateway": "ppppppp"
        }
        write_json(self.pushgateway_config_fn, self.push_config)

        if os.path.exists(self.configs_dir):
            shutil.rmtree(self.configs_dir)
        os.mkdir(self.configs_dir)
        self.one_config_fn = os.path.join(self.configs_dir, "test_config.json")
        self.one_config = {
            "conf": {
                "prom_id": "ExporterDevices_project1",
                "interval": 3,
                "timeout": 1,
                "value_dev_down": 3000
            },
            "jobs": [
                {
                    "job": "Device01",
                    "ip": "127.0.0.1",
                    "metrics": ["ping"]
                },
                {
                    "job": "Device02",
                    "ip": "127.0.0.1",
                    "metrics": ["ping"]
                }
            ]
        }
        write_json(self.one_config_fn, self.one_config)

    def tearDown(self):
        if os.path.exists(self.configs_dir):
            shutil.rmtree(self.configs_dir)
        if os.path.exists(self.pushgateway_config_fn):
            os.remove(self.pushgateway_config_fn)

    def test_start_engine_fake_pushgateway(self):
        exp = ExportersLauncher(self.pushgateway_config_fn, self.configs_dir)
        res = exp.load_configs()
        assert res == 0, "Engine not loaded even if config is good"

        mocks = []
        for exporter in exp.exporters:
            m = Mock()
            mocks.append(m)
            m.return_value = True
            exporter.prom_pusher = m


        def laterkill_all():
            time.sleep(5)
            for exportrer in exp.exporters:
                exportrer.stop()
        threading.Thread(target=laterkill_all).start()

        exp.start_engine()

        all_jobs = [
            self.one_config["conf"]["prom_id"],
            self.one_config["jobs"][0]["job"],
            self.one_config["jobs"][1]["job"]
        ]

        for m in mocks:
            calls = m.push.call_args_list
            assert len(calls) > 0, "no push have been made!"
            for call in calls:
                args, kwargs = call
                job, registry = args
                assert job in all_jobs
                assert type(registry) is CollectorRegistry
