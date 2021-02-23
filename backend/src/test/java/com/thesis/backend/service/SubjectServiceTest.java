package com.thesis.backend.service;

import com.thesis.backend.BackendApplication;
import com.thesis.backend.dto.model.SubjectDto;
import com.thesis.backend.dto.model.SubjectIDDto;
import com.thesis.backend.exception.CustomException;
import com.thesis.backend.model.Subject;
import com.thesis.backend.model.SubjectId;
import com.thesis.backend.repository.mysql.SubjectRepository;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.transaction.annotation.Transactional;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;

@RunWith(SpringRunner.class)
@SpringBootTest(classes = BackendApplication.class)
@Transactional
public class SubjectServiceTest {
    @Autowired
    private ModelMapper modelMapper;

    @Autowired
    private SubjectRepository subjectRepository;

    @Autowired
    private SubjectServiceImpl subjectService;
    public static final SubjectIDDto existingSubjectIDDto = SubjectIDDto.builder().
            id("SP1009")
            .groupCode("CC03")
            .semester(201)
            .build();
    public static final SubjectIDDto nonExistingSubjectIDDto = SubjectIDDto.builder().
            id("A")
            .groupCode("B")
            .semester(0)
            .build();
    public static final SubjectDto existingSubjectDto = SubjectDto.builder()
            .subjectIDDto(existingSubjectIDDto)
            .build();

    public static final SubjectDto nonExistingSubjectDto = SubjectDto.builder()
            .subjectIDDto(nonExistingSubjectIDDto)
            .build();

    @Test
    public void testModelMapperNotNull() {
        assertNotEquals(modelMapper, null);
    }

    @Test
    public void testSaveSubjectSuccessfully() {
        Subject testSubject = modelMapper.map(nonExistingSubjectDto, Subject.class);
        Subject savedSubject = modelMapper.map(subjectService.create(nonExistingSubjectDto), Subject.class);
        assertEquals(testSubject, savedSubject);
    }

    @Test
    public void testSavedSubjectFailedShouldThrowDuplicateException() {
        assertThrows(CustomException.DuplicateEntityException.class, () -> {
            subjectService.create(existingSubjectDto);
        });
    }

    @Test
    public void testFindExistingSubject() {
        SubjectDto subjectDto = subjectService.find(existingSubjectIDDto);
        assertNotNull(subjectDto);
    }

    @Test
    public void testFindNonExistingSubjectShouldThrowEntityNotFoundException() {
        assertThrows(CustomException.EntityNotFoundException.class, () -> {
            subjectService.find(nonExistingSubjectIDDto);
        });
    }

    @Test
    public void testUpdateExistingSubject() {
        SubjectDto subjectDto = subjectService.find(existingSubjectIDDto);
        assertNotNull(subjectDto);
        subjectDto.setName("test1");
        subjectService.update(subjectDto);
        assertEquals(subjectDto.getName(), subjectService.find(existingSubjectIDDto).getName());
    }

    @Test
    public void testUpdateNonExistingSubjectShouldThrowEntityNotFoundException() {
        assertThrows(CustomException.EntityNotFoundException.class, () -> {
            subjectService.update(nonExistingSubjectDto);
        });
    }

    @Test
    public void testDeleteExistingSubject() {
        subjectService.delete(existingSubjectIDDto);
        SubjectId subjectId = modelMapper.map(existingSubjectDto, SubjectId.class);
        Optional<Subject> subject = subjectRepository.findById(subjectId);
        assertTrue(subject.isEmpty());
    }

    @Test
    public void testDeleteNonExistingSubject() {
        assertThrows(CustomException.EntityNotFoundException.class, () -> {
            subjectService.delete(nonExistingSubjectIDDto);
        });
    }


}
