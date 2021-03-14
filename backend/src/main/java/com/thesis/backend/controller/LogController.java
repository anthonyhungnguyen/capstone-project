package com.thesis.backend.controller;

import com.thesis.backend.dto.model.SubjectIDDto;
import com.thesis.backend.dto.request.AttendanceRequest;
import com.thesis.backend.service.LogService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
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


    @Operation(description = "Query logs based on user id")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "Success"),
            @ApiResponse(responseCode = "404", description = "Fail")
    })
    @GetMapping("/user")
    public ResponseEntity<List<AttendanceRequest>> queryBasedOnUserid(@RequestParam Integer userid) {
        return ResponseEntity.ok(logService.findAllLogsBasedOnUserId(userid));
    }

    @Operation(description = "Query logs based on subject id")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "Success"),
            @ApiResponse(responseCode = "404", description = "Fail")
    })
    @GetMapping("/subject")
    public ResponseEntity<List<AttendanceRequest>> queryBasedOnSubjectid(@RequestParam String subjectId,
                                                              @RequestParam String groupCode,
                                                              @RequestParam int semester) {
        return ResponseEntity.ok(logService.findAllLogsBasedOnSubjectId(new SubjectIDDto(subjectId, groupCode, semester)));
    }
}
