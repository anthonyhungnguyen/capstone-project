package com.thesis.backend.controller;

import com.thesis.backend.dto.Enrollment;
import com.thesis.backend.dto.Subject;
import com.thesis.backend.dto.User;
import com.thesis.backend.repository.EnrollmentRepository;
import com.thesis.backend.repository.SubjectRepository;
import com.thesis.backend.repository.UserRepository;
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
    private final EnrollmentRepository enrollmentRepository;

    @Autowired
    public RegisterController(UserRepository userRepository, SubjectRepository subjectRepository, EnrollmentRepository enrollmentRepository) {
        this.userRepository = userRepository;
        this.subjectRepository = subjectRepository;
        this.enrollmentRepository = enrollmentRepository;
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
            return ResponseEntity.badRequest().body("Already exists");
        } else {
            subjectRepository.save(subject);
            return ResponseEntity.ok().body("Successfully");
        }
    }

    @PostMapping("enrollment")
    public ResponseEntity<String> addNewSubjectTimetable(@Valid @RequestBody Enrollment enrollment) {
        boolean existingUser = userRepository.existsById(enrollment.getUserId());
        boolean existingSubject = subjectRepository.existsByIdAndGroupCodeAndSemester(enrollment.getSubjectId(), enrollment.getGroupCode(), enrollment.getSemester());
        boolean existingEnrollment = enrollmentRepository.existsByUserIdAndSubjectIdAndGroupCodeAndSemester(enrollment.getUserId(), enrollment.getSubjectId(), enrollment.getGroupCode(), enrollment.getSemester());
        if (!existingSubject) {
            return ResponseEntity.badRequest().body("Subject not found");
        }
        if (!existingUser) {
            return ResponseEntity.badRequest().body("User not found");
        }
        if (existingEnrollment) {
            return ResponseEntity.badRequest().body("Duplicated enrollment");
        } else {
            enrollmentRepository.save(enrollment);
            return ResponseEntity.ok().body("Successfully");
        }

    }


    @PostMapping("user_subject")
    public ResponseEntity<String> addNewUserSubject(@Valid @RequestBody Enrollment enrollment) {
        Optional<Subject> checkSubjectExist = subjectRepository.findById(enrollment.getSubject().getId());
        Optional<User> checkUserExist = userRepository.findById(enrollment.getUser().getId());
        if (checkSubjectExist.isPresent() && checkUserExist.isPresent()) {
            logger.info(String.format("%s added", enrollment));
            enrollmentRepository.save(enrollment);
            return ResponseEntity.ok().body("Successfully");
        } else {
            return ResponseEntity.badRequest().body("Error");
        }
    }
}
