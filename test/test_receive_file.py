# from kafka import KafkaConsumer
from confluent_kafka import Consumer, KafkaException
import os
import pickle
import threading

outdir="/home/hoangphuc/OneDrive/Documents/deploy/test/files"
filename=""
# The files dictionary holds filedata objects that are dictionaries that contains file chunks.
files={}

# This class represents a bibary file chunk. It contains the actual bytes, along
# With the file name and the serial number of this chunk in the chunk list.
class datum:
    data = bytearray()
    filename = ""
    serial = 0
    __len__ = 0

    def __init__(self, data1, name1, serial1):
        self.data = data1
        self.filename = name1
        self.serial = serial1
        __len__ = len(data1)

    def getData(self):
        return self.data

    def getFileName(self):
        return self.filename

    def getSerial(self):
        return self.serial

# This class represent a whole file. It has a chunks dictionary that contains all the file's chunks, an add method that adds new chunks
# a isComplete method that determines if all th chunks of this file has arrived and a writeFile method that
# Writes all the chunks to the output file.
class filedata:
    chunks={}
    name=""
    outdir=""
    # Target is the number of chunks that this file is supposed to have
    target=0

    def __init__(self, out):
        self.outdir=out
        self.target = 0
    def add(self, key, value):
        #If this is the header entry, extract the target and the filename and ignore the binary data
        if key.startswith("Header"):
            dummy, self.name, itarget = key.split(":")
            self.target=int(itarget)
        else:
            self.chunks[key]=value

    def getFileName(self):
        return name

    def getTarget(self):
        return target

    def getValueAt(self, pointer):
        return self.chunks[pointer]

    def isComplete(self):
        if len(self.chunks)==self.target:
            return True
        else:
            return False

    def writeFile(self):
        f = open(self.outdir + "\\" + self.name, "wb")
        for i in range (1, self.target):
            data=self.getValueAt(str(i)).getData()
            f.write(data)
        f.close()

conf = {'bootstrap.servers': "localhost:9092", 'group.id': "None", 'session.timeout.ms': 6000,
            'auto.offset.reset': 'smallest'}
consumer = Consumer(conf, logger=logger)

def print_assignment(consumer, partitions):
    print('Assignment:', partitions)

# Subscribe to topics
consumer.subscribe(["filestopic"], on_assign=print_assignment)

while True:
    # Read the messages from the Kafka topic
    for msg in consumer:
        # Get the chunk
        mydatum = pickle.loads(msg.value)
        # Get the file name
        filename = mydatum.getFileName()
        # Add the file to the files dictionary if it's not already there
        if filename not in files:
            myfiledata = filedata(outdir)
            files[filename] = myfiledata
        # Add the chunk to the appropriate file data object
        files[filename].add(msg.key, mydatum)
        # Check if we already have all the chunks of the file. if yes, invoke the write file process.
        if files[filename].isComplete():
            files[filename].writeFile()
            del files[filename]
            print("Finished")