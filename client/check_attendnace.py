from kafka import KafkaConsumer
consumer = KafkaConsumer("schedule")
for msg in consumer:
    print(msg)
