package com.thesis.backend.service;

import com.thesis.backend.dto.model.EnrollmentDto;
import com.thesis.backend.dto.model.LogDto;

public interface AttendanceService {
    LogDto checkAttendance(EnrollmentDto enrollmentDto);
}
