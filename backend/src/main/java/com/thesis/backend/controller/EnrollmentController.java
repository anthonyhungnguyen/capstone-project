package com.thesis.backend.controller;


import com.thesis.backend.dto.model.EnrollmentDto;
import com.thesis.backend.dto.model.SubjectDto;
import com.thesis.backend.dto.model.SubjectIDDto;
import com.thesis.backend.dto.model.UserDto;
import com.thesis.backend.service.EnrollmentServiceImpl;
import com.thesis.backend.service.SubjectServiceImpl;
import com.thesis.backend.service.UserServiceImpl;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import java.util.List;

@RestController(value = "Enrollment controller")
@RequestMapping(value = "/api/enroll", produces = MediaType.APPLICATION_JSON_VALUE)
@Tag(name = "Enrollment controller")
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

    @Operation(description = "Get all subjects enrolled by user based on user id")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "Success"),
            @ApiResponse(responseCode = "404", description = "Not found")
    })
    @GetMapping(value = "/user")
    public ResponseEntity<List<SubjectDto>> findAllSubjectsEnrolledByUser(@RequestParam(value = "userid") Integer userid) {
        return ResponseEntity.ok(enrollmentServiceImpl.findAllSubjectsTakenByUser(userid));
    }

    @Operation(description = "Get all users taking subject based on subject id")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "Success"),
            @ApiResponse(responseCode = "404", description = "Not found")
    })
    @GetMapping(value = "/subject")
    public ResponseEntity<List<UserDto>> findAllUsersTakeSubject(@Valid SubjectIDDto subjectIDDto) {
        return ResponseEntity.ok(enrollmentServiceImpl.findAllUsersTakeSubject(subjectIDDto));
    }

    @Operation(description = "Enroll subject for user based on user id and subject id")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "Success"),
            @ApiResponse(responseCode = "404", description = "Not found"),
            @ApiResponse(responseCode = "400", description = "Subject already enrolled")
    })
    @PostMapping
    public ResponseEntity<EnrollmentDto> enroll(@RequestBody @Valid EnrollmentDto enrollmentDto) {
        return ResponseEntity.ok(enrollmentServiceImpl.enroll(enrollmentDto));
    }

    @Operation(description = "Unregister subject for user based on user id and subject id")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "Success"),
            @ApiResponse(responseCode = "404", description = "Not found")
    })
    @DeleteMapping
    public ResponseEntity<String> unregister(@RequestBody @Valid EnrollmentDto enrollmentDto) {
        enrollmentServiceImpl.unregister(enrollmentDto);
        return ResponseEntity.ok("Success");
    }

}