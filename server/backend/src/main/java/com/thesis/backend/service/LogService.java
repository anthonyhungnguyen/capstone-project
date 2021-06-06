package com.thesis.backend.service;

import com.thesis.backend.dto.request.AttendanceRequest;
import com.thesis.backend.model.Log;
import com.thesis.backend.repository.LogRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class LogService {
    private final LogRepository logRepository;

    public LogService(LogRepository logRepository) {
        this.logRepository = logRepository;
    }

    public List<Log> findLogsBasedOnUserID(Integer userid) {
        return logRepository.findByUserID(userid);
    }

    public List<Log> findLogsBasedOnTeacherID(Integer teacherid) {
        return logRepository.findByTeacherID(teacherid);
    }

    public void save(AttendanceRequest attendanceRequest, String imageLink) {
        Log log = Log.builder()
                .userID(attendanceRequest.getUserID())
                .semester(attendanceRequest.getSemester())
                .groupCode(attendanceRequest.getGroupCode())
                .subjectID(attendanceRequest.getSubjectID())
                .teacherID(attendanceRequest.getTeacherID())
                .deviceID(attendanceRequest.getDeviceID())
                .imageLink(imageLink)
                .attendanceTime(attendanceRequest.getTimestamp())
                .build();
        logRepository.save(log);
    }

    public Integer countAttendanceLogsBySubject(int semester, String subjectID, String groupCode) {
        return logRepository.countBySemesterAndSubjectIDAndGroupCode(semester, subjectID, groupCode);
    }
}
