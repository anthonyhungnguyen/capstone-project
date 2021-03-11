package com.thesis.backend.service;

import com.thesis.backend.dto.model.SubjectDto;
import com.thesis.backend.dto.model.SubjectIDDto;
import com.thesis.backend.dto.model.UserDto;
import com.thesis.backend.dto.request.AttendanceRequest;
import com.thesis.backend.exception.CustomException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import static com.thesis.backend.constant.EntityType.ENROLLMENT;
import static com.thesis.backend.constant.ExceptionType.ENTITY_NOT_FOUND;

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
    public void checkAttendanceUtil(AttendanceRequest attendanceRequest) {
        UserDto userDto = userService.find(attendanceRequest.getUserID());
        SubjectDto subjectDto = subjectService.find(new SubjectIDDto(attendanceRequest.getSubjectID(),
                attendanceRequest.getGroupCode(),
                attendanceRequest.getSemester()));
        if (enrollmentService.checkDidEnrolled(userDto, subjectDto)) {
            logService.saveAttendance(attendanceRequest);
            return;
        }
        throw CustomException.throwException(ENROLLMENT,
                ENTITY_NOT_FOUND,
                String.valueOf(userDto.getId()),
                subjectDto.getSubjectIDDto().toString());
    }
}
