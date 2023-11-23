
class Conf:
    interval: int
    timeout: int
    value_dev_down: int
    prom_id: str

    def __init__(self, interval: int, timeout: int, value_dev_down: int, prom_id: str) -> None:
        self.interval = interval
        self.timeout = timeout
        self.value_dev_down = value_dev_down
        self.prom_id = prom_id

class Job:
    job: str
    ip: str
    metrics: list
    metrics_prom: dict
    registry_prom: object

    def __init__(self, job: str, ip: str, metrics: list) -> None:
        self.job = job
        self.ip = ip
        self.metrics = metrics
        self.registry_prom = None
        self.metrics_prom = {}


class JobsConfig:
    conf: Conf
    jobs: list

    def __init__(self, conf: Conf, jobs: list) -> None:
        self.conf = conf
        self.jobs = jobs
