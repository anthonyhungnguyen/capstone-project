package com.thesis.backend.controller;

import com.thesis.backend.service.CheckAttendanceService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping(value = "/api", produces = MediaType.APPLICATION_JSON_VALUE)
@Slf4j
public class CheckAttendanceController {
    private final CheckAttendanceService checkAttendanceService;

    @Autowired
    public CheckAttendanceController(CheckAttendanceService checkAttendanceService) {
        this.checkAttendanceService = checkAttendanceService;
    }

//    @PostMapping("check/{id}")
//    public ResponseEntity<String> requestCheckAttendance(@PathVariable int id, @Valid @RequestBody SubjectId subject) {
//        Message message = checkAttendanceService.checkUserInSubject(id, subject);
//        if (message.isStatus()) {
//            return ResponseEntity.ok().body(message.getMessage());
//        } else {
//            return ResponseEntity.badRequest().body(message.getMessage());
//        }
//    }
}
