from kafka import KafkaProducer
from confluent_kafka import Producer
import os
import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pickle

# Those are hard coded parameters. In real world you will want to put them in a config file or pass them
# as inline parameters.

# Bootstrap servers
kafka_server = "localhost:9092"
conf = {'bootstrap.servers': kafka_server}

# The directory to watch for new files
basepath = "/home/hoangphuc/OneDrive/Documents/deploy/test/vector.index"

# Chunk size
chunksize_kb = 10

num_of_threads = 4

# Utility variable that makes sure threads don't compete on the same chunk
latest = 0
file_length = 0
filename = ""

# Utility variable that holds the number of chunks that this file should have
num_of_chunks = 0


# Sends a datum down the stream to Kafka
#def send(self, mydatum):
#    self.producer.send(topic="filestopic", value=pickle.dumps(mydatum),
#                       key=pickle.dumps(mydatum.getFileName() + ":" + str(mydatum.getSerial())))

# A class that represents a single chunk of data
class datum:
    # The binary data itself
    data = bytearray()
    # The file name
    filename = ""
    # Ordinal number of this chunk in the file
    serial = 0
    __len__ = 0

    def __init__(self, data1, name1, serial1):
        self.data = data1
        self.filename = name1
        self.serial = serial1

    def getData(self):
        return self.data

    def getFileName(self):
        return self.filename

    def getSerial(self):
        return self.serial

# This is a worker thread that reads chunks of file and send them to Kafka
class worker(threading.Thread):
    # we pass in the send function so we do not have to define it again in the threads
    def __init__(self, file, send):
        threading.Thread.__init__(self)
        self.file = file
        self.send = send
        self.filename=os.path.basename(file.name)
    def run(self):
        self.dowork(self.file, self.filename)

    def dowork(self, file, filename):
        # Latest is a file high water mark, this is the latest chunk read from the file
        global latest
        global num_of_chunks
        # Iterate until we get to the last chunk, then quit
        while latest <= num_of_chunks:
            # First of all , increase latest, so no other thread will work on the same chunk as this one
            latest += 1
            # get to the offset of latest x chunk size to get to the chunk we want to read now.
            file.seek((latest - 1) * chunksize_kb * 1024)
            # read a chunk
            piece = file.read(chunksize_kb * 1024)
            # Construct a datum with the filename, the ordinal number and the actual data and send it ti Kafka
            onedatum = datum(piece, filename, latest)
            self.send(onedatum)

class CreatedHandler(FileSystemEventHandler):
    serial = 0
    producer = KafkaProducer
    global latest
    global num_of_chunks

    def __init__(self, bootstrap):
        # Create the Kafka producer (all threads share the same producer)
        self.producer = Producer(**conf)

    # Sends a datum down the stream to Kafka
    def send(self, mydatum):
        self.producer.send(topic="filestopic", value=pickle.dumps(mydatum), key=str(mydatum.getSerial()).encode('utf-8'))

    # Before sending each file we send a header that tells the consumer what is the file name and how many chunks to expect.
    # We also have to serialize the datum object.
    def send_header(self, mydatum, mykey):
        self.producer.send(topic="filestopic", value=pickle.dumps(mydatum), key=mykey.encode('utf-8'))

    # This gets fired every time a new file is created in the directory. It then calls read_split_files.
    def on_created(self, event):
        time.sleep(0.5)
        if event.is_directory:
            return
        filepath = event.src_path
        # I use TeraCopy to copy files and it creates a temporary file while copying. You probably don;t need this check.
        if 'TeraCopyTestFile' not in filepath:
            self.read_split_file(filepath)

    def read_split_file(self, filepath):
        global num_of_chunks
        # We use a dictionary to hold pointers to the spawned threads
        threadmap = {}
        f = open(filepath, 'rb')
        self.filename = os.path.basename(filepath)
        self.file_length = os.path.getsize(filepath)
        # Calculate number of chunks
        num_of_chunks = self.file_length / chunksize_kb / 1024
        some_more = self.file_length % (chunksize_kb * 1024)
        if some_more > 0:
            num_of_chunks += 1
        # The header is sent once per file in format of "Header:filename:num_of_chunks" so that the consumer knows
        # How many chunks to expect.
        header_string="Header:"+self.filename+":"+str(num_of_chunks)
        header = datum(None, self.filename, header_string)
        self.send_header(header, header_string)
        # Starting the threads
        for i in range(1, num_of_threads):
            mythread = worker(f, self.send)
            mythread.setName("Thread " + str(i))
            threadmap[i] = mythread
            mythread.start()

        # waiting the threads to finish
        for i in range(1, num_of_threads):
            threadmap[i].join()

        f.close()
        self.latest=0
        self.producer.flush()


if __name__ == "__main__":
    event_handler = CreatedHandler(kafka_server)
    observer = Observer()
    observer.schedule(event_handler, basepath, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()