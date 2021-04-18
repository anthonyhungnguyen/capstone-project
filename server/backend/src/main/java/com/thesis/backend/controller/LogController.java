package com.thesis.backend.controller;

import com.thesis.backend.model.Log;
import com.thesis.backend.service.LogService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping(value = "/api/log")
public class LogController {
    private final LogService logService;

    @Autowired
    public LogController(LogService logService) {
        this.logService = logService;
    }

    @GetMapping("/user")
    public ResponseEntity<List<Log>> queryBasedOnUserid(@RequestParam Integer userid) {
        return ResponseEntity.ok(logService.findLogsBasedOnUserID(userid));
    }
}
