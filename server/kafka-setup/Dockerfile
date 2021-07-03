FROM confluentinc/cp-kafka:5.4.0

USER root

ENV ATTENDANCE_EVENT_NAME="attendance"
ENV RESULT_EVENT_NAME="result"
ENV CHECKIN_EVENT_NAME="checkin"
ENV SCHEDULE_EVENT_NAME="schedule"
ENV UPDATE_EVENT_NAME="update"
ENV DELETE_EVENT_NAME="delete"

COPY ./kafka-setup.sh ./kafka-setup.sh

RUN chmod 777 ./kafka-setup.sh

CMD ./kafka-setup.sh