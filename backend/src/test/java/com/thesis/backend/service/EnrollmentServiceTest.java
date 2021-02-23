package com.thesis.backend.service;

import com.thesis.backend.BackendApplication;
import com.thesis.backend.dto.model.EnrollmentDto;
import com.thesis.backend.dto.model.SubjectDto;
import com.thesis.backend.dto.model.SubjectIDDto;
import com.thesis.backend.dto.model.UserDto;
import com.thesis.backend.repository.mysql.SubjectRepository;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

@RunWith(SpringRunner.class)
@SpringBootTest(classes = BackendApplication.class)
@Transactional
public class EnrollmentServiceTest {
    @Autowired
    private ModelMapper modelMapper;

    @Autowired
    private SubjectRepository subjectRepository;

    @Autowired
    private EnrollmentServiceImpl enrollmentService;

    public static final SubjectIDDto existingSubjectIDDto = SubjectIDDto.builder().
            id("CO0000")
            .groupCode("CC01")
            .semester(201)
            .build();

    public static final SubjectDto existingSubjectDto = SubjectDto.builder()
            .subjectIDDto(existingSubjectIDDto)
            .build();

    @Test
    public void testFindAllSubjectsEnrolledByUser() {
        List<SubjectDto> subjectDtoList = enrollmentService.findAllSubjectsTakenByUser(1752259);
        assertFalse(subjectDtoList.isEmpty());
    }

    @Test
    public void testFindAllUsersTakeSubject() {
        List<UserDto> userDtoList = enrollmentService.findAllUsersTakeSubject(SubjectIDDto
                .builder()
                .id("SP1009")
                .groupCode("CC03")
                .semester(201)
                .build());
        assertFalse(userDtoList.isEmpty());
    }

//    @Test
//    public void testEnrolledSuccessfully() {
//        List<SubjectIDDto> subjectDtoList = enrollmentService.findAllSubjectIdsTakenByUser(1752259);
//        assertFalse(subjectDtoList.contains(existingSubjectIDDto));
//        EnrollmentDto enrollmentDto = EnrollmentDto.builder()
//                .userId(1752259)
//                .subjectIDDto(existingSubjectIDDto)
//                .build();
//        enrollmentService.enroll(enrollmentDto);
//        assertTrue(enrollmentService.checkDidEnrolled(1752259, existingSubjectDto));
//    }

    @Test
    public void testUnregisterSuccessfully() {
        List<SubjectIDDto> subjectDtoList = enrollmentService.findAllSubjectIdsTakenByUser(1752259);
        EnrollmentDto enrollmentDto = EnrollmentDto.builder()
                .userId(1752259)
                .subjectIDDto(subjectDtoList.get(0))
                .build();
        enrollmentService.unregister(enrollmentDto);
        List<SubjectIDDto> subjectIDDtoListToCheck = enrollmentService.findAllSubjectIdsTakenByUser(1752259);
        assertFalse(subjectIDDtoListToCheck.contains(subjectDtoList.get(0)));
    }

}
