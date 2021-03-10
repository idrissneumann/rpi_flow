import json
import requests
import sys
from datetime import date
from datetime import datetime
from elasticsearch import Elasticsearch
from time import sleep

with open('flow_conf.json') as json_file:
    conf = json.load(json_file)
    ES_HOST = conf['elastic_host']
    ES_PORT = conf['elastic_port']
    ES_SCHEME = conf['elastic_scheme']
    ES_URL = "{}://{}:{}".format(ES_SCHEME, ES_HOST, ES_PORT)
    WAIT_TIME = conf['wait_time']
    FLOW_INDEX_PREFIX = conf['flow_meter_index_prefix']

    ESP_IP = conf['esp_ip']
    ESP_PATH = conf['esp_data_path']

es = Elasticsearch(ES_URL)

while True:
    flow_index_name = "{}_{}".format(FLOW_INDEX_PREFIX, date.today().strftime("%Y%m%d"))
    es.indices.create(index=flow_index_name, ignore=400)

    try:
        # print("Received flow meter value of : {}".format(val.strip("vp-io-3 : ")))
        # timestamp = datetime.now()
        # flow_val = float(val.strip("vp-io-3 : ").strip("\r\n"))
        # es.index(index=flow_index_name, id=timestamp,
        #          body={"flow_value": flow_val, "value_format": "l/h",
        #                "timestamp": timestamp})
        # print("http://{}{}".format(ESP_IP, ESP_PATH))
        # print(requests.get("http://{}{}".format(ESP_IP, ESP_PATH)))
        page = requests.get("http://{}{}".format(ESP_IP, ESP_PATH))
        payload = json.loads(page.content)
        print(payload)
        es.index(index=flow_index_name, id=timestamp,
                 body={"flow_value": payload, "value_format": "l/h",
                       "timestamp": timestamp})
    except:
        print("Something went wrong!", sys.exc_info()[0])

    sleep(WAIT_TIME)
