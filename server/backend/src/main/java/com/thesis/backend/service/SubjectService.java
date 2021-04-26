package com.thesis.backend.service;

import com.thesis.backend.dto.mapper.SubjectMapper;
import com.thesis.backend.dto.model.SubjectDto;
import com.thesis.backend.dto.model.SubjectIDDto;
import com.thesis.backend.exception.CustomException;
import com.thesis.backend.model.Subject;
import com.thesis.backend.model.SubjectId;
import com.thesis.backend.model.User;
import com.thesis.backend.repository.SubjectRepository;
import lombok.extern.slf4j.Slf4j;
import org.jetbrains.annotations.NotNull;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

import static com.thesis.backend.constant.EntityType.SUBJECT;
import static com.thesis.backend.constant.ExceptionType.DUPLICATE_ENTITY;
import static com.thesis.backend.constant.ExceptionType.ENTITY_NOT_FOUND;

@Service
@Slf4j
public class SubjectService {
    private final SubjectRepository subjectRepository;
    private final ModelMapper modelMapper;

    @Autowired
    public SubjectService(SubjectRepository subjectRepository, ModelMapper modelMapper) {
        this.subjectRepository = subjectRepository;
        this.modelMapper = modelMapper;
    }

    public List<SubjectDto> findAll() {
        return subjectRepository.findAll().stream().map(SubjectMapper::toSubjectDto).collect(Collectors.toList());

    }

    public SubjectDto find(@NotNull SubjectIDDto id) {
        Optional<Subject> subject = subjectRepository.findById(modelMapper.map(id, SubjectId.class));
        if (subject.isPresent()) {
            return SubjectMapper.toSubjectDto(subject.get());
        }
        throw CustomException.throwException(SUBJECT, ENTITY_NOT_FOUND, id.toString());
    }

    public SubjectDto create(@NotNull SubjectDto o) {
        Optional<Subject> subject = subjectRepository.findById(modelMapper.map(o.getSubjectIDDto(), SubjectId.class));
        if (subject.isEmpty()) {
            Subject mapToSubject = modelMapper.map(o, Subject.class);
            return modelMapper.map(subjectRepository.save(mapToSubject), SubjectDto.class);
        }
        throw CustomException.throwException(SUBJECT, DUPLICATE_ENTITY, o.getSubjectIDDto().toString());
    }

    public List<User> findAllUsersTakeSubject(int semester, String subjectID, String groupCode) {
        SubjectIDDto o = new SubjectIDDto(subjectID, groupCode, semester);
        Optional<Subject> subject = subjectRepository.findById(modelMapper.map(o, SubjectId.class));
        if (subject.isPresent()) {
            return subject.get().getUsers();
        }
        throw CustomException.throwException(SUBJECT, ENTITY_NOT_FOUND, o.toString());
    }

    public Integer countStudentsInSubject(int semester, String subjectID, String groupCode) {
        return subjectRepository.countStudentsInSubject(semester, subjectID, groupCode);
    }
}
