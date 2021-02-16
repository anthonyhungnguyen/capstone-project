package com.thesis.backend;

import com.thesis.backend.dto.model.SubjectDto;
import com.thesis.backend.dto.model.SubjectIDDto;
import com.thesis.backend.dto.model.UserDto;
import com.thesis.backend.repository.SubjectRepository;
import com.thesis.backend.service.EnrollmentServiceImpl;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertFalse;

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
        List<SubjectDto> subjectDtoList = enrollmentService.findAllSubjectsEnrolledByUser(1752259);
        assertFalse(subjectDtoList.isEmpty());
    }

    @Test
    public void testFindAllUsersTakeSubject() {
        List<UserDto> userDtoList = enrollmentService.findAllUsersTakeSubject(existingSubjectIDDto);
        assertFalse(userDtoList.isEmpty());
    }

    @Test
    public void testEnrolledSuccessfully() {
        List<SubjectDto> subjectDtoList = enrollmentService.findAllSubjectsEnrolledByUser(1752259);
        
    }
}
