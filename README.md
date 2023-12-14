# PingExporter

A tool to scrape multiple devices and push to prometheus gateway.

[![Python package](https://github.com/fabian57fabian/scrape4prometheus/actions/workflows/ci.yml/badge.svg)](https://github.com/fabian57fabian/scrape4prometheus/actions/workflows/ci.yml)
[![Coverage Status](https://coveralls.io/repos/github/fabian57fabian/PingExporter/badge.svg?branch=main)](https://coveralls.io/github/fabian57fabian/PingExporter?branch=main)

## Installation

This application requires python installed.

Execute ```python3 -m pip install -r requirements.txt ``` to install necessary requirements.

### Configuration

All configurations are written in json.

There will be a **config_xxxx.json** file for each type of device.

All targets have following template:

```json
{
  "conf": {
    "prom_id": "ExporterINFO_PROJECT",
    "interval": 55,
    "timeout": 3,
    "value_dev_down": 3000
  },
  "jobs": [
    {
      "job": "MyDevice01", 
      "ip": "192.168.1.57",
      "metrics": [
        "ping"
      ]
    },
    {
      "job": "MyDevice01", 
      "ip": "192.168.1.57",
      "metrics": [
        "ping"
      ]
    }
  ]
}
```

## How it works

Since we don't always have a connection between Prometheus server and targets, we would like to automatically retrieve some metrics and send them to PushGateway.

How PingExporter works?

- We define various **configs** project1_config.json files with above structure
- An **ExporterEngine** is given to this config and it will loop every **jobs**.
- A job is a targeted device with multiple metrics.
- An **AbstractScraper** is created for each **metric** (e.g. for "ping" is "PingScraper")
- Each **scraper** defines his own **metrics** (e.g. Pingscraper defines 'dev_ping')

Why do we need to specify multiple configs (e.g. project1_consig.json, project2_config.json)?
Because we may want to monitor metrics every 30 seconds but i have 50 devices, so although ping is fast, we may break the 40 seconds barrier (we don't keep up with the export loop).

But if we split those devices in multiple configs (remember, each config has its own cycle in its own thread), we are ok.
Besides that, we can define the scrape interval for each config!

Monitoring PingExporter performances is easy, since it exports itself a exporter_duration and exporter_job for each config.
