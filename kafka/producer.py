from confluent_kafka import Producer
import socket
import json

conf = {'bootstrap.servers': "localhost:9092",
        'client.id': socket.gethostname()}

producer = Producer(conf)
topic = "attendance"

value = """{"userID": 1752258, "semester": 201, "groupCode": "CC01", "subjectID": "CO0000",
         "timestamp": 1615628437000, "deviceID": 1, "imgSrcBase64": "12321", "teacherID": 1}"""

producer.produce(topic, key="key", value=value)
producer.flush()
