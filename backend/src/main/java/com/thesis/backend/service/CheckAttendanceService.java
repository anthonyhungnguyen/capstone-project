package com.thesis.backend.service;

import com.thesis.backend.dto.UserSubject;
import com.thesis.backend.repository.CheckLogRepository;
import com.thesis.backend.repository.UserSubjectRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class CheckAttendanceService {
    private final CheckLogRepository checkLogRepository;
    private final UserSubjectRepository userSubjectRepository;

    @Autowired
    public CheckAttendanceService(CheckLogRepository checkLogRepository, UserSubjectRepository userSubjectRepository) {
        this.checkLogRepository = checkLogRepository;
        this.userSubjectRepository = userSubjectRepository;
    }

    public boolean checkUserInSubject(String userID, String subjectID) {
        List<String> subjectsTakenByUsers = userSubjectRepository.getSubjectsFromUserId(userID);
        return subjectsTakenByUsers.contains(subjectID);
    }
}
