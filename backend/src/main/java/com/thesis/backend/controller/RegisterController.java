package com.thesis.backend.controller;

import com.thesis.backend.dto.Subject;
import com.thesis.backend.dto.SubjectTimetable;
import com.thesis.backend.dto.User;
import com.thesis.backend.dto.UserSubject;
import com.thesis.backend.repository.SubjectRepository;
import com.thesis.backend.repository.SubjectTimetableRepository;
import com.thesis.backend.repository.UserRepository;
import com.thesis.backend.repository.UserSubjectRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.validation.Valid;
import java.util.Optional;

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
        Optional<User> userExist = userRepository.findById(user.getId());
        if (userExist.isEmpty()) {
            userRepository.save(user);
            return ResponseEntity.ok().body("Successfully");
        } else {
            return ResponseEntity.badRequest().body("Error");
        }
    }


    @PostMapping("subject")
    public ResponseEntity<String> addNewSubject(@Valid @RequestBody Subject subject) {
        Optional<Subject> subjectExist = subjectRepository.findById(subject.getId());
        if (subjectExist.isPresent()) {
            logger.error(String.format("%s exists", subject));
            return ResponseEntity.badRequest().body("Already exists");
        } else {
            logger.info(String.format("%s created successfully", subject));
            subjectRepository.save(subject);
            return ResponseEntity.ok().body("Successfully");
        }
    }

    @PostMapping("timetable")
    public ResponseEntity<String> addNewSubjectTimetable(@Valid @RequestBody SubjectTimetable subjectTimetable) {
        Optional<Subject> subjectExist = subjectRepository.findById(subjectTimetable.getSubject().getId());
        if (subjectExist.isPresent()) {
            subjectTimetableRepository.save(subjectTimetable);
            logger.info("Insert new timetable successfully");
            return ResponseEntity.ok().body("Successfully");
        } else {
            return ResponseEntity.badRequest().body("Error");
        }
    }


    @PostMapping("user_subject")
    public ResponseEntity<String> addNewUserSubject(@Valid @RequestBody UserSubject userSubject) {
        Optional<Subject> checkSubjectExist = subjectRepository.findById(userSubject.getSubject().getId());
        Optional<User> checkUserExist = userRepository.findById(userSubject.getUser().getId());
        if (checkSubjectExist.isPresent() && checkUserExist.isPresent()) {
            logger.info(String.format("%s added", userSubject));
            userSubjectRepository.save(userSubject);
            return ResponseEntity.ok().body("Successfully");
        } else {
            return ResponseEntity.badRequest().body("Error");
        }
    }
}
