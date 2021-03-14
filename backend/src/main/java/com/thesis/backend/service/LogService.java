package com.thesis.backend.service;

import com.thesis.backend.dto.mapper.LogMapper;
import com.thesis.backend.dto.model.SubjectIDDto;
import com.thesis.backend.dto.request.AttendanceRequest;
import com.thesis.backend.model.Log;
import com.thesis.backend.repository.mongodb.LogRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.sql.Timestamp;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class LogService {
    private final LogRepository logRepository;

    @Autowired
    public LogService(LogRepository logRepository) {
        this.logRepository = logRepository;
    }

    public List<AttendanceRequest> findAllLogsBasedOnUserId(Integer userid) {
        return logRepository.findLogsByUserID(userid)
                .stream().map(LogMapper::toDto)
                .collect(Collectors.toList());
    }

    public List<AttendanceRequest> findAllLogsBasedOnSubjectId(SubjectIDDto subjectIDDto) {
        return logRepository.findLogsBySubjectIDAndGroupCodeAndSemester(
                subjectIDDto.getId(),
                subjectIDDto.getGroupCode(),
                subjectIDDto.getSemester())
                .stream()
                .map(LogMapper::toDto)
                .collect(Collectors.toList());
    }

    public List<AttendanceRequest> findAllLogsInTimeRange(AttendanceRequest attendanceRequest,
                                                          Timestamp start,
                                                          Timestamp end) {
        List<Log> logs = logRepository.findLogsByUserIDAndSubjectIDAndGroupCodeAndSemester(
                attendanceRequest.getUserID(),
                attendanceRequest.getSubjectID(),
                attendanceRequest.getGroupCode(),
                attendanceRequest.getSemester());
        return logs.stream().filter(
                l -> l.getTimestamp().isAfter(start.toLocalDateTime())
                        && l.getTimestamp().isBefore(end.toLocalDateTime()))
                .map(LogMapper::toDto)
                .collect(Collectors.toList());

    }

    public void saveAttendance(AttendanceRequest request) {
        logRepository.save(Log.builder()
                .userID(request.getUserID())
                .teacherID(request.getTeacherID())
                .semester(request.getSemester())
                .subjectID(request.getSubjectID())
                .timestamp(LocalDateTime.ofInstant(Instant.ofEpochMilli(Long.parseLong(request.getTimestamp())), ZoneId.of("Asia/Ho_Chi_Minh")))
                .deviceID(request.getDeviceID())
                .imgSrcBase64(request.getImgSrcBase64())
                .groupCode(request.getGroupCode())
                .build());
    }


}
