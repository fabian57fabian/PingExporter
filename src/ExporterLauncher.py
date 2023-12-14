import os
import logging
import json
import argparse
from .ExporterEngine import ExporterEngine
from .config_objs.JobsConfig import JobsConfig, Conf, Job
from .config_objs.PushgatewayConfig import PushgatewayConfig
from .utils.thread_utils import run_startables_in_parallel

class ExportersLauncher:
    def __init__(self, conf_pushgateway_fn:str, conf_targets_dir:str):
        self.conf_pushgateway_fn=conf_pushgateway_fn
        self.conf_targets_dir=conf_targets_dir
        self.cfg:PushgatewayConfig = None
        self.targets:list = []
        self.exporters = []

    def load_configs(self) -> int:
        logging.debug("Checking configuration files")
        if not os.path.isfile(self.conf_pushgateway_fn):
            logging.error("Pushgateay config file does not exist!")
            return 3
        if not os.path.isdir(self.conf_targets_dir):
            logging.error("Targets config folder does not exist!")
            return 4

        logging.debug("Loading config files")
        pg_config_json = {}
        with open(self.conf_pushgateway_fn, 'r') as file:
            pg_config_json = json.load(file)

        try:
            self.cfg = PushgatewayConfig(**pg_config_json)
        except Exception as e:
            logging.error("Error in pushgateway config file: "+str(e))
            return 1

        self.targets = []
        for fn in os.listdir(self.conf_targets_dir):
            with open(os.path.join(self.conf_targets_dir,fn), 'r') as file:
                targ_config_json = json.load(file)
                try:
                    targ = JobsConfig(**targ_config_json)
                except Exception as e:
                    logging.error(f"Error loading json config file {fn}: " + str(e))
                    return 5
                try:
                    targ.conf = Conf(**targ.conf)
                except Exception as e:
                    logging.error(f"Error loading 'conf' from config {fn}: " + str(e))
                    return 6
                jobs_parsed = []
                if type(targ.jobs) is not list:
                    logging.error(f"Error loading 'jobs' from config {fn}: 'jobs' is not a list!")
                    return 7
                try:
                    for t in targ.jobs:
                        j = Job(**t)
                        jobs_parsed.append(j)
                    targ.jobs = jobs_parsed
                except Exception as e:
                    logging.error(f"Error loading following Job from config {fn}: {t}; REASON: " + str(e))
                    return 8
                self.targets.append(targ)

        self.exporters = []
        for jobs_config in self.targets:
            try:
                e = ExporterEngine(self.cfg, jobs_config)
                self.exporters.append(e)
            except Exception as e:
                logging.error(f"Error in config file {jobs_config}: " + str(e))
                return 2
        return 0

    def start_engine(self):
        logging.info("****************************************")
        logging.info("********** Starting scraper ************")
        logging.info("****************************************")

        run_startables_in_parallel(self.exporters, delay_between=4)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--push-config", type=str, help="Config json file with pushgateway connection info")
    parser.add_argument("--configs", type=str, help="Directory where configs are located")
    parser.add_argument("--debug", type=bool, action="store_true", help="Activates debugging")
    args = parser.parse_args()
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=logging.DEBUG if args.debug else logging.INFO,
                        filename="logs_scraper.txt")
    exp = ExportersLauncher(args.push_config, args.configs)
    exp.start_engine()
