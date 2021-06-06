package com.thesis.backend.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.thesis.backend.dto.request.AttendanceRequest;
import com.thesis.backend.model.CacheAttendance;
import com.thesis.backend.repository.RedisRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
@Slf4j
public class AttendanceService {
    private final String ATTENDANCE_TOPIC = "attendance";
    private final String ATTENDANCE_RESULT_TOPIC = "result";
    private final String ONLINE_LEARNING = "checkin";
    private final String GROUP_ID = "None";
    private final LogService logService;
    private final KafkaTemplate<String, Object> kafkaTemplate;
    private final FirebaseService firebaseService;
    private final RedisRepository redisRepository;

    @Autowired
    public AttendanceService(LogService logService, KafkaTemplate<String, Object> kafkaTemplate, FirebaseService firebaseService, RedisRepository redisRepository) {
        this.logService = logService;
        this.kafkaTemplate = kafkaTemplate;
        this.firebaseService = firebaseService;
        this.redisRepository = redisRepository;
    }

    @KafkaListener(topics = ATTENDANCE_TOPIC, groupId = GROUP_ID)
    public void receiveAttendance(String message) throws IOException {
        log.info("ATTENDANCE MESSAGE: {}", message);
        ObjectMapper objectMapper = new ObjectMapper();
        AttendanceRequest attendanceRequest = objectMapper.readValue(message, AttendanceRequest.class);
        if (attendanceRequest.getIsMatched().equals(true)) {
            String result = checkAttendanceUtil(attendanceRequest);
            log.info("ATTENDANCE RESULT {}", result);
            kafkaTemplate.send(ATTENDANCE_RESULT_TOPIC, result);
            if (result.equals("Successfully")) {
                String imageLink = firebaseService.saveImg(attendanceRequest.getImgSrcBase64(), attendanceRequest.getUserID().toString(), attendanceRequest.getTimestamp());
                logService.save(attendanceRequest, imageLink);
                kafkaSendCheckInResult(attendanceRequest);
            }
        }
    }


    private void kafkaSendCheckInResult(AttendanceRequest attendanceRequest) {
        Map<String, Object> checkinResult = new HashMap<>();
        checkinResult.put("timestamp", attendanceRequest.getTimestamp());
        checkinResult.put("feature", attendanceRequest.getFeature());
        checkinResult.put("npy_path", String.format("student/%s/attendance/features/", attendanceRequest.getUserID()));
        kafkaTemplate.send(ONLINE_LEARNING, checkinResult);
    }


    public String checkAttendanceUtil(AttendanceRequest attendanceRequest) {
        String classCode = String.format("%s_%s_%s", attendanceRequest.getSemester(), attendanceRequest.getSubjectID(), attendanceRequest.getGroupCode());
        CacheAttendance cacheAttendance = redisRepository.findById(classCode);
        String timestamp = attendanceRequest.getTimestamp();
        Integer userID = attendanceRequest.getUserID();
        log.info("[checkAttendanceUtil] userID: {}, subjectID: {}", userID, classCode);
        log.info("Cache attendances: {}", redisRepository.findById(classCode));
        if (timestamp.compareTo(cacheAttendance.getStartTime()) > 0 && timestamp.compareTo(cacheAttendance.getEndTime()) < 0) {
            if (cacheAttendance.getStudentList().contains(userID)) {
                if (!cacheAttendance.getStudentHaveAttendances().contains(userID)) {
                    List<Integer> studentHaveAttendances = cacheAttendance.getStudentHaveAttendances();
                    studentHaveAttendances.add(userID);
                    cacheAttendance.setStudentHaveAttendances(studentHaveAttendances);
                    redisRepository.save(cacheAttendance);
                    return "Successfully";
                }
                return "Exists";
            }
            return "Not found";
        }
        return "No schedule";
    }

}
