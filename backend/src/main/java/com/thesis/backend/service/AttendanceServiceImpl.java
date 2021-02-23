package com.thesis.backend.service;

import com.thesis.backend.dto.model.EnrollmentDto;
import com.thesis.backend.dto.model.LogDto;
import com.thesis.backend.dto.model.SubjectDto;
import com.thesis.backend.dto.model.UserDto;
import com.thesis.backend.exception.CustomException;
import com.thesis.backend.util.DateUtil;
import com.thesis.backend.util.StringUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalTime;
import java.util.List;

import static com.thesis.backend.constant.EntityType.ATTENDANCE;
import static com.thesis.backend.constant.EntityType.ENROLLMENT;
import static com.thesis.backend.constant.ExceptionType.*;

@Service
public class AttendanceServiceImpl implements AttendanceService {
    private final EnrollmentServiceImpl enrollmentService;
    private final UserServiceImpl userService;
    private final SubjectServiceImpl subjectService;
    private final LogService logService;

    @Autowired
    public AttendanceServiceImpl(EnrollmentServiceImpl enrollmentService, UserServiceImpl userService, SubjectServiceImpl subjectService, LogService logService) {
        this.enrollmentService = enrollmentService;
        this.userService = userService;
        this.subjectService = subjectService;
        this.logService = logService;
    }


    @Override
    public LogDto checkAttendance(EnrollmentDto enrollmentDto) {
        UserDto userDto = userService.find(enrollmentDto.userId());
        SubjectDto subjectDto = subjectService.find(enrollmentDto.subjectIDDto());
        if (enrollmentService.checkDidEnrolled(userDto, subjectDto)) {
            List<String> timeRangeList = StringUtil.convertRawTimeRangeToList(subjectDto.getTimeRange());
            LocalTime start = DateUtil.convertTimeStringToLocalTimeObject(timeRangeList.get(0));
            LocalTime end = DateUtil.convertTimeStringToLocalTimeObject(timeRangeList.get(1));
            if (isCurrentDayInSchedule(subjectDto.getWeekDay())
                    && isCurrentWeekInSchedule(subjectDto.getWeekLearn())
                    && isCurrentTimeInSchedule(start, end)) {
                if (!hasChecked(enrollmentDto, start, end)) {
                    String attendanceType = generateSuitableAttendanceType(start, end);
                    return logService.save(enrollmentDto, attendanceType);
                }
                throw CustomException.throwException(ATTENDANCE,
                        DUPLICATE_ENTITY,
                        String.valueOf(userDto.getId()),
                        subjectDto.getSubjectIDDto().toString());
            }
            throw CustomException.throwException(ATTENDANCE,
                    TIME_NOT_MATCH,
                    String.valueOf(userDto.getId()),
                    subjectDto.getSubjectIDDto().toString());
        }
        throw CustomException.throwException(ENROLLMENT,
                ENTITY_NOT_FOUND,
                String.valueOf(userDto.getId()),
                subjectDto.getSubjectIDDto().toString());
    }

    public String generateSuitableAttendanceType(LocalTime start, LocalTime end) {
        LocalTime current = DateUtil.localTime();
        String attendanceType = "check-in";
        long timeDifferenceFromStart = DateUtil.timeDifferenceInMinutes(start, current);
        long timeDifferenceToEnd = DateUtil.timeDifferenceInMinutes(current, end);
        if (timeDifferenceFromStart > 5) {
            attendanceType = "late";
        }
        if (timeDifferenceToEnd < 5) {
            attendanceType = "check-out";
        }
        return attendanceType;
    }

    private boolean hasChecked(EnrollmentDto enrollmentDto, LocalTime start, LocalTime end) {
        return logService.findAllLogsInTimeRange(enrollmentDto, start, end).size() > 0;
    }

    private boolean isCurrentTimeInSchedule(LocalTime start, LocalTime end) {
        LocalTime current = DateUtil.localTime();
        return start.isBefore(current) && end.isAfter(current);
    }

    private boolean isCurrentWeekInSchedule(String weekString) {
        int weekOfYear = DateUtil.weekOfYear();
        return StringUtil.convertRawWeekScheduleToList(weekString).contains(weekOfYear);
    }

    private boolean isCurrentDayInSchedule(int scheduleDay) {
        return DateUtil.dayOfWeek() == scheduleDay;
    }
}
