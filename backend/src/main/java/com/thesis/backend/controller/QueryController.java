package com.thesis.backend.controller;

import com.thesis.backend.dto.*;
import com.thesis.backend.repository.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.*;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/query")
public class QueryController {
    private static final Logger logger = LoggerFactory.getLogger(QueryController.class);
    private final UserRepository userRepository;
    private final SubjectRepository subjectRepository;
    private final UserSubjectRepository userSubjectRepository;
    private final CheckLogRepository checkLogRepository;
    private final SubjectTimetableRepository subjectTimetableRepository;

    @Autowired
    public QueryController(UserRepository userRepository, SubjectRepository subjectRepository, UserSubjectRepository userSubjectRepository, CheckLogRepository checkLogRepository, SubjectTimetableRepository subjectTimetableRepository) {
        this.userRepository = userRepository;
        this.subjectRepository = subjectRepository;
        this.userSubjectRepository = userSubjectRepository;
        this.checkLogRepository = checkLogRepository;
        this.subjectTimetableRepository = subjectTimetableRepository;
    }



    @GetMapping("/user/{id}")
    public ResponseEntity<User> getUser(@PathVariable String id) {
        Optional<User> user =  userRepository.findById(id);
        return user.map(value -> ResponseEntity.ok().body(value)).orElse(ResponseEntity.badRequest().build());
    }

    @GetMapping("/subject/{id}")
    public ResponseEntity<Subject> getSubject(@PathVariable String id) {
        return subjectRepository.findById(id).map(subject -> ResponseEntity.ok().body(subject)).orElse(ResponseEntity.badRequest().build());
    }


    @GetMapping("/user_subject/user/{id}")
    public ResponseEntity<List<Subject>> getSubjectsTakenByUser(@PathVariable String id) {
        Optional<List<UserSubject>> subjectsTakenByUser = Optional.ofNullable(userSubjectRepository.findUserSubjectsByUser_Id(id));
        if (subjectsTakenByUser.isPresent()) {
            List<Subject> subjectList = subjectsTakenByUser.get().stream().map(UserSubject::getSubject).collect(Collectors.toList());
            return ResponseEntity.ok().body(subjectList);
        } else {
            return ResponseEntity.badRequest().body(null);
        }
    }

    @GetMapping("/user/{id}/log")
    public List<CheckLog> getAttendanceLogs(@PathVariable String id) {
        return checkLogRepository.findAllByStudentID(id);
    }

    @GetMapping("/subjects")
    public ResponseEntity<List<Map<String, Object>>> getAllSubjectsTimetable() {
        List<SubjectTimetable> subjectTimetableList = subjectTimetableRepository.findAll();
        List<Map<String, Object>> formattedSubjectTimetables = subjectTimetableList.stream().map(st -> {
            Map<String, Object> newItem = new HashMap<>();
            newItem.put("key", st.getId());
            newItem.put("subjectID", st.getSubject().getId());
            newItem.put("subjectName", st.getSubject().getName());
            newItem.put("startTime", st.getStart_time());
            newItem.put("endTime", st.getEnd_time());
            newItem.put("weekDay", st.getDay_in_week());
            return newItem;
        }).collect(Collectors.toList());

        return ResponseEntity.ok().body(formattedSubjectTimetables);
    }
}
