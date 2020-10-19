package com.thesis.backend.controller;

import com.thesis.backend.dto.Subject;
import com.thesis.backend.dto.SubjectTimetable;
import com.thesis.backend.dto.User;
import com.thesis.backend.dto.UserSubject;
import com.thesis.backend.repository.SubjectRepository;
import com.thesis.backend.repository.SubjectTimetableRepository;
import com.thesis.backend.repository.UserRepository;
import com.thesis.backend.repository.UserSubjectRepository;
import org.apache.coyote.Response;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.validation.Valid;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;

@RestController
@RequestMapping("/api/register")
@Validated
public class RegisterController {
    private static final Logger logger = LoggerFactory.getLogger(RegisterController.class);
    private final UserRepository userRepository;
    private final SubjectRepository subjectRepository;
    private final UserSubjectRepository userSubjectRepository;
    private final SubjectTimetableRepository subjectTimetableRepository;

    @Autowired
    public RegisterController(UserRepository userRepository, SubjectRepository subjectRepository, UserSubjectRepository userSubjectRepository, SubjectTimetableRepository subjectTimetableRepository) {
        this.userRepository = userRepository;
        this.subjectRepository = subjectRepository;
        this.userSubjectRepository = userSubjectRepository;
        this.subjectTimetableRepository = subjectTimetableRepository;
    }

    @PostMapping("user")
    public ResponseEntity<String> addNewUser(@Valid @RequestBody User user) {
        if (userRepository.existsById(user.getId())) {
            logger.error(String.format("%s exists", user));
            return new ResponseEntity<>("User already exists", HttpStatus.BAD_REQUEST);
        } else {
            logger.info(String.format("%s created successfully", user));
            userRepository.save(user);
            return new ResponseEntity<>("User created successfully", HttpStatus.OK);
        }
    }

    @PostMapping("subject")
    public ResponseEntity<String> addNewSubject(@Valid @RequestBody Subject subject) {
        if (subjectRepository.existsById(subject.getId())) {
            logger.error(String.format("%s exists", subject));
            return new ResponseEntity<>("Subject already exists", HttpStatus.BAD_REQUEST);
        } else {
            logger.info(String.format("%s created successfully", subject));
            subjectRepository.save(subject);
            return new ResponseEntity<>("Subject created successfully", HttpStatus.OK);
        }
    }

    @PostMapping("subject/timetable")
    public ResponseEntity<String> addNewSubjectTimetable(@Valid @RequestBody SubjectTimetable subjectTimetable) {
        try {
            subjectTimetableRepository.save(subjectTimetable);
            logger.info("Insert new timetable successfully");
            return ResponseEntity.ok().body("Insert new timetable successfully");
        } catch (DataIntegrityViolationException ex) {
            throw new DataIntegrityViolationException(String.format("SubjectID: %s not found", subjectTimetable.getSubject_id()));
        } 
    }

    @PostMapping("user_subject")
    public ResponseEntity<String> addNewUserSubject(@Valid @RequestBody UserSubject userSubject) {
        try {
            logger.info(String.format("%s added", userSubject));
            userSubjectRepository.save(userSubject);
            return new ResponseEntity<>(String.format("%s added", userSubject), HttpStatus.OK);
        } catch (DataIntegrityViolationException ex) {
            throw new DataIntegrityViolationException(String.format("SubjectId: %s or UserID: %s not found", userSubject.getSubject().getId(), userSubject.getUser().getId()));
        }
    }
}
