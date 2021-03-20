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


FREE = "free"
CHECKIN = "checkin"
# BOOTSTRAP_SERVER = "10.130.98.242:9092"
BOOTSTRAP_SERVER = "127.0.0.1:9092"
GROUP = "None"
TOPIC_SCHEDULE = ["schedule"]
TOPIC_FAISS = ["faiss"]
TOPIC_ATTENDANCE = "attendance"
TOPIC_UPDATE = ["update"]
TOPIC_DELETE = ["delete"]
SCHEDULE_PATH = os.path.join(PYTHON_PATH, "ailibs_data/log/schedule.csv")
SEMESTER = 'semester'
GROUPCODE = 'groupCode'
SUBJECTID = 'subjectID'
TEACHERID = 'teacherID'
STARTTIME = 'startTime'
ENDTIME = 'endTime'
DEVICEID = 'deviceID'
ID ='id'
TIMESTAMP = 'timestamp'
conf_consumer = {'bootstrap.servers': BOOTSTRAP_SERVER, 'group.id': GROUP, 'session.timeout.ms': 6000,
                'auto.offset.reset': 'smallest'}
conf_producer = {'bootstrap.servers': BOOTSTRAP_SERVER}

USER = {'Phuc': 1752041, 'Hung': 1752259}

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
    consumer_schedule = None 
    consumer_update = None
    producer_attendance = None
    
    def __init__(self, **kwargs):
        """
        Constructor.
        Args:

        """
        if not os.path.exists(SCHEDULE_PATH):
            COLUMN_NAMES = [SEMESTER, GROUPCODE, SUBJECTID,
                            TEACHERID, STARTTIME, ENDTIME, DEVICEID, ID]
            df = pd.DataFrame(columns=COLUMN_NAMES)
            df.to_csv(SCHEDULE_PATH, index=False)
        # Create logger for consumer (logs will be emitted when poll() is called)
        logger = logging.getLogger('consumer')
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            '%(asctime)-15s %(levelname)-8s %(message)s'))
        logger.addHandler(handler)

        # Create Consumer instance
        # Hint: try debug='fetch' to generate some log messages
        config.consumer_schedule = Consumer(conf_consumer, logger=logger)
        config.consumer_update = Consumer(conf_consumer, logger=logger)
        config.producer_attendance = Producer(**conf_producer)

        def print_assignment(consumer, partitions):
            print('Assignment:', partitions)

        # Subscribe to topics
        config.consumer_schedule.subscribe(TOPIC_SCHEDULE, on_assign=print_assignment)
        config.consumer_update.subscribe(TOPIC_UPDATE, on_assign=print_assignment)        

    def schedule(self):
        # Read messages from Kafka, print to stdout
        msg = config.consumer_schedule.poll(timeout=0.01)
        # time.sleep(10)
        if msg is None:
            return
        if msg.error():
            raise KafkaException(msg.error())
        else:
            # Proper message
            sys.stderr.write('%% %s [%d] at offset %d with key %s:\n' %
                            (msg.topic(), msg.partition(), msg.offset(),
                            str(msg.key())))
            print(msg.value())
            my_json = msg.value().decode('utf8').replace("'", '"')
            data = json.loads(my_json)
            df = pd.read_csv(SCHEDULE_PATH)
            df = df.append(data, ignore_index=True)
            df.to_csv(SCHEDULE_PATH, index=False)

    def check_status(self):
        df = pd.read_csv(SCHEDULE_PATH)
        if df.empty: 
            return FREE
        df.sort_values(STARTTIME)
        if  get_time() >= df[STARTTIME][0] and  get_time() <= df[ENDTIME][0]:
            return CHECKIN
        else:
            while  get_time() > df[ENDTIME][0]:
                df = df.drop(df.index[0])
                if df.empty:
                    break
            df.to_csv(SCHEDULE_PATH, index=False)
        return FREE 

    def attendance(self, name, image):
        encoded_string = base64.b64encode(cv2.imencode(".jpg", image)[1]).decode('utf-8')
        df = pd.read_csv(SCHEDULE_PATH)
        if df.empty: 
            return FREE
        df.sort_values(STARTTIME)
        log = {'userID': str(USER[name]), SEMESTER: str(df[SEMESTER][0]), GROUPCODE: df[GROUPCODE][0], SUBJECTID: df[SUBJECTID][0], TIMESTAMP: str(get_time()),
               DEVICEID: str(df[DEVICEID][0]), 'imgSrcBase64': encoded_string, TEACHERID: str(df[TEACHERID][0])}
        msg = json.dumps(log)
        config.producer_attendance.produce(TOPIC_ATTENDANCE, msg, callback=delivery_callback)
        config.producer_attendance.poll(0)
        sys.stderr.write('%% Waiting for %d deliveries\n' % len(config.producer_attendance))
        config.producer_attendance.flush()
    
    def update(self):
        # Read messages from Kafka, print to stdout
        msg = config.consumer_update.poll(timeout=0.01)
        # time.sleep(10)
        if msg is None:
            return
        if msg.error():
            raise KafkaException(msg.error())
        else:
            # Proper message
            sys.stderr.write('%% %s [%d] at offset %d with key %s:\n' %
                            (msg.topic(), msg.partition(), msg.offset(),
                            str(msg.key())))
            print(msg.value())
            my_json = msg.value().decode('utf8').replace("'", '"')
            data = json.loads(my_json)
            df = pd.read_csv(SCHEDULE_PATH)
            df = df.drop(df.index[df.index[df[ID] == data[ID]].tolist()[0]])
            df = df.append(data, ignore_index=True)
            df.to_csv(SCHEDULE_PATH, index=False)



