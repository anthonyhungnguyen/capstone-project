package com.thesis.backend.service;

import com.thesis.backend.dto.request.AttendanceRequest;

public interface AttendanceService {

    void checkAttendanceUtil(AttendanceRequest request);

}
