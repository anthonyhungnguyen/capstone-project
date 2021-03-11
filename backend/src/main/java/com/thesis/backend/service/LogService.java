package com.thesis.backend.service;

import com.thesis.backend.dto.model.EnrollmentDto;
import com.thesis.backend.dto.model.LogDto;
import com.thesis.backend.dto.model.SubjectIDDto;
import com.thesis.backend.dto.request.AttendanceRequest;
import com.thesis.backend.model.Log;

import java.time.LocalTime;
import java.util.List;

public interface LogService {

    List<LogDto> findAllLogsBasedOnUserId(Integer userid);

    List<LogDto> findAllLogsBasedOnSubjectId(SubjectIDDto subjectIDDto);

    List<LogDto> findAllLogsInTimeRange(EnrollmentDto enrollmentDto,
                                        LocalTime start,
                                        LocalTime end);

    Log saveAttendance(AttendanceRequest request);
}
