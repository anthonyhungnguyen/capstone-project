package com.thesis.backend.service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.thesis.backend.dto.mapper.ScheduleMapper;
import com.thesis.backend.dto.request.AttendanceRequest;
import com.thesis.backend.dto.request.ScheduleRequest;
import com.thesis.backend.model.Schedule;
import com.thesis.backend.util.DateUtil;
import lombok.extern.slf4j.Slf4j;
import org.apache.tomcat.jni.Local;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.ClassPathResource;
import org.springframework.core.io.Resource;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;
import org.springframework.util.FileCopyUtils;

import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.time.LocalDateTime;

@Service
@Slf4j
public class AutomationService {
    private final static String GROUP_ID = "group-id";
    private final static String SCHEDULE_TOPIC = "schedule";
    private final static String ATTENDANCE_TOPIC = "attendance";
    private final static String MODIFY_TOPIC = "modify";
    private final static String DELETE_TOPIC = "delete";
    private final static String DATA_TOPIC = "data";
    private final KafkaTemplate<String, Object> kafkaTemplate;
    private final AttendanceService attendanceService;
    private final ScheduleService scheduleService;
    private final String BASE_URL = "http://localhost:3000/";

    @Autowired
    public AutomationService(KafkaTemplate<String, Object> kafkaTemplate, AttendanceService attendanceService, ScheduleService scheduleService) {
        this.kafkaTemplate = kafkaTemplate;
        this.attendanceService = attendanceService;
        this.scheduleService = scheduleService;
    }

    public Boolean registerSchedule(ScheduleRequest scheduleRequest) throws IOException {
        LocalDateTime startDateTimeLdt = DateUtil.convertStringToLocalDateTime(scheduleRequest.getStartTime());
        LocalDateTime endDateTimeLdt = DateUtil.convertStringToLocalDateTime(scheduleRequest.getEndTime());
        if (!scheduleService.checkOverlap(scheduleRequest.getDeviceID(), startDateTimeLdt, endDateTimeLdt)) {
            Schedule schedule = ScheduleMapper.toModel(scheduleRequest);
            scheduleService.save(schedule);
            kafkaTemplate.send(SCHEDULE_TOPIC, schedule);
        }
        return true;
    }

    @KafkaListener(topics = ATTENDANCE_TOPIC, groupId = GROUP_ID)
    public void receiveAttendance(String message) throws JsonProcessingException {
        ObjectMapper objectMapper = new ObjectMapper();
        AttendanceRequest attendanceRequest = objectMapper.readValue(message, AttendanceRequest.class);
        attendanceService.checkAttendanceUtil(attendanceRequest);
    }


    private void sendData() throws IOException {
        Resource resource = new ClassPathResource("/static/emb.pickle");
        InputStream inputStream = resource.getInputStream();
        try {
            byte[] bData = FileCopyUtils.copyToByteArray(inputStream);
            String data = new String(bData, StandardCharsets.UTF_8);
            kafkaTemplate.send("data", data);
        } catch (IOException ioException) {
            log.error("IO Exception", ioException);
        }
    }
}
