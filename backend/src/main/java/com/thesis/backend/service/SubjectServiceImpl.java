package com.thesis.backend.service;

import com.thesis.backend.dto.model.SubjectDto;
import com.thesis.backend.dto.model.SubjectIDDto;
import com.thesis.backend.exception.CustomException;
import com.thesis.backend.model.Subject;
import com.thesis.backend.model.SubjectId;
import com.thesis.backend.repository.SubjectRepository;
import lombok.extern.slf4j.Slf4j;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Optional;

import static com.thesis.backend.constant.EntityType.SUBJECT;
import static com.thesis.backend.constant.ExceptionType.DUPLICATE_ENTITY;
import static com.thesis.backend.constant.ExceptionType.ENTITY_NOT_FOUND;

@Service
@Slf4j
public class SubjectServiceImpl implements BaseService<SubjectDto, SubjectIDDto>, SubjectService {
    private final SubjectRepository subjectRepository;
    private final ModelMapper modelMapper;

    @Autowired
    public SubjectServiceImpl(SubjectRepository subjectRepository, ModelMapper modelMapper) {
        this.subjectRepository = subjectRepository;
        this.modelMapper = modelMapper;
    }

    @Override
    public SubjectDto find(SubjectIDDto id) {
        Optional<Subject> subject = subjectRepository.findById(modelMapper.map(id, SubjectId.class));
        if (subject.isPresent()) {
            return modelMapper.map(subject.get(), SubjectDto.class);
        }
        throw CustomException.throwException(SUBJECT, ENTITY_NOT_FOUND, id.toString());
    }

    @Override
    public SubjectDto create(SubjectDto o) {
        Optional<Subject> subject = subjectRepository.findById(modelMapper.map(o.getSubjectIDDto(), SubjectId.class));
        if (subject.isEmpty()) {
            Subject mapToSubject = modelMapper.map(o, Subject.class);
            return modelMapper.map(subjectRepository.save(mapToSubject), SubjectDto.class);
        }
        throw CustomException.throwException(SUBJECT, DUPLICATE_ENTITY, o.getSubjectIDDto().toString());
    }

    @Override
    public void delete(SubjectIDDto o) {
        Optional<Subject> subject = subjectRepository.findById(modelMapper.map(o, SubjectId.class));
        if (subject.isPresent()) {
            subjectRepository.delete(modelMapper.map(o, Subject.class));
            return;
        }
        throw CustomException.throwException(SUBJECT, ENTITY_NOT_FOUND, o.toString());
    }

    @Override
    public SubjectDto update(SubjectDto o) {
        Optional<Subject> subject = subjectRepository.findById(modelMapper.map(o.getSubjectIDDto(), SubjectId.class));
        if (subject.isPresent()) {
            Subject savedSubject = subjectRepository.save(modelMapper.map(o, Subject.class));
            return modelMapper.map(savedSubject, SubjectDto.class);
        }
        throw CustomException.throwException(SUBJECT, ENTITY_NOT_FOUND, o.getSubjectIDDto().toString());
    }
}
