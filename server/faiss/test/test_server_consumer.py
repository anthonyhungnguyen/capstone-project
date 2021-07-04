from confluent_kafka import Consumer

conf = {'bootstrap.servers': "34.126.168.244:9093",
        'group.id': "None",
        'auto.offset.reset': 'earliest'}

consumer = Consumer(conf)

running = True


def basic_consume_loop(consumer, topics):
    try:
        consumer.subscribe(topics)

        while running:
            msg = consumer.poll(timeout=1.0)
            print(msg)
            if msg is None:
                continue
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()


basic_consume_loop(consumer, ['test'])
