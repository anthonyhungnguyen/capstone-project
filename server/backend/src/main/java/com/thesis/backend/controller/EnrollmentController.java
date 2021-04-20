package com.thesis.backend.controller;


import com.thesis.backend.dto.model.EnrollmentDto;
import com.thesis.backend.dto.model.SubjectDto;
import com.thesis.backend.dto.model.SubjectIDDto;
import com.thesis.backend.dto.model.UserDto;
import com.thesis.backend.service.EnrollmentServiceImpl;
import com.thesis.backend.service.SubjectServiceImpl;
import com.thesis.backend.service.UserServiceImpl;
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
    private final SubjectServiceImpl subjectServiceImpl;
    private final UserServiceImpl userServiceImpl;
    private final EnrollmentServiceImpl enrollmentServiceImpl;

    @Autowired
    public EnrollmentController(SubjectServiceImpl subjectServiceImpl, UserServiceImpl userServiceImpl, EnrollmentServiceImpl enrollmentServiceImpl) {
        this.subjectServiceImpl = subjectServiceImpl;
        this.userServiceImpl = userServiceImpl;
        this.enrollmentServiceImpl = enrollmentServiceImpl;
    }

    public ResponseEntity<List<SubjectDto>> findAllSubjectsEnrolledByUser(@RequestParam(value = "userid") Integer userid) {
        return ResponseEntity.ok(enrollmentServiceImpl.findAllSubjectsTakenByUser(userid));
    }

    public ResponseEntity<List<UserDto>> findAllUsersTakeSubject(@Valid SubjectIDDto subjectIDDto) {
        return ResponseEntity.ok(enrollmentServiceImpl.findAllUsersTakeSubject(subjectIDDto));
    }

    @PostMapping
    public ResponseEntity<EnrollmentDto> enroll(@RequestBody @Valid EnrollmentDto enrollmentDto) {
        return ResponseEntity.ok(enrollmentServiceImpl.enroll(enrollmentDto));
    }

    @DeleteMapping
    public ResponseEntity<String> unregister(@RequestBody @Valid EnrollmentDto enrollmentDto) {
        enrollmentServiceImpl.unregister(enrollmentDto);
        return ResponseEntity.ok("Success");
    }
}
