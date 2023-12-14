import time
import logging
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
import datetime
from .PrometheusPusher import PrometherusPusher
from .config_objs.PushgatewayConfig import PushgatewayConfig
from .config_objs.JobsConfig import JobsConfig
from .scrapers.ScrapersFactory import create_scraper


class ExporterEngine:
    def __init__(self, pushgateway_config: PushgatewayConfig, jobs_config: JobsConfig):
        self.started = False
        self.requested_stop = False
        self.push_config = pushgateway_config
        self.jobs_config = jobs_config
        self.prom_pusher = PrometherusPusher(self.push_config)
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
        if self.started:
            logging.warning("Trying to start even if already started.")
            return
        self.started = True
        while not self.requested_stop:
            start = datetime.datetime.now()
            self.collect_once()
            dur = (datetime.datetime.now() - start).total_seconds()

            self.gauge_export_time.set(dur)
            self.gauge_export_jobs.set(len(self.jobs_config.jobs))
            sleep_time = self.calculate_sleep_time(dur)
            try:
                self.prom_pusher.push(self.jobs_config.conf.prom_id, self.registry_exporter)
            except Exception as e:
                logging.error("Unable to push to gateway: "+str(e))
            time.sleep(sleep_time)
        self.requested_stop = False
        self.started = False

    def stop(self):
        if self.started:
            self.requested_stop = True

    def collect_once(self):
        try:
            logging.debug("Collecting {} metrics".format(self.jobs_config.conf.prom_id))
            for job in self.jobs_config.jobs:
                if self.requested_stop:
                    return
                for metric, metrics_prom in job.metrics_prom.items():
                    scraper = create_scraper(metric)
                    if scraper is None:
                        logging.warning(f"Given metric '{metric}' has no scrape method attached! skipping")
                    scraper.host = job.ip
                    res = scraper.execute_once()
                    for r, m_description in zip(res, metrics_prom):
                        m_description.metric_prometheus.set(r)
                try:
                    if self.requested_stop:
                        return
                    self.prom_pusher.push(job.job, job.registry_prom)
                except Exception as e:
                    logging.error("Unable to push to gateway: " + str(e))
        except Exception as e:
            logging.error("Err processing metrics: " + str(e))
