package com.thesis.backend.controller;

import com.thesis.backend.dto.request.ScheduleRequest;
import com.thesis.backend.service.ScheduleService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import java.io.IOException;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping(value = "/api/teacher")
public class ScheduleController {

    private final ScheduleService teacherService;
    private final ScheduleService scheduleService;

    @Autowired
    public ScheduleController(ScheduleService teacherService, ScheduleService scheduleService) {
        this.teacherService = teacherService;
        this.scheduleService = scheduleService;
    }

    @PostMapping
    public ResponseEntity<String> register(@Valid @RequestBody ScheduleRequest scheduleRequest) throws IOException {
        return ResponseEntity.ok(teacherService.registerSchedule(scheduleRequest));
    }

    @PutMapping
    public ResponseEntity<ScheduleRequest> update(@Valid @RequestBody ScheduleRequest scheduleRequest) {
        return ResponseEntity.ok(scheduleService.updateSchedule(scheduleRequest));
    }

    @DeleteMapping
    public ResponseEntity<String> delete(@Valid @RequestBody ScheduleRequest scheduleRequest) {
        scheduleService.deleteSchedule(scheduleRequest);
        return ResponseEntity.ok("Delete successfully!");
    }

    @GetMapping("/schedules")
    public ResponseEntity<List<ScheduleRequest>> fetch(@RequestParam int teacherid) {
        return ResponseEntity.ok(scheduleService.fetch(teacherid));
    }
}
