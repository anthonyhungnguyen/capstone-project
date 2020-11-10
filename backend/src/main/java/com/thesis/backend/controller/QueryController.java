package com.thesis.backend.controller;

import com.thesis.backend.dto.CheckLog;
import com.thesis.backend.dto.Subject;
import com.thesis.backend.dto.User;
import com.thesis.backend.repository.CheckLogRepository;
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
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/query")
public class QueryController {
    private static final Logger logger = LoggerFactory.getLogger(QueryController.class);
    private final UserRepository userRepository;
    private final SubjectRepository subjectRepository;
    private final CheckLogRepository checkLogRepository;

    @Autowired
    public QueryController(UserRepository userRepository, SubjectRepository subjectRepository, CheckLogRepository checkLogRepository) {
        this.userRepository = userRepository;
        this.subjectRepository = subjectRepository;
        this.checkLogRepository = checkLogRepository;
    }

    @GetMapping("user/{id}/{semester}/enrollment")
    public ResponseEntity<List<Subject>> getEnrollmentsByUser(@PathVariable Integer id, @PathVariable int semester) {
        return userRepository.findById(id).map(user -> ResponseEntity.ok().body(user.getSubjects().stream().filter(x -> x.getSemester() == semester).collect(Collectors.toList()))).orElse(ResponseEntity.badRequest().body(null));
    }


    @GetMapping("/user/{id}")
    public ResponseEntity<User> getUser(@PathVariable Integer id) {
        return userRepository.findById(id).map(value -> ResponseEntity.ok().body(value)).orElse(ResponseEntity.badRequest().build());
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
