package com.thesis.backend.controller;

import com.thesis.backend.repository.CheckLogRepository;
import com.thesis.backend.service.CheckAttendanceService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
public class CheckAttendanceController {
    private final Logger logger = LoggerFactory.getLogger(CheckAttendanceController.class);
    private final CheckLogRepository checkLogRepository;
    private final CheckAttendanceService checkAttendanceService;

    public CheckAttendanceController(CheckLogRepository checkLogRepository, CheckAttendanceService checkAttendanceService) {
        this.checkLogRepository = checkLogRepository;
        this.checkAttendanceService = checkAttendanceService;
    }

//    @PostMapping("check")
//    public ResponseEntity<String> requestCheckLog(@Valid @RequestBody CheckLog checkLog) {
//        boolean checkUserInSubject = checkAttendanceService.checkUserInSubject(checkLog.getStudentID(), checkLog.getSubjectID());
//        if (checkUserInSubject) {
//            try {
//                checkLogRepository.save(checkLog);
//                logger.info("Successfully check-in " + checkLog);
//                return ResponseEntity.status(HttpStatus.ACCEPTED).body("Successfully checking attendance");
//            } catch (Exception e) {
//                logger.error("Error when check-in " + checkLog);
//                return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Error when checking attendance");
//            }
//        } else {
//            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("User does not taken this subject");
//        }
//    }
}
