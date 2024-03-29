#!/usr/bin/env python
#
# Copyright 2016 Confluent Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

#
# Example high-level Kafka 0.9 balanced Consumer
#
from confluent_kafka import Consumer, KafkaException
import sys
import getopt
import json
import logging
from pprint import pformat
import time
import pandas as pd
from datetime import datetime
import pytz

# COLUMN_NAMES = ['semester', 'groupCode', 'subjectID',
#                 'teacherID', 'startTime', 'endTime', 'deviceID', 'id']
# df = pd.DataFrame(columns=COLUMN_NAMES)
# df.to_csv('schedule.csv', index=False)


def stats_cb(stats_json_str):
    stats_json = json.loads(stats_json_str)
    print('\nKAFKA Stats: {}\n'.format(pformat(stats_json)))


def print_usage_and_exit(program_name):
    sys.stderr.write(
        'Usage: %s [options..] <bootstrap-brokers> <group> <topic1> <topic2> ..\n' % program_name)
    options = '''
 Options:
  -T <intvl>   Enable client statistics at specified interval (ms)
'''
    sys.stderr.write(options)   
    sys.exit(1)


if __name__ == '__main__':
    optlist, argv = getopt.getopt(sys.argv[1:], 'T:')
    if len(argv) < 3:
        print_usage_and_exit(sys.argv[0])

    broker = argv[0]
    group = argv[1]
    topics = argv[2:]
    # Consumer configuration
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    conf = {'bootstrap.servers': broker, 'group.id': group, 'session.timeout.ms': 6000,
            'auto.offset.reset': 'smallest'}

    # Check to see if -T option exists
    for opt in optlist:
        if opt[0] != '-T':
            continue
        try:
            intval = int(opt[1])
        except ValueError:
            sys.stderr.write("Invalid option value for -T: %s\n" % opt[1])
            sys.exit(1)

        if intval <= 0:
            sys.stderr.write(
                "-T option value needs to be larger than zero: %s\n" % opt[1])
            sys.exit(1)

        conf['stats_cb'] = stats_cb
        conf['statistics.interval.ms'] = int(opt[1])

    # Create logger for consumer (logs will be emitted when poll() is called)
    logger = logging.getLogger('consumer')
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        '%(asctime)-15s %(levelname)-8s %(message)s'))
    logger.addHandler(handler)

    # Create Consumer instance
    # Hint: try debug='fetch' to generate some log messages
    c = Consumer(conf, logger=logger)

    def print_assignment(consumer, partitions):
        print('Assignment:', partitions)

    # Subscribe to topics
    c.subscribe(topics, on_assign=print_assignment)

    # Read messages from Kafka, print to stdout
    try:
        while True:
            msg = c.poll(timeout=1.0)
            # time.sleep(10)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())
            else:
                # Proper message
                sys.stderr.write('%% %s [%d] at offset %d with key %s:\n' %
                                 (msg.topic(), msg.partition(), msg.offset(),
                                  str(msg.key())))
                # print(msg.value())
                my_json = msg.value().decode('utf8').replace("'", '"')
                data = json.loads(my_json)
                print(data)
                # print(type(data))
                # df = pd.read_csv('schedule.csv')
                # df = df.append(data, ignore_index=True)
                # print(df)
                # df.to_csv('schedule.csv', index=False)
                # print(data['startTime'])
                # print(type(data['endTime']))
                # print(time.time())
                # data['startTime'] = datetime.strptime(data['startTime'], "%Y-%m-%d %H:%M:%S").timestamp()
                # data['endTime'] = datetime.strptime(data['endTime'], "%Y-%m-%d %H:%M:%S").timestamp()
                # print(data)
                # tz1 = pytz.timezone('GMT')
                # now = pytz.UTC.localize(utc_time)
                # now_tz = now.astimezone(tz1)
                # print(now_tz)
                # print(now_tz.strftime('%s'))


    except KeyboardInterrupt:
        sys.stderr.write('%% Aborted by user\n')

    finally:
        # Close down consumer to commit final offsets.
        c.close()
