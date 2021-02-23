package com.thesis.backend.controller;

import com.thesis.backend.dto.model.EnrollmentDto;
import com.thesis.backend.dto.model.LogDto;
import com.thesis.backend.model.Log;
import com.thesis.backend.service.AttendanceServiceImpl;
import com.thesis.backend.service.EnrollmentServiceImpl;
import io.swagger.annotations.Api;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import java.util.List;

@RestController(value = "Attendance controller")
@RequestMapping(value = "/api/attendance", produces = MediaType.APPLICATION_JSON_VALUE)
@Slf4j
public class AttendanceController {
    private final AttendanceServiceImpl attendanceService;

    @Autowired
    public AttendanceController(AttendanceServiceImpl attendanceService) {
        this.attendanceService = attendanceService;
    }

    @Operation(description = "Check attendance based on user id and subject id")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "Success"),
            @ApiResponse(responseCode = "404", description = "Not found"),
            @ApiResponse(responseCode = "400", description = "Fail")
    })
    @PostMapping
    public ResponseEntity<LogDto> check(@Valid EnrollmentDto enrollmentDto) {
        return ResponseEntity.ok(attendanceService.checkAttendance(enrollmentDto));
    }


}
