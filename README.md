# scrape4prometheus

A tool to scrape multiple devices and push to prometheus gateway.

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
    /* Name of Server Exporter */
    "prom_id": "ExporterINFO_PROJECT",
    /* Check interval, better > JOBS * 2 */
    "interval": 55,
    /* Integer timeout, better in [1, 2] */
    "timeout": 1,
    /* Value to set as ping time on offline device */
    "value_dev_down": 3000
  },
  "jobs": [
    {
      /* job name */
      "job": "MyDevice01", 
      /* device ip reachable from server */
      "ip": "192.168.1.57",
      /* metrics list */
      "metrics": [
        "ping"
      ]
    },
    {...},
    {...}
  ]
}
```
