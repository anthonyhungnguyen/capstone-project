#!/bin/bash
: ${PARTITIONS:=1}
: ${REPLICATION_FACTOR:=1}

: ${KAFKA_PROPERTIES_SECURITY_PROTOCOL:=PLAINTEXT}

kafka-topics --create --if-not-exists --zookeeper $KAFKA_ZOOKEEPER_CONNECT --replication-factor $REPLICATION_FACTOR --partitions $PARTITIONS --topic $ATTENDANCE_EVENT_NAME

kafka-topics --create --if-not-exists --zookeeper $KAFKA_ZOOKEEPER_CONNECT --replication-factor $REPLICATION_FACTOR --partitions $PARTITIONS --topic $RESULT_EVENT_NAME

kafka-topics --create --if-not-exists --zookeeper $KAFKA_ZOOKEEPER_CONNECT --replication-factor $REPLICATION_FACTOR --partitions $PARTITIONS --topic $CHECKIN_EVENT_NAME

kafka-topics --create --if-not-exists --zookeeper $KAFKA_ZOOKEEPER_CONNECT --replication-factor $REPLICATION_FACTOR --partitions $PARTITIONS --topic $SCHEDULE_EVENT_NAME

kafka-topics --create --if-not-exists --zookeeper $KAFKA_ZOOKEEPER_CONNECT --replication-factor $REPLICATION_FACTOR --partitions $PARTITIONS --topic $UPDATE_EVENT_NAME

kafka-topics --create --if-not-exists --zookeeper $KAFKA_ZOOKEEPER_CONNECT --replication-factor $REPLICATION_FACTOR --partitions $PARTITIONS --topic $DELETE_EVENT_NAME
