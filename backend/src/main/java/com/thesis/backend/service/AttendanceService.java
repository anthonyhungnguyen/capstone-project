package com.thesis.backend.service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.thesis.backend.dto.model.SubjectDto;
import com.thesis.backend.dto.model.SubjectIDDto;
import com.thesis.backend.dto.model.UserDto;
import com.thesis.backend.dto.request.AttendanceRequest;
import com.thesis.backend.model.Schedule;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class AttendanceService {
    private final String ATTENDANCE_TOPIC = "attendance";
    private final String GROUP_ID = "group-id";
    private final EnrollmentServiceImpl enrollmentService;
    private final UserServiceImpl userService;
    private final SubjectServiceImpl subjectService;
    private final LogService logService;
    private final ScheduleService scheduleService;
    private final KafkaTemplate<String, Object> kafkaTemplate;

    @Autowired
    public AttendanceService(EnrollmentServiceImpl enrollmentService, UserServiceImpl userService, SubjectServiceImpl subjectService, LogService logService, ScheduleService scheduleService, KafkaTemplate<String, Object> kafkaTemplate) {
        this.enrollmentService = enrollmentService;
        this.userService = userService;
        this.subjectService = subjectService;
        this.logService = logService;
        this.scheduleService = scheduleService;
        this.kafkaTemplate = kafkaTemplate;
    }

    @KafkaListener(topics = ATTENDANCE_TOPIC, groupId = "None")
    public void receiveAttendance(String message) throws JsonProcessingException {
        System.out.println(message);
        ObjectMapper objectMapper = new ObjectMapper();
        AttendanceRequest attendanceRequest = objectMapper.readValue(message, AttendanceRequest.class);
        String result = checkAttendanceUtil(attendanceRequest);
        String ATTENDANCE_RESULT_TOPIC = "attendance_result";
        kafkaTemplate.send(ATTENDANCE_RESULT_TOPIC, result);
    }


    public String checkAttendanceUtil(AttendanceRequest attendanceRequest) {
        UserDto userDto = userService.find(attendanceRequest.getUserID());
        SubjectDto subjectDto = subjectService.find(new SubjectIDDto(attendanceRequest.getSubjectID(),
                attendanceRequest.getGroupCode(),
                attendanceRequest.getSemester()));
        Optional<Schedule> schedule = scheduleService.existScheduleRightNow(attendanceRequest.getDeviceID());

        if (enrollmentService.checkDidEnrolled(userDto, subjectDto)) {
            if (!hasChecked(attendanceRequest, schedule.get())) {
                logService.saveAttendance(attendanceRequest);
                return "Successfully";
            }
            return "You have\n checked attendance";
        }
        return "Unknown";
    }

    public boolean hasChecked(AttendanceRequest request, Schedule schedule) {
        List<AttendanceRequest> requests = logService.findAllLogsInTimeRange(request,
                schedule.getStartTime(),
                schedule.getEndTime());
        return requests.size() > 0;
    }
}
