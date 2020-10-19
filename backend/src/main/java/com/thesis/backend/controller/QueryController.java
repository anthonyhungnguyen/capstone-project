package com.thesis.backend.controller;

import com.thesis.backend.dto.Subject;
import com.thesis.backend.dto.User;
import com.thesis.backend.repository.SubjectRepository;
import com.thesis.backend.repository.UserRepository;
import com.thesis.backend.repository.UserSubjectRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/query")
public class QueryController {
    private static final Logger logger = LoggerFactory.getLogger(QueryController.class);
    private final UserRepository userRepository;
    private final SubjectRepository subjectRepository;
    private final UserSubjectRepository userSubjectRepository;

    @Autowired
    public QueryController(UserRepository userRepository, SubjectRepository subjectRepository, UserSubjectRepository userSubjectRepository) {
        this.userRepository = userRepository;
        this.subjectRepository = subjectRepository;
        this.userSubjectRepository = userSubjectRepository;
    }

    @GetMapping("/user/{id}")
    public Optional<User> getUser(@PathVariable String id) {
        return userRepository.findById(id);
    }

    @GetMapping("/subject/{id}")
    public Optional<Subject> getSubject(@PathVariable String id) {
        return subjectRepository.findById(id);
    }

    @GetMapping("/user_subject/user/{id}")
    public List<String> getSubjectsTakenByUser(@PathVariable String id) {
        return userSubjectRepository.getSubjectsFromUserId(id);
    }
}
