package com.thesis.backend.service;

import com.thesis.backend.repository.CheckLogRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class CheckAttendanceService {
    private final CheckLogRepository checkLogRepository;

    @Autowired
    public CheckAttendanceService(CheckLogRepository checkLogRepository) {
        this.checkLogRepository = checkLogRepository;
    }

//    public boolean checkUserInSubject(String userID, String subjectID) {
//        Optional<List<Enrollment>> subjectsTakenByUsers = Optional.ofNullable(enrollmentRepository.findUserSubjectsByUser_Id(userID));
//        if (subjectsTakenByUsers.isPresent()) {
//            List<String> subjectList = subjectsTakenByUsers.get().stream().map(us -> us.getSubject().getId()).collect(Collectors.toList());
//            return subjectList.contains(subjectID);
//        } else {
//            return false;
//        }
//    }
}
