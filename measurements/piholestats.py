#!/usr/bin/env python3

import os
import logging
import requests
from datetime import datetime, timedelta

from influxdb import InfluxDBClient

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


def is_influxdb_available():
    try:
        resp=requests.get('http://localhost:8086/health')
        return resp.json()['status']=='pass'
    except:
        return False


resp = requests.get('http://pi.hole/admin/api.php')

blocklist_domains = resp.json()['domains_being_blocked']
queries_made_today = resp.json()['dns_queries_today']
queries_blocked_today = resp.json()['ads_blocked_today']

logging.info("{} on blocklist, {} queries today, {} blocked today".format(blocklist_domains, queries_made_today, queries_blocked_today))

if is_influxdb_available():
    influxtime = datetime.utcnow()
    json_body=[{ "measurement" : "pihole", "time": influxtime, "fields": { "blocklist_domains": float(blocklist_domains), "queries_made_today": float(queries_made_today), "queries_blocked_today": float(queries_blocked_today) }}]

    client = InfluxDBClient('localhost', '8086', database='everything')
    client.write_points(json_body, time_precision='ms')
    logging.info(json_body)