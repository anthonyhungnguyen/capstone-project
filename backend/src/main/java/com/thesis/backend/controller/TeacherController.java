package com.thesis.backend.controller;

import com.thesis.backend.dto.request.ScheduleRequest;
import com.thesis.backend.service.AutomationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.validation.Valid;
import java.io.IOException;

@RestController
@RequestMapping(value = "/api/teacher")
public class TeacherController {

    private final AutomationService teacherService;

    @Autowired
    public TeacherController(AutomationService teacherService) {
        this.teacherService = teacherService;
    }

    @PostMapping
    public ResponseEntity<Boolean> register(@Valid @RequestBody ScheduleRequest scheduleRequest) throws IOException {
        return ResponseEntity.ok(teacherService.registerSchedule(scheduleRequest));
    }
}
