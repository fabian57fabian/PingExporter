from unittest import TestCase
import json
import os
import shutil
from src.ExporterLauncher import ExportersLauncher


def write_json(path, js):
    with open(path, "w") as file:
        json.dump(js, file)


class TestExportersLauncherErrorsLoading(TestCase):
    def setUp(self):
        self.config_fn_good = "test_push_file_err_loading.json"
        cfg = {
            "ip_pushgateway": "100.200.150.250",
            "port_pushgateway": "9091",
            "username_pushgateway": "uuuuuu",
            "pass_pushgateway": "ppppppp"
        }
        write_json(self.config_fn_good, cfg)

        self.config_fn_wrong = "test_push_file_err_loading_wrong.json"
        cfg_wrong = {
            "ip_pushgateway": 1,
            "username_pushgateway": "uuuuuu",
            "asdhvykishucvskljdv": "saoidhpisubvfbiu"
        }
        write_json(self.config_fn_wrong, cfg_wrong)

        self.configs_dir = "test_configs_dir_errors_loading"
        if os.path.exists(self.configs_dir):
            shutil.rmtree(self.configs_dir)
        os.mkdir(self.configs_dir)
        self.one_config_fn = os.path.join(self.configs_dir, "test_config.json")
        self.one_config = {
            "conf": {
                "prom_id": "ExporterDevices_project1",
                "interval": 55,
                "timeout": 1,
                "value_dev_down": 3000
            },
            "jobs": [
                {
                    "job": "Device01",
                    "ip": "127.0.0.1",
                    "metrics": ["ping"]
                }
            ]
        }
        write_json(self.one_config_fn, self.one_config)

        self.configs_dir_wrong = "test_configs_dir_errors_loading"
        if os.path.exists(self.configs_dir_wrong):
            shutil.rmtree(self.configs_dir_wrong)
        os.mkdir(self.configs_dir_wrong)
        self.one_config_wrong_fn = os.path.join(self.configs_dir_wrong, "test_config.json")
        self.one_config_wrong = {
            "conf": {
                "prom_id": "ExporterDevices_project1",
                "interval": 55,
                "timeout": 1,
                "value_dev_down": 3000
            },
            "jobs": [
                {
                    "job": "Device01",
                    "ipasdasda": "127.0.0.1",
                    "metrics": 7
                }
            ]
        }
        write_json(self.one_config_wrong_fn, self.one_config_wrong)

    def tearDown(self):
        if os.path.exists(self.config_fn_good):
            os.remove(self.config_fn_good)
        if os.path.exists(self.config_fn_wrong):
            os.remove(self.config_fn_wrong)
        if os.path.exists(self.configs_dir):
            shutil.rmtree(self.configs_dir)
        if os.path.exists(self.configs_dir_wrong):
            shutil.rmtree(self.configs_dir_wrong)

    def test_ExportersLauncher_nopushgatwey_conf(self):
        exp = ExportersLauncher("aaaaaaaaaaaaaaaaaaaaaaa", self.configs_dir)
        res = exp.load_configs()
        assert res > 0, "Engine loaded even with wrong paths"

    def test_ExportersLauncher_notargets_dir(self):
        exp = ExportersLauncher(self.config_fn_good, "bbbbbbbbbbbbbbbbbbbb")
        res = exp.load_configs()
        assert res > 0, "Engine loaded even with wrong config dir"

    def test_ExportersLauncher_wrong_pushgatewaw(self):
        exp = ExportersLauncher(self.config_fn_wrong,  self.configs_dir)
        res = exp.load_configs()
        assert res > 0, "Engine loaded even with wrong pushgateway config"

    def test_ExportersLauncher_wrong_targets(self):
        exp = ExportersLauncher(self.config_fn_good,  self.configs_dir_wrong)
        res = exp.load_configs()
        assert res > 0, "Engine loaded even with wrong pushgateway config"
