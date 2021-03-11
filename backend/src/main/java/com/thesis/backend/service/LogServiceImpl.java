package com.thesis.backend.service;

import com.thesis.backend.dto.mapper.LogMapper;
import com.thesis.backend.dto.model.EnrollmentDto;
import com.thesis.backend.dto.model.LogDto;
import com.thesis.backend.dto.model.SubjectIDDto;
import com.thesis.backend.dto.request.AttendanceRequest;
import com.thesis.backend.model.Log;
import com.thesis.backend.repository.mongodb.LogRepository;
import com.thesis.backend.util.DateUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalTime;
import java.time.ZonedDateTime;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class LogServiceImpl implements LogService {
    private final LogRepository logRepository;

    @Autowired
    public LogServiceImpl(LogRepository logRepository) {
        this.logRepository = logRepository;
    }

    @Override
    public List<LogDto> findAllLogsBasedOnUserId(Integer userid) {
        return logRepository.findLogsByUserID(userid)
                .stream().map(LogMapper::toLogDto)
                .collect(Collectors.toList());
    }

    @Override
    public List<LogDto> findAllLogsBasedOnSubjectId(SubjectIDDto subjectIDDto) {
        return logRepository.findLogsBySubjectIDAndGroupCodeAndSemester(
                subjectIDDto.getId(),
                subjectIDDto.getGroupCode(),
                subjectIDDto.getSemester())
                .stream()
                .map(LogMapper::toLogDto)
                .collect(Collectors.toList());
    }

    @Override
    public List<LogDto> findAllLogsInTimeRange(EnrollmentDto enrollmentDto,
                                               LocalTime start,
                                               LocalTime end) {
        List<Log> logs = logRepository.findLogsByUserIDAndSubjectIDAndGroupCodeAndSemester(
                enrollmentDto.userId(),
                enrollmentDto.subjectIDDto().getId(),
                enrollmentDto.subjectIDDto().getGroupCode(),
                enrollmentDto.subjectIDDto().getSemester());
        return logs.stream().filter(
                l -> ZonedDateTime.parse(l.getTimestamp()).toLocalTime().isAfter(start)
                        && ZonedDateTime.parse(l.getTimestamp()).toLocalTime().isBefore(end))
                .map(LogMapper::toLogDto)
                .collect(Collectors.toList());

    }

    public Log saveAttendance(AttendanceRequest request) {
        return logRepository.save(Log.builder()
                .userID(request.getUserID())
                .teacherID(request.getTeacherID())
                .semester(request.getSemester())
                .subjectID(request.getSubjectID())
                .timestamp(request.getTimestamp())
                .deviceID(request.getDeviceID())
                .imgSrcBase64(request.getImgSrcBase64())
                .groupCode(request.getGroupCode())
                .build());
    }
}
