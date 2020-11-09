package com.thesis.backend.service;

import com.thesis.backend.dto.Enrollment;
import com.thesis.backend.repository.CheckLogRepository;
import com.thesis.backend.repository.EnrollmentRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
public class CheckAttendanceService {
    private final CheckLogRepository checkLogRepository;
    private final EnrollmentRepository enrollmentRepository;

    @Autowired
    public CheckAttendanceService(CheckLogRepository checkLogRepository, EnrollmentRepository enrollmentRepository) {
        this.checkLogRepository = checkLogRepository;
        this.enrollmentRepository = enrollmentRepository;
    }

    public boolean checkUserInSubject(String userID, String subjectID) {
        Optional<List<Enrollment>> subjectsTakenByUsers = Optional.ofNullable(enrollmentRepository.findUserSubjectsByUser_Id(userID));
        if (subjectsTakenByUsers.isPresent()) {
            List<String> subjectList = subjectsTakenByUsers.get().stream().map(us -> us.getSubject().getId()).collect(Collectors.toList());
            return subjectList.contains(subjectID);
        } else {
            return false;
        }
    }
}
