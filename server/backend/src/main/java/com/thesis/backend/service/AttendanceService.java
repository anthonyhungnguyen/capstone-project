package com.thesis.backend.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.thesis.backend.dto.model.SubjectDto;
import com.thesis.backend.dto.model.SubjectIDDto;
import com.thesis.backend.dto.model.UserDto;
import com.thesis.backend.dto.request.AttendanceRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

@Service
public class AttendanceService {
    private final String ATTENDANCE_TOPIC = "attendance";
    private final String ATTENDANCE_RESULT_TOPIC = "result";
    private final String ONLINE_LEARNING = "checkin";
    private final String GROUP_ID = "None";
    private final LogService logService;
    private final EnrollmentServiceImpl enrollmentService;
    private final UserServiceImpl userService;
    private final SubjectServiceImpl subjectService;
    private final ScheduleService scheduleService;
    private final KafkaTemplate<String, Object> kafkaTemplate;
    private final FirebaseService firebaseService;

    @Autowired
    public AttendanceService(LogService logService, EnrollmentServiceImpl enrollmentService, UserServiceImpl userService, SubjectServiceImpl subjectService, ScheduleService scheduleService, KafkaTemplate<String, Object> kafkaTemplate, FirebaseService firebaseService) {
        this.logService = logService;
        this.enrollmentService = enrollmentService;
        this.userService = userService;
        this.subjectService = subjectService;
        this.scheduleService = scheduleService;
        this.kafkaTemplate = kafkaTemplate;
        this.firebaseService = firebaseService;
    }

    @KafkaListener(topics = ATTENDANCE_TOPIC, groupId = GROUP_ID)
    public void receiveAttendance(String message) throws IOException {
        ObjectMapper objectMapper = new ObjectMapper();
        AttendanceRequest attendanceRequest = objectMapper.readValue(message, AttendanceRequest.class);
        String result = checkAttendanceUtil(attendanceRequest);
        kafkaTemplate.send(ATTENDANCE_RESULT_TOPIC, result);
        if (result.equals("Successfully")) {
            String savedPath = firebaseService.saveImg(attendanceRequest.getImgSrcBase64(), attendanceRequest.getUserID().toString(), attendanceRequest.getTimestamp());
            String downloadUrl = firebaseService.getDownloadUrlOnPath(savedPath);
            logService.save(attendanceRequest);
            Map<String, Object> checkinResult = new HashMap<>();
            checkinResult.put("timestamp", attendanceRequest.getTimestamp());
            checkinResult.put("feature", attendanceRequest.getFeature());
            checkinResult.put("npy_path", String.format("students/%s/attendance/photos/%s.jpg", attendanceRequest.getUserID(), attendanceRequest.getTimestamp()));
            kafkaTemplate.send(ONLINE_LEARNING, checkinResult);
        }
    }


    public String checkAttendanceUtil(AttendanceRequest attendanceRequest) {
        UserDto userDto = userService.find(attendanceRequest.getUserID());
        SubjectDto subjectDto = subjectService.find(new SubjectIDDto(attendanceRequest.getSubjectID(),
                attendanceRequest.getGroupCode(),
                attendanceRequest.getSemester()));
//        Optional<Schedule> schedule = scheduleService.existScheduleRightNow(attendanceRequest.getDeviceID());
        return "Successfully";
//        if (enrollmentService.checkDidEnrolled(userDto, subjectDto)) {
//            if (!logService.checkAttendanceExist(attendanceRequest, schedule.get())) {
//                return "Successfully";
//            }
//            return "Exists ";
//        }
//        return "Unknown";
    }
}
