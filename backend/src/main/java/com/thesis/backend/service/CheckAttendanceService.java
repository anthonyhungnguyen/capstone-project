package com.thesis.backend.service;

import com.thesis.backend.dto.*;
import com.thesis.backend.repository.CheckLogRepository;
import com.thesis.backend.repository.SubjectRepository;
import com.thesis.backend.repository.UserRepository;
import org.apache.tomcat.jni.Local;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.*;
import java.time.temporal.TemporalAdjuster;
import java.time.temporal.WeekFields;
import java.util.*;
import java.util.stream.Collectors;

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
            int weekOfYear = getWeekOfYear();
            boolean isCurrentWeekInWeekLearn = checkCurrentWeekInWeekLearn(weekOfYear, existingSubject.get().getWeekLearn());
            boolean isCurrentDayInWeekAvailable = checkCurrentDayInWeekAvailable(existingSubject.get().getWeekDay());
            boolean isSubjectAvailable = checkSubjectAvailable(existingSubject.get());
            if (isCurrentWeekInWeekLearn && isCurrentDayInWeekAvailable && isSubjectAvailable) {
                boolean haveStudentCheckedIn = haveStudentCheckedInYet(userID, existingSubject.get());
                if(!haveStudentCheckedIn) {
                    CheckLog checkLog = new CheckLog(userID, subject.getSemester(), subject.getGroupCode(), subject.getId(), "check-in");
                    checkLogRepository.save(checkLog);
                    return Message.builder().status(true).message(checkLog.toString()).build();
                } else {
                    return Message.builder().status(false).message("You have checked-in").build();
                }
            } else {
                return Message.builder().status(false).message("Subject is not available to check-in").build();
            }
        }
    }

    private boolean checkSubjectAvailable(Subject subject) {
        String rawTimeRange = subject.getTimeRange();
        List<String> rawTimeRangeSplit = Arrays.asList(rawTimeRange.split("-", 0).clone());
        LocalTime startTime = LocalTime.parse(rawTimeRangeSplit.get(0).trim());
        LocalTime endTime = LocalTime.parse(rawTimeRangeSplit.get(1).trim());
        LocalTime currentTime = getLocalTime();
        return startTime.isBefore(currentTime) && endTime.isAfter(currentTime);
    }

    private boolean haveStudentCheckedInYet(int userID, Subject subject) {
        String rawTimeRange = subject.getTimeRange();
        List<String> rawTimeRangeSplit = Arrays.asList(rawTimeRange.split("-", 0).clone());
        LocalTime startTime = LocalTime.parse(rawTimeRangeSplit.get(0).trim());
        LocalTime endTime = LocalTime.parse(rawTimeRangeSplit.get(1).trim());
        List<CheckLog> checkStudentLog = checkLogRepository.findByStudentIDAndSemesterAndGroupCodeAndSubjectID(userID, subject.getSemester(), subject.getGroupCode(), subject.getId());
        if (checkStudentLog.size() > 0) {
            LocalDateTime startDateTime = LocalDateTime.now().with(startTime);
            LocalDateTime endDateTime = LocalDateTime.now().with(endTime);
            List<CheckLog> hasCheckedInList = checkStudentLog.stream().filter(x -> x.getTimestamp().isAfter(startDateTime) && x.getTimestamp().isBefore(endDateTime)).collect(Collectors.toList());
            return hasCheckedInList.size() > 0;
        } else {
            return true;
        }
    }

    private boolean checkCurrentWeekInWeekLearn(int weekOfYear, String rawWeekLearn) {
        List<Integer> weekLearnList = Arrays.stream(rawWeekLearn.split("\\|", 0)).filter(x -> !x.equals("--")).map(Integer::parseInt).collect(Collectors.toList());
        return weekLearnList.contains(weekOfYear);
    }

    private boolean checkCurrentDayInWeekAvailable(int dayInWeek) {
        LocalDate localDate = LocalDate.now(ZoneId.of("Asia/Ho_Chi_Minh"));
        return localDate.getDayOfWeek().getValue() + 1 == dayInWeek;
    }

    private LocalTime getLocalTime() {
        Instant instant =  Instant.now();
        ZonedDateTime atZone =  instant.atZone(ZoneId.of("Asia/Ho_Chi_Minh"));
        return atZone.toLocalTime();
    }
    
    private int getWeekOfYear() {
        LocalDate localDate = LocalDate.now(ZoneId.of("Asia/Ho_Chi_Minh"));
        return localDate.get(WeekFields.of(Locale.ENGLISH).weekOfYear());
    }
}
