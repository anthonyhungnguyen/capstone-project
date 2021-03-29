package com.thesis.backend.dto.mapper;

import com.thesis.backend.dto.request.ScheduleRequest;
import com.thesis.backend.model.Schedule;

import java.sql.Timestamp;

public class ScheduleMapper {
    public static Schedule toModel(ScheduleRequest request) {
        return Schedule.builder()
                .teacherID(request.getTeacherID())
                .deviceID(request.getDeviceID())
                .subjectID(request.getSubjectID())
                .groupCode(request.getGroupCode())
                .semester(request.getSemester())
                .startTime(Timestamp.valueOf(request.getStartTime()))
                .endTime(Timestamp.valueOf(request.getEndTime()))
                .build();
    }

    public static ScheduleRequest toDto(Schedule schedule) {
        return ScheduleRequest.builder()
                .id(schedule.getId())
                .teacherID(schedule.getTeacherID())
                .deviceID(schedule.getDeviceID())
                .subjectID(schedule.getSubjectID())
                .groupCode(schedule.getGroupCode())
                .semester(schedule.getSemester())
                .startTime(schedule.getStartTime().toLocalDateTime().toString())
                .endTime(schedule.getEndTime().toLocalDateTime().toString())
                .build();
    }
}
