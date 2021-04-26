package com.thesis.backend.controller;

import com.thesis.backend.service.TeacherService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

@RestController
@RequestMapping(value = "/api/teacher")
public class TeacherController {
    private final TeacherService teacherService;

    @Autowired
    public TeacherController(TeacherService teacherService) {
        this.teacherService = teacherService;
    }

    @GetMapping("/percentage")
    public ResponseEntity<Map<String, Float>> findAttendancePercentageByTeacherID(@RequestParam Integer teacherid) {
        return ResponseEntity.ok(teacherService.calculateAttendanceRate(teacherid));
    }
}
