import logging
import shlex
from subprocess import Popen, PIPE, STDOUT

from AbstractScraper import AbstractScraper
from src.scrapers.Metricdescriptor import Metricdescriptor


def _get_simple_cmd_output(cmd, stderr=STDOUT):
    """
    Execute a simple external command and get its output.
    """
    args = shlex.split(cmd)
    return Popen(args, stdout=PIPE, stderr=stderr).communicate()[0]


class PingScraper(AbstractScraper):
    def __init__(self):
        super().__init__("ping")
        self.host = ""
        self.count = 1
        self.timeout_sec = 2
        self.val_dev_down = 3000

    def build_metrics(self) -> list:
        return [
            Metricdescriptor("dev_ping", "Ping to device (ms)")
        ]

    def execute_once(self) -> list:
        try:
            host = self.host.split(':')[0]
            cmd = "ping {host} -c {count} -t {timeout} -q".format(host=host, count=self.count, timeout=int(self.timeout_sec))
            res_process = _get_simple_cmd_output(cmd)
            lines = res_process.decode('utf-8').split('\n')
            res = lines[-1]
            if res == '':
                res = lines[-2]
            if 'rtt' not in res:
                return [self.val_dev_down]
            if 'pipe' in res:
                return [self.val_dev_down]
            res = res.split('=')[1]
            res = res.split('/')
            res_avg = float(res[1])
            return [res_avg]
        except Exception as e:
            logging.error("Got erro trying to ping: " + str(e))
            return [self.val_dev_down]