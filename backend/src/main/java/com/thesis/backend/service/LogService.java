package com.thesis.backend.service;

import com.thesis.backend.dto.model.EnrollmentDto;
import com.thesis.backend.dto.model.LogDto;
import com.thesis.backend.dto.model.SubjectIDDto;

import java.time.LocalTime;
import java.util.List;

public interface LogService {

    List<LogDto> findAllLogsBasedOnUserId(Integer userid);

    List<LogDto> findAllLogsBasedOnSubjectId(SubjectIDDto subjectIDDto);

    List<LogDto> findAllLogsInTimeRange(EnrollmentDto enrollmentDto,
                                        LocalTime start,
                                        LocalTime end);

    LogDto save(EnrollmentDto enrollmentDto);
}
