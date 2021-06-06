package com.thesis.backend.controller;


import com.thesis.backend.dto.model.EnrollmentDto;
import com.thesis.backend.dto.model.SubjectDto;
import com.thesis.backend.dto.model.SubjectIDDto;
import com.thesis.backend.dto.model.UserDto;
import com.thesis.backend.service.EnrollmentService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import java.util.List;

@RestController(value = "Enrollment controller")
@RequestMapping(value = "/api/enroll", produces = MediaType.APPLICATION_JSON_VALUE)
@Slf4j
public class EnrollmentController {
    private final EnrollmentService enrollmentService;

    @Autowired
    public EnrollmentController(EnrollmentService enrollmentService) {
        this.enrollmentService = enrollmentService;
    }


    public ResponseEntity<List<SubjectDto>> findAllSubjectsEnrolledByUser(@RequestParam(value = "userid") Integer userid) {
        return ResponseEntity.ok(enrollmentService.findAllSubjectsTakenByUser(userid));
    }

    public ResponseEntity<List<UserDto>> findAllUsersTakeSubject(@Valid SubjectIDDto subjectIDDto) {
        return ResponseEntity.ok(enrollmentService.findAllUsersTakeSubject(subjectIDDto));
    }

    @PostMapping
    public ResponseEntity<EnrollmentDto> enroll(@RequestBody @Valid EnrollmentDto enrollmentDto) {
        return ResponseEntity.ok(enrollmentService.enroll(enrollmentDto));
    }
}
