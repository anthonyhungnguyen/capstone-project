package com.thesis.backend.service;

import com.thesis.backend.dto.Subject;
import com.thesis.backend.dto.UserSubject;
import com.thesis.backend.repository.CheckLogRepository;
import com.thesis.backend.repository.UserSubjectRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

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
        Optional<List<UserSubject>> subjectsTakenByUsers = Optional.ofNullable(userSubjectRepository.findUserSubjectsByUser_Id(userID));
        if (subjectsTakenByUsers.isPresent()) {
            List<String> subjectList = subjectsTakenByUsers.get().stream().map(us -> us.getSubject().getId()).collect(Collectors.toList());
            return subjectList.contains(subjectID);
        } else {
            return false;
        }
    }
}
