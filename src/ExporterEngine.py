import time
import logging
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
import datetime
from src.prometheus_manager import ExporterAuth
from src.config_objs.PushgatewayConfig import PushgatewayConfig
from src.config_objs.JobsConfig import JobsConfig
from src.scrapers.ScrapersFactory import create_scraper


class ExporterEngine:
    def __init__(self, pushgateway_config: PushgatewayConfig, jobs_config: JobsConfig):
        self.push_config = pushgateway_config
        self.jobs_config = jobs_config
        self.auth = ExporterAuth(self.push_config.username_pushgateway, self.push_config.pass_pushgateway)
        for job in self.jobs_config.jobs:
            job.registry_prom = CollectorRegistry()
            for metric in job.metrics:  # like "ping" or similar
                scraper = create_scraper(metric)
                if scraper is None:
                    logging.error(f"Unable to create scraper type '{metric}'. Skipping.")
                    continue
                metric_descriptors = scraper.build_metrics()
                if len(metric_descriptors) == 0:
                    logging.warning(f"Metric {metric} does not scrape any metric. Skipping.")
                    continue

                job.metrics_prom[metric] = []
                for m_descriptor in metric_descriptors:
                    m_descriptor.metric_prometheus = Gauge(m_descriptor.id, m_descriptor.description, registry=job.registry_prom)
                    job.metrics_prom[metric].append(m_descriptor)
        # Also publish this exporter data
        self.registry_exporter = CollectorRegistry()
        self.url_push = "{}:{}".format(self.push_config.ip_pushgateway, self.push_config.port_pushgateway)
        self.gauge_export_time = Gauge("exporter_duration",
                                       "Duration of all metrics exprot",
                                       registry=self.registry_exporter)
        self.gauge_export_jobs = Gauge("exporter_jobs",
                                       "Number of jobs to export",
                                       registry=self.registry_exporter)

    def calculate_sleep_time(self, dur):
        sleep_time = self.jobs_config.conf.interval - dur
        logging.debug("Remaining {exporter} sleep time: {time}".format(exporter=self.jobs_config.conf.prom_id,
                                                                       time=sleep_time))
        if sleep_time < 0:
            logging.warning("Can't keep up with sleep interval! consider increasing it.")
            sleep_time = 5
        return sleep_time

    def start(self):
        while True:
            start = datetime.datetime.now()
            self.collect_once()
            dur = (datetime.datetime.now() - start).total_seconds()

            self.gauge_export_time.set(dur)
            self.gauge_export_jobs.set(len(self.jobs_config.jobs))
            sleep_time = self.calculate_sleep_time(dur)
            push_to_gateway(self.url_push, job=self.jobs_config.conf.prom_id,
                            registry=self.registry_exporter,
                            handler=self.auth.exec_auth_handler)
            time.sleep(sleep_time)

    def collect_once(self):
        try:
            logging.debug("Collecting {} metrics".format(self.jobs_config.conf.prom_id))
            for job in self.jobs_config.jobs:
                for metric, metrics_prom in job.metrics_prom.items():
                    scraper = create_scraper(metric)
                    if scraper is None:
                        logging.warning(f"Given metric '{metric}' has no scrape method attached! skipping")
                    scraper.host = job.ip
                    res = scraper.execute_once()
                    for r, m_description in zip(res, metrics_prom):
                        m_description.metric_prometheus.set(r)
                push_to_gateway(self.url_push , job=job.job,
                                registry=job.registry_prom,
                                handler=self.auth.exec_auth_handler)
        except Exception as e:
            logging.error("Err processing metrics: " + str(e))
