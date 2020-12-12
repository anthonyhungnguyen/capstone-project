package com.thesis.backend.controller;

import com.thesis.backend.dto.CheckLog;
import com.thesis.backend.dto.Message;
import com.thesis.backend.dto.SubjectId;
import com.thesis.backend.repository.CheckLogRepository;
import com.thesis.backend.service.CheckAttendanceService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;

@RestController
@RequestMapping("/api")
public class CheckAttendanceController {
    private final Logger logger = LoggerFactory.getLogger(CheckAttendanceController.class);
    private final CheckAttendanceService checkAttendanceService;

    @Autowired
    public CheckAttendanceController(CheckAttendanceService checkAttendanceService) {
        this.checkAttendanceService = checkAttendanceService;
    }

    @PostMapping("check/{id}")
    public ResponseEntity<String> requestCheckAttendance(@PathVariable int id, @Valid @RequestBody SubjectId subject) {
        Message message = checkAttendanceService.checkUserInSubject(id, subject);
        if (message.isStatus()) {
            return ResponseEntity.ok().body(message.getMessage());
        } else {
            return ResponseEntity.badRequest().body(message.getMessage());
        }
    }
}
