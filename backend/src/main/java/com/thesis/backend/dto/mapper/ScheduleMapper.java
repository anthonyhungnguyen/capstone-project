package com.thesis.backend.dto.mapper;

import com.thesis.backend.dto.request.ScheduleRequest;
import com.thesis.backend.model.Schedule;
import com.thesis.backend.util.DateUtil;

import java.sql.Timestamp;

public class ScheduleMapper {
    public static Schedule toModel(ScheduleRequest request) {
        return Schedule.builder()
                .teacherID(request.getTeacherID())
                .deviceID(request.getDeviceID())
                .subjectID(request.getSubjectID())
                .groupCode(request.getGroupCode())
                .semester(request.getSemester())
                .startTime(Timestamp.valueOf(DateUtil.convertStringToLocalDateTime(request.getStartTime())))
                .endTime(Timestamp.valueOf(DateUtil.convertStringToLocalDateTime(request.getEndTime())))
                .build();
    }
}
