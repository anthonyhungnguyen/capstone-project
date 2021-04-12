package com.thesis.backend.dto.mapper;

import com.thesis.backend.dto.request.AttendanceRequest;
import com.thesis.backend.model.Log;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class LogMapper {
    private static ModelMapper modelMapper;

    @Autowired
    public LogMapper(ModelMapper modelMapper) {
        LogMapper.modelMapper = modelMapper;
    }

    public static AttendanceRequest toDto(Log log) {
        return AttendanceRequest.builder()
                .userID(log.getUserID())
                .semester(log.getSemester())
                .groupCode(log.getGroupCode())
                .subjectID(log.getSubjectID())
                .timestamp(log.getAttendanceTime().toString())
                .deviceID(log.getDeviceID())
                .teacherID(log.getTeacherID())
                .build();
    }
}
