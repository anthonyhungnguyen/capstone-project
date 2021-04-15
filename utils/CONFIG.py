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
import pyrebase
import faiss
import pickle
from datetime import datetime
import pytz
from time import time
import numpy as np
from utils.__init__ import timeit
# import utils libs
from utils.AIlibs import AILIBS
mAILIBS = AILIBS


FREE = "free"
CHECKIN = "checkin"
BOOTSTRAP_SERVER = "34.87.104.34:9092"
# BOOTSTRAP_SERVER = "127.0.0.1:9092"
GROUP = "None"
TOPIC_SCHEDULE = ["schedule"]
TOPIC_DATA = ["data"]
TOPIC_ATTENDANCE = "attendance"
TOPIC_UPDATE = ["update"]
TOPIC_DELETE = ["delete"]
TOPIC_RESULT = ["result"]
TOPIC_CHECKIN = "checkin"
VECTOR_FILE = "vector.index"
INDEX_FILE = "index.pickle"
THRESHOLD_FILE = "threshold.pickle"
METADATA_FILE = "meta.txt"
SCHEDULE_PATH = os.path.join(PYTHON_PATH, "ailibs_data/log/schedule.csv")
CHECKED_PATH = os.path.join(PYTHON_PATH, "ailibs_data/log/image/frame.jpg")
CHECKED_INFO_PATH = os.path.join(PYTHON_PATH, "ailibs_data/log/image/info.pickle")
CHECKED_TIME_PATH = os.path.join(PYTHON_PATH, "ailibs_data/log/image/time.txt")
VECTOR_PATH = os.path.join(PYTHON_PATH, "ailibs_data", "classifier", "faiss", VECTOR_FILE)
INDEX_PATH = os.path.join(PYTHON_PATH, "ailibs_data", "classifier", "faiss", INDEX_FILE)
THRESHOLD_PATH = os.path.join(PYTHON_PATH, "ailibs_data", "classifier", "faiss", THRESHOLD_FILE)
METADATA_PATH = os.path.join(PYTHON_PATH, "ailibs_data", "classifier", "faiss", METADATA_FILE)
SEMESTER = 'semester'
GROUPCODE = 'groupCode'
SUBJECTID = 'subjectID'
TEACHERID = 'teacherID'
STARTTIME = 'startTime'
ENDTIME = 'endTime'
DEVICEID = 'deviceID'
BASE64 = 'imgSrcBase64'
ISMATCHED = 'isMatched'
ID ='id'
TIMESTAMP = 'timestamp'
USERID = 'userID'
VECTOR = 'vector'
INDEX = 'index'
NAME = 'name'
FEATURE = 'feature'
THRESHOLD = "threshold"

conf_consumer = {'bootstrap.servers': BOOTSTRAP_SERVER, 'group.id': GROUP, 'session.timeout.ms': 6000,
                'auto.offset.reset': 'smallest', 'fetch.message.max.bytes': 15728640,
                'message.max.bytes': 15728640}
conf_producer = {'bootstrap.servers': BOOTSTRAP_SERVER, 'message.max.bytes': 15728640}

USER = {'phuc': 1752041, 'Hung': 1752259, 'Duc': 1752015, 'KhoaT': 1752025}

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
    consumer_delete = None
    producer_attendance = None
    consumer_result = None
    consumer_data = None
    producer_checkin = None
    
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
        config.consumer_data = Consumer(conf_consumer, logger=logger)
        # config.consumer_delete = Consumer(conf_consumer, logger=logger)
        config.consumer_result = Consumer(conf_consumer, logger=logger)
        config.producer_attendance = Producer(**conf_producer)
        config.producer_checkin = Producer(**conf_producer)

        def print_assignment(consumer, partitions):
            print('Assignment:', partitions)

        # Subscribe to topics
        config.consumer_schedule.subscribe(TOPIC_SCHEDULE, on_assign=print_assignment)
        config.consumer_update.subscribe(TOPIC_UPDATE, on_assign=print_assignment)
        # config.consumer_delete.subscribe(TOPIC_DELETE, on_assign=print_assignment)
        config.consumer_data.subscribe(TOPIC_DATA, on_assign=print_assignment)
        config.consumer_result.subscribe(TOPIC_RESULT, on_assign=print_assignment)  

        self.config = {"apiKey": "AIzaSyDvyKgZQdDzn49T_QX-vox-RwawATduCo0",
                       "authDomain": "capstone-bk.firebaseapp.com",
                       "projectId": "capstone-bk",
                       "storageBucket": "capstone-bk.appspot.com",
                       "messagingSenderId": "616596048413",
                       "databaseURL": "https://capstone-bk-default-rtdb.firebaseio.com",
                       "appId": "1:616596048413:web:b409fa85dca7cbe5d854f4",
                       "serviceAccount": "./serviceAccount.json"}

        self.firebase = pyrebase.initialize_app(self.config)
        self.storage = self.firebase.storage()
     

    def schedule(self):
        # Read messages from Kafka, print to stdout
        msg = config.consumer_schedule.poll(timeout=0.01)
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
            data[STARTTIME] = self.parse_time(data[STARTTIME])
            data[ENDTIME] = self.parse_time(data[ENDTIME])
            print(data)
            df = pd.read_csv(SCHEDULE_PATH)
            df = df.append(data, ignore_index=True)
            df.to_csv(SCHEDULE_PATH, index=False)
    
    def parse_time(self,time_str):
        return int(datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S").timestamp())*1000
    
    def check_status(self):
        df = pd.read_csv(SCHEDULE_PATH)
        if df.empty: 
            return FREE
        df.sort_values(STARTTIME)
        if  get_time() >= df[STARTTIME][0] and  get_time() <= df[ENDTIME][0] and \
            os.path.exists(VECTOR_PATH) and os.path.exists(INDEX_PATH) and os.path.exists(THRESHOLD_PATH):
            mAILIBS.CLASSIFIER.update(VECTOR_PATH, INDEX_PATH, THRESHOLD_PATH)
            return CHECKIN
        else:
            while get_time() > int(df[ENDTIME][0]):
                df = df.drop(df.index[0])
                df = df.reset_index()
                print(df)
                if df.empty:
                    break
            df.to_csv(SCHEDULE_PATH, index=False)
        return FREE 

    def attendance(self, flag):
        # encoded_string = base64.b64encode(cv2.imencode(".jpg", image)[1]).decode('utf-8')
        with open(CHECKED_PATH, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        # f = open(CHECKED_INFO_PATH, "r")
        # name = f.read()
        with open(CHECKED_INFO_PATH, 'rb') as encodePickle:
            user = pickle.load(encodePickle)
        df = pd.read_csv(SCHEDULE_PATH)
        if df.empty: 
            return FREE
        df.sort_values(STARTTIME)
        log = {USERID: user[NAME], FEATURE: user[FEATURE], SEMESTER: str(df[SEMESTER][0]), GROUPCODE: df[GROUPCODE][0], 
               SUBJECTID: df[SUBJECTID][0], TIMESTAMP: str(get_time()), DEVICEID: str(df[DEVICEID][0]), 
               BASE64: encoded_string, TEACHERID: str(df[TEACHERID][0]), ISMATCHED: flag}
        msg = json.dumps(log)
        config.producer_attendance.produce(TOPIC_ATTENDANCE, msg, callback=delivery_callback)
        config.producer_attendance.poll(0)
        sys.stderr.write('%% Waiting for %d deliveries\n' % len(config.producer_attendance))
        config.producer_attendance.flush()
        os.remove(CHECKED_PATH) 

        print(user)
        log = {FEATURE: user[FEATURE], NAME: user[NAME]}
        msg = json.dumps(log)
        config.producer_checkin.produce(TOPIC_CHECKIN, msg, callback=delivery_callback)
        config.producer_checkin.poll(0)
        sys.stderr.write('%% Waiting for %d deliveries\n' % len(config.producer_checkin))
        config.producer_checkin.flush()

    def attendance_result(self):
        # Read messages from Kafka, print to stdout
        msg = config.consumer_result.poll(timeout=0.01)
        if msg is None:
            return ""
        if msg.error():
            raise KafkaException(msg.error())
        else:
            # Proper message
            sys.stderr.write('%% %s [%d] at offset %d with key %s:\n' %
                            (msg.topic(), msg.partition(), msg.offset(),
                            str(msg.key())))
            print(msg.value().decode('utf8').replace("'", '"'))
            return msg.value().decode('utf8').replace("'", '"') 
    
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
            my_json = msg.value().decode('utf8')
            data = json.loads(my_json)
            df = pd.read_csv(SCHEDULE_PATH)
            df = df.drop(df.index[df.index[df[ID] == data[ID]].tolist()[0]])
            df = df.append(data, ignore_index=True)
            df.to_csv(SCHEDULE_PATH, index=False)
    
    # def delete(self):
    #     # Read messages from Kafka, print to stdout
    #     msg = config.consumer_delete.poll(timeout=0.01)
    #     # time.sleep(10)
    #     if msg is None:
    #         return
    #     if msg.error():
    #         raise KafkaException(msg.error())
    #     else:
    #         # Proper message
    #         sys.stderr.write('%% %s [%d] at offset %d with key %s:\n' %
    #                         (msg.topic(), msg.partition(), msg.offset(),
    #                         str(msg.key())))
    #         print(msg.value())
    #         my_json = msg.value().decode('utf8').replace("'", '"')
    #         data = json.loads(my_json)
    #         df = pd.read_csv(SCHEDULE_PATH)
    #         df = df.drop(df.index[df.index[df[ID] == data[ID]].tolist()[0]])
    #         df.to_csv(SCHEDULE_PATH, index=False)

    def update_data(self):
        # Read messages from Kafka, print to stdout
        msg = config.consumer_data.poll(timeout=0.01)
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
            print("****** UPDATE DATA SUCCESS *******")
            my_json = msg.value().decode('utf8')
            data = json.loads(my_json)
            list_files = self.storage.child("faiss").list_files()
            list_name = []
            for file in list_files:
                if file.name.split("/")[0]=="faiss" and len(file.name.split("/"))>1:
                    list_name.append(file.name)
            for name in list_name:
                if name.split("/")[1]=="faiss":
                    self.download_file(name.split("/",1)[1], METADATA_PATH)
            for name in list_name:
                if name.split("/")[1]!="faiss":
                    if name.split("/")[3]==VECTOR_FILE:
                        self.download_file(name, VECTOR_PATH)
                    if name.split("/")[3]==INDEX_FILE:
                        self.download_file(name, INDEX_PATH)
                    if name.split("/")[3]==THRESHOLD_FILE:
                        self.download_file(name, THRESHOLD_PATH)
            mAILIBS.CLASSIFIER.update(VECTOR_PATH, INDEX_PATH, THRESHOLD_PATH)
    
    def download_file(self, path_on_cloud, path_local):
        self.storage.child(path_on_cloud).download(path_local)

    def checked_image(self, info, feature, image):
        cv2.imwrite(CHECKED_PATH, image)
        user = {NAME: info, FEATURE: feature.tolist()}
        with open(CHECKED_INFO_PATH,"wb") as handle:
            pickle.dump(user, handle, protocol=pickle.HIGHEST_PROTOCOL)       
    
    def lasted_checking(self):
        f = open(CHECKED_TIME_PATH, "w")
        f.write(str(int(time())))
        f.close()

    def get_checked_image(self):
        if os.path.exists(CHECKED_PATH):
            return cv2.imread(CHECKED_PATH), True
        else:
            return None, False

    def course_info(self):
        df = pd.read_csv(SCHEDULE_PATH)
        if df.empty: 
            return ""
        df.sort_values(STARTTIME)
        info = df[SUBJECTID][0] + '-' + df[GROUPCODE][0]
        return info

    def check_time(self):
        if os.path.exists(CHECKED_TIME_PATH):
            f = open(CHECKED_TIME_PATH, "r")
            info = f.read()
            f.close()
            return int(time()) - int(info)>6
        else:
            return True
        




