import os
import logging
import json
import argparse
import threading
import time
from src.engine_exporter import Exporter
from src.config_objs.JobsConfig import JobsConfig, Conf, Job
from src.config_objs.PushgatewayConfig import PushgatewayConfig

def read_configs(conf_pushgateway_fn:str, conf_targets_dir:str) ->(PushgatewayConfig, list):
    logging.debug("Checking configuration files")
    if not os.path.isfile(conf_pushgateway_fn):
        logging.error("Pushgateay config file does not exist!")
        return None, None
    if not os.path.isdir(conf_targets_dir):
        logging.error("Targets config folder does not exist!")
        return None, None

    logging.debug("Loading config files")
    pg_config_json = {}
    with open(conf_pushgateway_fn, 'r') as file:
        pg_config_json = json.load(file)

    cfg = PushgatewayConfig(**pg_config_json)

    targets = []
    for fn in os.listdir(conf_targets_dir):
        with open(os.path.join(conf_targets_dir,fn), 'r') as file:
            targ_config_json = json.load(file)
            targ = JobsConfig(**targ_config_json)
            targ.conf = Conf(**targ.conf)
            targ.jobs = [Job(**t) for t in targ.jobs]
            targets.append(targ)

    return cfg, targets


def start_engine(push_config_path: str, configs_path: str) -> int:
    logging.info("****************************************")
    logging.info("********** Starting scraper ************")
    logging.info("****************************************")

    pg_config_json, jobs_configrations = read_configs(push_config_path, configs_path)
    if pg_config_json is None or jobs_configrations is None:
        return 1

    logging.info("Starting scraper")
    thread_list = []
    for jobs_config in jobs_configrations:
        e = Exporter(pg_config_json, jobs_config)
        th = threading.Thread(target=e.start)
        th.start()
        thread_list.append(th)
        time.sleep(4) #delayed to start ping separately
    logging.info("All exporters have started")
    for th in thread_list:
        th.join()
    return 0

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
    start_engine(args.push_config, args.configs)
