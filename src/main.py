import json
import requests
import sys
from datetime import date
from datetime import datetime
from elasticsearch import Elasticsearch
from time import sleep

from veggie_utils import *
from elastic_utils import es_connect

with open('flow_conf.json') as json_file:
    conf = json.load(json_file)

override_conf_from_env_array(conf, 'elastic_hosts')
override_conf_from_env(conf, 'log_level')
override_conf_from_env(conf, 'elastic_port')
override_conf_from_env(conf, 'elastic_scheme')
override_conf_from_env(conf, 'elastic_subpath')
override_conf_from_env(conf, 'elastic_username')
override_conf_from_env(conf, 'elastic_password')
override_conf_from_env(conf, 'wait_time')
override_conf_from_env(conf, 'index_prefix')
override_conf_from_env(conf, 'esp_ip')
override_conf_from_env(conf, 'esp_data_path')

LOG_LEVEL = conf['log_level']
ES_HOSTS = conf['elastic_hosts']
ES_SUBPATH = conf['elastic_subpath']
ES_PORT = cast_int(conf['elastic_port'])
ES_USER = conf['elastic_username']
ES_PASS = conf['elastic_password']
ES_SCHEME = conf['elastic_scheme']
INDEX_PREFIX = conf['index_prefix']
ESP_IP = conf['esp_ip']
ESP_PATH = conf['esp_data_path']
WAIT_TIME = cast_int(conf['wait_time'])
DATA_PIN = cast_int(conf['pin'])

es = es_connect(LOG_LEVEL, ES_SCHEME, ES_HOSTS, ES_PORT, ES_USER, ES_PASS, ES_SUBPATH)

while True:
    index_name = "{}_{}".format(INDEX_PREFIX, date.today().strftime("%Y%m%d"))
    es.indices.create(index=index_name, ignore=400)

    try:
        page = requests.get("http://{}{}".format(ESP_IP, ESP_PATH))
        payload = json.loads(page.content)
        timestamp = datetime.now()
        log_msg(LOG_LEVEL, "info", "payload = {}".format(payload))
        es.index(index=index_name, id=timestamp, body={"flow_value": payload, "value_format": "l/h", "timestamp": timestamp})
    except:
        log_msg(LOG_LEVEL, "error", "Something went wrong! i = {}".format(sys.exc_info()[0]))

    sleep(WAIT_TIME)
