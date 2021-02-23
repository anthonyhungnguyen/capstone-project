package com.thesis.backend.service;


import com.thesis.backend.BackendApplication;
import com.thesis.backend.dto.model.EnrollmentDto;
import com.thesis.backend.dto.model.LogDto;
import com.thesis.backend.dto.model.SubjectIDDto;
import com.thesis.backend.exception.CustomException;
import com.thesis.backend.model.Subject;
import com.thesis.backend.model.User;
import com.thesis.backend.repository.mongodb.LogRepository;
import com.thesis.backend.repository.mysql.SubjectRepository;
import com.thesis.backend.util.DateUtil;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;

import static org.junit.jupiter.api.Assertions.*;

@RunWith(SpringRunner.class)
@SpringBootTest(classes = BackendApplication.class)
@Transactional
public class AttendanceServiceTest {
    @Autowired
    private ModelMapper modelMapper;

    @Autowired
    private LogRepository logRepository;

    @Autowired
    private EnrollmentServiceImpl enrollmentService;

    @Autowired
    private SubjectRepository subjectRepository;

    @Autowired
    private AttendanceServiceImpl attendanceService;

    @Test
    public void testCheckAttendanceSuccess() {
        Integer userid = 1752259;
        SubjectIDDto subjectIDDto = SubjectIDDto.builder()
                .id("id_test")
                .groupCode("group_test")
                .semester(0)
                .build();
        EnrollmentDto enrollmentDto = EnrollmentDto.builder()
                .userId(userid)
                .subjectIDDto(subjectIDDto)
                .build();
        LogDto logDto = attendanceService.checkAttendance(enrollmentDto);
        assertEquals(logDto.getEnrollmentDto().userId(), userid);
    }

    @Test
    public void testCheckAttendanceTimeNotMatchFail() {
        Integer userid = 1752259;
        SubjectIDDto subjectIDDto = SubjectIDDto.builder()
                .id("SP1009")
                .groupCode("CC03")
                .semester(201)
                .build();
        EnrollmentDto enrollmentDto = EnrollmentDto.builder()
                .userId(userid)
                .subjectIDDto(subjectIDDto)
                .build();
        assertThrows(CustomException.TimeNotMatchException.class, () -> {
            attendanceService.checkAttendance(enrollmentDto);
        });
    }
}
