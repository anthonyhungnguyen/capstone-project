package com.thesis.backend.controller;

import com.thesis.backend.dto.Subject;
import com.thesis.backend.dto.SubjectId;
import com.thesis.backend.dto.User;
import com.thesis.backend.repository.SubjectRepository;
import com.thesis.backend.repository.UserRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import java.util.Optional;

@RestController
@RequestMapping("/api/register")
@Validated
public class RegisterController {
    private static final Logger logger = LoggerFactory.getLogger(RegisterController.class);
    private final UserRepository userRepository;
    private final SubjectRepository subjectRepository;

    @Autowired
    public RegisterController(UserRepository userRepository, SubjectRepository subjectRepository) {
        this.userRepository = userRepository;
        this.subjectRepository = subjectRepository;
    }

    @PostMapping("user")
    public ResponseEntity<String> addUser(@Valid @RequestBody User user) {
        if (userRepository.existsById(user.getId())) {
            return ResponseEntity.badRequest().body("Fail");
        } else {
            userRepository.save(user);
            return ResponseEntity.ok().body("Successfully");
        }
    }

    @PostMapping("subject")
    public ResponseEntity<String> addSubject(@Valid @RequestBody Subject subject) {
        if (subjectRepository.existsById(new SubjectId(subject.getId(), subject.getGroupCode(), subject.getSemester()))) {
            return ResponseEntity.badRequest().body("Fail");
        } else {
            subjectRepository.save(subject);
            return ResponseEntity.ok().body("Successfully");
        }
    }

    @PostMapping("enrollment/{id}")
    public ResponseEntity<String> addEnrollment(@PathVariable int id, @Valid @RequestBody Subject subject) {
        Optional<User> existingUser = userRepository.findById(id);
        Optional<Subject> existingSubject = subjectRepository.findById(new SubjectId(subject.getId(), subject.getGroupCode(), subject.getSemester()));
        if (existingUser.isEmpty()) {
            return ResponseEntity.badRequest().body("User not found");
        } else if (existingSubject.isEmpty()) {
            return ResponseEntity.badRequest().body("Subject not found");
        } else if (existingUser.get().getSubjects().contains(existingSubject.get())) {
            return ResponseEntity.badRequest().body("Subject is already existed");
        } else {
            existingUser.get().getSubjects().add(existingSubject.get());
            userRepository.save(existingUser.get());
            return ResponseEntity.ok().body("Successfully");
        }
    }

////    @PostMapping("enrollment")
////    public ResponseEntity<String> addNewSubjectTimetable(@Valid @RequestBody Enrollment enrollment) {
////        boolean existingUser = userRepository.existsById(enrollment.getUserId());
////        boolean existingSubject = subjectRepository.existsByIdAndGroupCodeAndSemester(enrollment.getSubjectId(), enrollment.getGroupCode(), enrollment.getSemester());
////        boolean existingEnrollment = enrollmentRepository.existsByUserIdAndSubjectIdAndGroupCodeAndSemester(enrollment.getUserId(), enrollment.getSubjectId(), enrollment.getGroupCode(), enrollment.getSemester());
////        if (!existingSubject) {
////            return ResponseEntity.badRequest().body("Subject not found");
////        }
////        if (!existingUser) {
////            return ResponseEntity.badRequest().body("User not found");
////        }
////        if (existingEnrollment) {
////            return ResponseEntity.badRequest().body("Duplicated enrollment");
////        } else {
////            enrollmentRepository.save(enrollment);
////            return ResponseEntity.ok().body("Successfully");
////        }
////
////    }
//
//
//    @PostMapping("user_subject")
//    public ResponseEntity<String> addNewUserSubject(@Valid @RequestBody Enrollment enrollment) {
//        Optional<Subject> checkSubjectExist = subjectRepository.findById(enrollment.getSubject().getId());
//        Optional<User> checkUserExist = userRepository.findById(enrollment.getUser().getId());
//        if (checkSubjectExist.isPresent() && checkUserExist.isPresent()) {
//            logger.info(String.format("%s added", enrollment));
//            enrollmentRepository.save(enrollment);
//            return ResponseEntity.ok().body("Successfully");
//        } else {
//            return ResponseEntity.badRequest().body("Error");
//        }
//    }
}
