package com.thesis.backend.controller;

import com.thesis.backend.dto.CheckLog;
import com.thesis.backend.dto.Enrollment;
import com.thesis.backend.dto.Subject;
import com.thesis.backend.dto.User;
import com.thesis.backend.repository.CheckLogRepository;
import com.thesis.backend.repository.EnrollmentRepository;
import com.thesis.backend.repository.SubjectRepository;
import com.thesis.backend.repository.UserRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/query")
public class QueryController {
    private static final Logger logger = LoggerFactory.getLogger(QueryController.class);
    private final UserRepository userRepository;
    private final SubjectRepository subjectRepository;
    private final EnrollmentRepository enrollmentRepository;
    private final CheckLogRepository checkLogRepository;

    @Autowired
    public QueryController(UserRepository userRepository, SubjectRepository subjectRepository, EnrollmentRepository enrollmentRepository, CheckLogRepository checkLogRepository, SubjectTimetableRepository subjectTimetableRepository) {
        this.userRepository = userRepository;
        this.subjectRepository = subjectRepository;
        this.enrollmentRepository = enrollmentRepository;
        this.checkLogRepository = checkLogRepository;
    }


    @GetMapping("/user/{id}")
    public ResponseEntity<User> getUser(@PathVariable String id) {
        Optional<User> user = userRepository.findById(id);
        return user.map(value -> ResponseEntity.ok().body(value)).orElse(ResponseEntity.badRequest().build());
    }

    @GetMapping("/subject/{id}/{semester}")
    public ResponseEntity<List<Subject>> getSubject(@PathVariable String id, @PathVariable int semester)  {
        Optional<List<Subject>> subjectByIdAndSemester = Optional.ofNullable(subjectRepository.findSubjectByIdAndSemester(id, semester));
        return subjectByIdAndSemester.map(subjects -> ResponseEntity.ok().body(subjects)).orElseGet(() -> ResponseEntity.badRequest().body(null));
    }


    @GetMapping("/enrollment/user/{id}/{semester}")
    public ResponseEntity<List<Subject>> getSubjectsEnrolledByUser(@PathVariable int id, @PathVariable int semester) {
        Optional<List<Enrollment>> subjectsTakenByUser = Optional.ofNullable(enrollmentRepository.findEnrollmentsByUserIdAndSemester(id, semester));
        if (subjectsTakenByUser.isPresent()) {
            List<Subject> subjectList = subjectsTakenByUser.get().stream().map(Enrollment::getSubject).collect(Collectors.toList());
            return ResponseEntity.ok().body(subjectList);
        } else {
            return ResponseEntity.badRequest().body(null);
        }
    }

    @GetMapping("/user/{id}/log")
    public List<CheckLog> getAttendanceLogs(@PathVariable String id) {
        return checkLogRepository.findAllByStudentID(id);
    }

    @GetMapping("/subjects/{semester}")
    public ResponseEntity<List<Subject>> getTimetables(@PathVariable int semester) {
        List<Subject> subjectsBySemester = subjectRepository.findSubjectsBySemester(semester);
        return ResponseEntity.ok().body(subjectsBySemester);
    }
}
