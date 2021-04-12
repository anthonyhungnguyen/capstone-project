package com.thesis.backend.service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.thesis.backend.dto.model.SubjectDto;
import com.thesis.backend.dto.model.SubjectIDDto;
import com.thesis.backend.dto.model.UserDto;
import com.thesis.backend.dto.request.AttendanceRequest;
import com.thesis.backend.model.Schedule;
import com.thesis.backend.util.ImageUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

import java.util.Optional;

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
    private final FirebaseImageService firebaseImageService;
    private final KafkaTemplate<String, Object> kafkaTemplate;

    @Autowired
    public AttendanceService(LogService logService, EnrollmentServiceImpl enrollmentService, UserServiceImpl userService, SubjectServiceImpl subjectService, ScheduleService scheduleService, FirebaseImageService firebaseImageService, KafkaTemplate<String, Object> kafkaTemplate) {
        this.logService = logService;
        this.enrollmentService = enrollmentService;
        this.userService = userService;
        this.subjectService = subjectService;
        this.scheduleService = scheduleService;
        this.firebaseImageService = firebaseImageService;
        this.kafkaTemplate = kafkaTemplate;
    }

    @KafkaListener(topics = ATTENDANCE_TOPIC, groupId = GROUP_ID)
    public void receiveAttendance(String message) throws JsonProcessingException {
        ObjectMapper objectMapper = new ObjectMapper();
        AttendanceRequest attendanceRequest = objectMapper.readValue(message, AttendanceRequest.class);
        byte[] imgBytes = ImageUtil.base64ToBytesArray(attendanceRequest.getImgSrcBase64());
        String path_on_cloud = "student/1710779/attendance";
        String filename = "0";
        String filetype = "image/jpeg";
        firebaseImageService.saveBase64Bytes(path_on_cloud, filename, filetype, imgBytes);
//        String result = checkAttendanceUtil(attendanceRequest);
//        kafkaTemplate.send(ATTENDANCE_RESULT_TOPIC, result);
//        if (result.equals("Successfully")) {
//            Map<String, Object> checkinResult = new HashMap<>();
//            checkinResult.put("name", attendanceRequest.getUserID());
//            checkinResult.put("feature", attendanceRequest.getFeature());
//            kafkaTemplate.send(ONLINE_LEARNING, checkinResult);
//        }
    }


    public String checkAttendanceUtil(AttendanceRequest attendanceRequest) {
        UserDto userDto = userService.find(attendanceRequest.getUserID());
        SubjectDto subjectDto = subjectService.find(new SubjectIDDto(attendanceRequest.getSubjectID(),
                attendanceRequest.getGroupCode(),
                attendanceRequest.getSemester()));
        Optional<Schedule> schedule = scheduleService.existScheduleRightNow(attendanceRequest.getDeviceID());

        if (enrollmentService.checkDidEnrolled(userDto, subjectDto)) {
            if (!logService.checkAttendanceExist(attendanceRequest, schedule.get())) {
                logService.save(attendanceRequest, "123");
                return "Successfully";
            }
            return "Exists ";
        }
        return "Unknown";
    }
}
