package com.thesis.backend.service;

import com.thesis.backend.constant.EntityType;
import com.thesis.backend.constant.ExceptionType;
import com.thesis.backend.dto.mapper.ScheduleMapper;
import com.thesis.backend.dto.request.AttendanceRequest;
import com.thesis.backend.dto.request.ScheduleRequest;
import com.thesis.backend.exception.CustomException;
import com.thesis.backend.model.Schedule;
import com.thesis.backend.repository.mysql.ScheduleRepository;
import com.thesis.backend.util.DateUtil;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.sql.Timestamp;
import java.time.Instant;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
@Slf4j
public class ScheduleService {
    private final static String GROUP_ID = "group-id";
    private final static String SCHEDULE_TOPIC = "schedule";
    private final static String ATTENDANCE_TOPIC = "attendance";
    private final static String MODIFY_TOPIC = "update";
    private final static String DELETE_TOPIC = "delete";
    private final static String DATA_TOPIC = "data";
    private final UserServiceImpl userService;
    private final ScheduleRepository scheduleRepository;
    private final KafkaTemplate<String, Object> kafkaTemplate;

    @Autowired
    public ScheduleService(UserServiceImpl userService, ScheduleRepository scheduleRepository, KafkaTemplate<String, Object> kafkaTemplate) {
        this.userService = userService;
        this.scheduleRepository = scheduleRepository;
        this.kafkaTemplate = kafkaTemplate;
    }

    public Boolean registerSchedule(ScheduleRequest scheduleRequest) throws IOException {
        LocalDateTime startDateTimeLdt = DateUtil.convertStringToLocalDateTime(scheduleRequest.getStartTime());
        LocalDateTime endDateTimeLdt = DateUtil.convertStringToLocalDateTime(scheduleRequest.getEndTime());
        // if (!checkOverlap(scheduleRequest.getDeviceID(), startDateTimeLdt, endDateTimeLdt)) {
            Schedule schedule = ScheduleMapper.toModel(scheduleRequest);
            scheduleRepository.save(schedule);
            kafkaTemplate.send(SCHEDULE_TOPIC, schedule);
        //throw CustomException.throwException(EntityType.SCHEDULE, ExceptionType.OVERLAP);
        return null;
    }

    public ScheduleRequest updateSchedule(ScheduleRequest request) {
        Optional<Schedule> schedule = scheduleRepository.findById(request.getId());
        if (schedule.isPresent()) {
            schedule.get().setStartTime(Timestamp.valueOf(DateUtil.convertStringToLocalDateTime(request.getStartTime())));
            schedule.get().setEndTime(Timestamp.valueOf(DateUtil.convertStringToLocalDateTime(request.getEndTime())));
            Schedule scheduleUpdated = scheduleRepository.save(schedule.get());
            kafkaTemplate.send(MODIFY_TOPIC, scheduleUpdated);
            return ScheduleMapper.toDto(scheduleUpdated);
        }
        throw CustomException.throwException(EntityType.SCHEDULE, ExceptionType.ENTITY_EXCEPTION, String.valueOf(request.getId()));
    }



    public void deleteSchedule(ScheduleRequest request) {
        Optional<Schedule> schedule = scheduleRepository.findById((request.getId()));
        if (schedule.isPresent()) {
            scheduleRepository.delete(schedule.get());
            kafkaTemplate.send(DELETE_TOPIC, schedule.get());
        }
        throw CustomException.throwException(EntityType.SCHEDULE, ExceptionType.ENTITY_EXCEPTION, String.valueOf(request.getId()));
    }

    public List<ScheduleRequest> fetch(int userid) {
        userService.find(userid);
        return scheduleRepository.findByTeacherID(userid)
                .stream().map(ScheduleMapper::toDto)
                .collect(Collectors.toList());
    }

    public Optional<Schedule> existScheduleRightNow(Integer deviceID) {
        Timestamp now = Timestamp.from(Instant.now());
        Optional<Schedule> schedule = Optional.ofNullable(scheduleRepository.findByDeviceIDAndStartTimeBeforeAndEndTimeAfter(deviceID, now, now));
        return schedule;
    }

    public Optional<Schedule> fetchOne(Integer deviceID, Timestamp timestamp) {
        return Optional.ofNullable(scheduleRepository.findByDeviceIDAndStartTimeBeforeAndEndTimeAfter(deviceID, timestamp, timestamp));
    }


//    private void sendData() throws IOException {
//        Resource resource = new ClassPathResource("/static/emb.pickle");
//        InputStream inputStream = resource.getInputStream();
//        try {
//            byte[] bData = FileCopyUtils.copyToByteArray(inputStream);
//            String data = new String(bData, StandardCharsets.UTF_8);
//            kafkaTemplate.send("data", data);
//        } catch (IOException ioException) {
//            log.error("IO Exception", ioException);
//        }
//    }

    public boolean checkOverlap(Integer deviceID, LocalDateTime startTime, LocalDateTime endTime) {
        Timestamp startTimeTS = Timestamp.valueOf(startTime);
        Timestamp endTimeTS = Timestamp.valueOf(endTime);
        List<Schedule> schedules = scheduleRepository.findByDeviceIDAndEndTimeAfterOrderByEndTime(deviceID, startTimeTS);
        Optional<Schedule> minEndTimeSchedule = schedules.stream().findFirst();
        if (minEndTimeSchedule.isPresent()) {
            if (endTimeTS.getTime() > minEndTimeSchedule.get().getStartTime().getTime()) {
                return true;
            }
        }
        return false;
    }
}
