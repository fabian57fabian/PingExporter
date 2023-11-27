# scrape4prometheus

A tool to scrape multiple devices and push to prometheus gateway.

[![Python package](https://github.com/fabian57fabian/scrape4prometheus/actions/workflows/ci.yml/badge.svg)](https://github.com/fabian57fabian/scrape4prometheus/actions/workflows/ci.yml)
[![Coverage Status](https://coveralls.io/repos/github/fabian57fabian/scrape4prometheus/badge.svg)](https://coveralls.io/github/fabian57fabian/scrape4prometheus)


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
