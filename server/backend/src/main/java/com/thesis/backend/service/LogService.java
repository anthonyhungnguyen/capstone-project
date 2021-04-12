package com.thesis.backend.service;

import com.thesis.backend.dto.request.AttendanceRequest;
import com.thesis.backend.model.Log;
import com.thesis.backend.model.Schedule;
import com.thesis.backend.repository.LogRepository;
import com.thesis.backend.util.DateUtil;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class LogService {
    private final LogRepository logRepository;
    private DateUtil dateUtil;

    public LogService(LogRepository logRepository) {
        this.logRepository = logRepository;
    }

    public boolean checkAttendanceExist(AttendanceRequest request, Schedule schedule) {
        List<Log> logs =
                logRepository.findByUserIDAndSemesterAndGroupCodeAndSubjectIDAndAttendanceTimeBetween(request.getUserID(),
                        request.getSemester(), request.getGroupCode(), request.getSubjectID(), schedule.getStartTime(), schedule.getEndTime());
        return logs.size() > 0;
    }

    public Log save(AttendanceRequest attendanceRequest, String imageID) {
        Log log = Log.builder()
                .userID(attendanceRequest.getUserID())
                .semester(attendanceRequest.getSemester())
                .groupCode(attendanceRequest.getGroupCode())
                .subjectID(attendanceRequest.getSubjectID())
                .teacherID(attendanceRequest.getTeacherID())
                .deviceID(attendanceRequest.getDeviceID())
                .attendanceTime(DateUtil.convertStringToTimestamp(attendanceRequest.getTimestamp()))
                .imageID(imageID)
                .build();
        return logRepository.save(log);
    }
}
