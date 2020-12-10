package com.thesis.backend.service;

import com.thesis.backend.dto.*;
import com.thesis.backend.repository.CheckLogRepository;
import com.thesis.backend.repository.SubjectRepository;
import com.thesis.backend.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class CheckAttendanceService {
    private final UserRepository userRepository;
    private final CheckLogRepository checkLogRepository;
    private final SubjectRepository subjectRepository;

    @Autowired
    public CheckAttendanceService(UserRepository userRepository, CheckLogRepository checkLogRepository, SubjectRepository subjectRepository) {
        this.checkLogRepository = checkLogRepository;
        this.userRepository = userRepository;
        this.subjectRepository = subjectRepository;
    }

    public Message checkUserInSubject(int userID, SubjectId subject) {
        Optional<User> existingUser = userRepository.findById(userID);
        Optional<Subject> existingSubject = subjectRepository.findById(new SubjectId(subject.getId(), subject.getGroupCode(), subject.getSemester()));
        if (existingUser.isEmpty()) {
            return Message.builder().status(false).message("User not found").build();
        }
        else if (existingSubject.isEmpty()) {
            return Message.builder().status(false).message("Subject not found").build();
        } else {
            CheckLog checkLog = new CheckLog(userID, subject.getSemester(), subject.getGroupCode(), subject.getId(), "check-in");
            checkLogRepository.save(checkLog);
            return Message.builder().status(true).message(checkLog.toString()).build();
        }
    }
}
