import os
from __init__ import PYTHON_PATH
from confluent_kafka import Consumer, KafkaException, Producer
import sys
import getopt
import json
import logging
from pprint import pformat
from time import time
import pandas as pd
import base64
import cv2
from datetime import datetime, date
import pytz
from time import time
import numpy as np
import pyrebase
import faiss


BOOTSTRAP_SERVER = "localhost:9092"
GROUP = "None"
TOPIC_REGISTER = ["register"]
TOPIC_SCHEDULE = ["schedule"]
TOPIC_DATA = "data"
USERID = "userId"
PHOTO = "photo"
VECTOR = "vector"
INDEX = "index"
THRESHOLD = "threshold"
VECTOR_FILE = "vector.index"
FEATURE_FILE = "features.pickle"
INDEX_FILE = "index.pickle"
THRESHOLD_FILE = "threshold.pickle"
METADATA_FILE = "metadata.json"
VECTOR_PATH = os.path.join(PYTHON_PATH, "ailibs_data", "data", VECTOR_FILE)
FEATURE_PATH = os.path.join(PYTHON_PATH, "ailibs_data", "data", FEATURE_FILE)
INDEX_PATH = os.path.join(PYTHON_PATH, "ailibs_data", "data", INDEX_FILE)
THRESHOLD_PATH = os.path.join(
    PYTHON_PATH, "ailibs_data", "data", THRESHOLD_FILE)
METADATA_PATH = os.path.join(PYTHON_PATH, "ailibs_data", "data", METADATA_FILE)
SUBJECT = "subject"

conf_consumer = {'bootstrap.servers': BOOTSTRAP_SERVER, 'group.id': GROUP, 'session.timeout.ms': 6000,
                 'auto.offset.reset': 'smallest', 'fetch.message.max.bytes': 15728640,
                 'message.max.bytes': 15728640}
conf_producer = {'bootstrap.servers': BOOTSTRAP_SERVER,
                 'message.max.bytes': 15728640}


def stats_cb(stats_json_str):
    stats_json = json.loads(stats_json_str)
    print('\nKAFKA Stats: {}\n'.format(pformat(stats_json)))


def get_time():
    return int(time()*1000)


def delivery_callback(err, msg):
    if err:
        sys.stderr.write('%% Message failed delivery: %s\n' % err)
    else:
        sys.stderr.write('%% Message delivered to %s [%d] @ %d\n' %
                         (msg.topic(), msg.partition(), msg.offset()))


class config():
    consumer_register = None
    consumer_checkin = None
    producer_data = None

    def __init__(self, **kwargs):
        """
        Constructor.
        Args:

        """
        # Create logger for consumer (logs will be emitted when poll() is called)
        logger = logging.getLogger('consumer')
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            '%(asctime)-15s %(levelname)-8s %(message)s'))
        logger.addHandler(handler)

        # Create Consumer instance
        # Hint: try debug='fetch' to generate some log messages
        config.consumer_register = Consumer(conf_consumer, logger=logger)
        config.consumer_checkin = Consumer(conf_consumer, logger=logger)
        config.producer_data = Producer(**conf_producer)

        def print_assignment(consumer, partitions):
            print('Assignment:', partitions)

        # Subscribe to topics
        config.consumer_register.subscribe(
            TOPIC_REGISTER, on_assign=print_assignment)
        config.consumer_checkin.subscribe(
            TOPIC_SCHEDULE, on_assign=print_assignment)

        self.config = {"apiKey": "AIzaSyDvyKgZQdDzn49T_QX-vox-RwawATduCo0",
                       "authDomain": "capstone-bk.firebaseapp.com",
                       "projectId": "capstone-bk",
                       "storageBucket": "capstone-bk.appspot.com",
                       "messagingSenderId": "616596048413",
                       "databaseURL": "https://capstone-bk-default-rtdb.firebaseio.com",
                       "appId": "1:616596048413:web:97990995ad196f04d854f4",
                       "serviceAccount": "./serviceAccount.json"}
        self.firebase = pyrebase.initialize_app(self.config)
        self.storage = self.firebase.storage()

    def checkin(self):
        # Read messages from Kafka, print to stdout
        msg = config.consumer_checkin.poll(0)
        if msg is None:
            return None, False
        if msg.error():
            raise KafkaException(msg.error())
        else:
            # Proper message
            sys.stderr.write('%% %s [%d] at offset %d with key %s:\n' %
                             (msg.topic(), msg.partition(), msg.offset(),
                              str(msg.key())))
            print("*** GET VECTOR SUCCESS ***")
            my_json = msg.value().decode('utf8').replace("'", '"')
            data = json.loads(my_json)
            return data, True

    def check_faiss(self, path_on_cloud):
        list_files = self.storage.child("").list_files()
        list_faiss = []
        flag = False
        SUBJECT_CODE = path_on_cloud.split("/")[1]
        TIMESTAMP = path_on_cloud.split("/")[2]
        for file in list_files:
            if file.name.split("/")[0] == SUBJECT and file.name.split("/")[1] == SUBJECT_CODE and file.name.split("/")[2] == TIMESTAMP:
                list_faiss.append(file.name)
        print(list_faiss)
        for name in list_faiss:
            print(name)
            if name.split("/")[3] == VECTOR_FILE:
                self.download_file(name, VECTOR_PATH)
                flag = True
            if name.split("/")[3] == INDEX_FILE:
                self.download_file(name, INDEX_PATH)
            if name.split("/")[3] == THRESHOLD_FILE:
                self.download_file(name, THRESHOLD_PATH)
            if name.split("/")[3] == FEATURE_FILE:
                self.download_file(name, FEATURE_PATH)   
            if name.split("/")[3] == METADATA_FILE:
                self.download_file(name, METADATA_PATH)
        return flag

    def calculate_threshold(self, vector, y):
        threshold = []
        for i, x in enumerate(vector):
            x = np.array(x).astype(np.float32)
            max_thresh_same_label = float('-inf')
            min_thresh = float('-inf')
            for i_, x_ in enumerate(vector):
                x_ = np.array(x_).astype(np.float32)
                if (y[i] != y[i_]):
                    min_thresh = max(min_thresh, np.linalg.norm(
                        x.reshape(1, 128)-x_.reshape(1, 128))**2)
                else:
                    max_thresh_same_label = max(max_thresh_same_label, np.linalg.norm(
                        x.reshape(1, 128) - x_.reshape(1, 128)) ** 2)
            harmonic = 2*(min_thresh+max_thresh_same_label) / \
                (min_thresh+max_thresh_same_label)
            if harmonic < 30:
                threshold.append((min_thresh+max_thresh_same_label)/4)
            else:
                threshold.append(harmonic)
        return threshold

    def send_data(self,timestamp, path_on_cloud, log):
        SUBJECT_CODE = path_on_cloud.split("/")[1]
        BASE_METADATA_PATH = os.path.join(
            SUBJECT, SUBJECT_CODE, timestamp, METADATA_FILE)
        BASE_VECTOR_PATH = os.path.join(
            SUBJECT, SUBJECT_CODE, timestamp, VECTOR_FILE)
        BASE_INDEX_PATH = os.path.join(
            SUBJECT, SUBJECT_CODE, timestamp, INDEX_FILE)
        BASE_THRESHOLD_PATH = os.path.join(
            SUBJECT, SUBJECT_CODE, timestamp, THRESHOLD_FILE)
        BASE_FEATURE_PATH = os.path.join(
            SUBJECT, SUBJECT_CODE, timestamp, FEATURE_FILE)

        self.put_file(BASE_METADATA_PATH, METADATA_PATH)
        self.put_file(BASE_VECTOR_PATH, VECTOR_PATH)
        self.put_file(BASE_INDEX_PATH, INDEX_PATH)
        self.put_file(BASE_THRESHOLD_PATH, THRESHOLD_PATH)
        self.put_file(BASE_FEATURE_PATH, FEATURE_PATH)
        os.remove(VECTOR_PATH)
        os.remove(FEATURE_PATH)
        os.remove(INDEX_PATH)
        os.remove(THRESHOLD_PATH)
        os.remove(METADATA_PATH)

        log[VECTOR] = BASE_VECTOR_PATH
        log[INDEX] = BASE_INDEX_PATH
        log[THRESHOLD] = BASE_THRESHOLD_PATH
        msg = json.dumps(log)
        config.producer_data.produce(TOPIC_DATA, msg, callback=delivery_callback)
        config.producer_data.poll(0)
        sys.stderr.write('%% Waiting for %d deliveries\n' % len(config.producer_data))
        config.producer_data.flush()

    def put_file(self, path_on_cloud, path_local):
        self.storage.child(path_on_cloud).put(path_local)

    def download_file(self, path_on_cloud, path_local):
        self.storage.child(path_on_cloud).download(path_local)
