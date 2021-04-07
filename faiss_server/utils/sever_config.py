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
from datetime import datetime
import pytz
from time import time
import numpy as np

BOOTSTRAP_SERVER = "34.87.104.34:9092"
GROUP = "None"
TOPIC_REGISTER = ["register"]
TOPIC_CHECKIN = ["checkin"]
TOPIC_DATA = "data"
USERID = "userId"
PHOTO = "photo"
VECTOR = "vector"
INDEX = "index"
THRESHOLD = "threshold"
conf_consumer = {'bootstrap.servers': BOOTSTRAP_SERVER, 'group.id': GROUP, 'session.timeout.ms': 6000,
                 'auto.offset.reset': 'smallest'}
conf_producer = {'bootstrap.servers': BOOTSTRAP_SERVER}


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
            TOPIC_CHECKIN, on_assign=print_assignment)

    def register(self):
        # Read messages from Kafka, print to stdout
        msg = config.consumer_register.poll(timeout=0.01)
        if msg is None:
            return None, False
        if msg.error():
            raise KafkaException(msg.error())
        else:
            # Proper message
            sys.stderr.write('%% %s [%d] at offset %d with key %s:\n' %
                             (msg.topic(), msg.partition(), msg.offset(),
                              str(msg.key())))
            print("*** GET IMAGE SUCCESS ***")
            my_json = msg.value().decode('utf8').replace("'", '"')
            data = json.loads(my_json)
            return data, True

    def checkin(self):
        # Read messages from Kafka, print to stdout
        msg = config.consumer_checkin.poll(timeout=0.01)
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

    def decode(self, photo):
        img_data = base64.b64decode(photo)
        img_array = np.fromstring(img_data, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        return img

    def send_data(self, vector, y):
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
        print(threshold)
        log = {VECTOR: vector, INDEX: y, THRESHOLD: threshold}
        msg = json.dumps(log)
        config.producer_data.produce(
            TOPIC_DATA, msg, callback=delivery_callback)
        config.producer_data.poll(0)
        sys.stderr.write('%% Waiting for %d deliveries\n' %
                         len(config.producer_data))
        config.producer_data.flush()
