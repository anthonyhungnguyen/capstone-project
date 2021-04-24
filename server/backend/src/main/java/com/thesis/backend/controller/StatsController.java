package com.thesis.backend.controller;

import com.thesis.backend.dto.model.SubjectIDDto;
import com.thesis.backend.service.StatsService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

@RestController
@RequestMapping(value = "/api/stats")
public class StatsController {
    private final StatsService statsService;

    @Autowired
    public StatsController(StatsService statsService) {
        this.statsService = statsService;
    }

    @GetMapping("/teacher/percentage")
    public ResponseEntity<Map<String, Float>> findAttendancePercentageByTeacherID(@RequestParam Integer teacherid) {
        return ResponseEntity.ok(statsService.calculateAttendanceRate(teacherid));
    }
}
