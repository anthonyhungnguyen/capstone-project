package com.thesis.backend.service;

import com.thesis.backend.dto.model.EnrollmentDto;
import com.thesis.backend.dto.model.SubjectDto;
import com.thesis.backend.dto.model.SubjectIDDto;
import com.thesis.backend.dto.model.UserDto;
import com.thesis.backend.exception.CustomException;
import com.thesis.backend.model.Subject;
import com.thesis.backend.model.SubjectId;
import com.thesis.backend.model.User;
import com.thesis.backend.repository.SubjectRepository;
import com.thesis.backend.repository.UserRepository;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

import static com.thesis.backend.constant.EntityType.*;
import static com.thesis.backend.constant.ExceptionType.*;

@Service
public class EnrollmentServiceImpl implements EnrollmentService {
    private final UserRepository userRepository;
    private final SubjectRepository subjectRepository;
    private final ModelMapper modelMapper;

    @Autowired
    public EnrollmentServiceImpl(UserRepository userRepository, SubjectRepository subjectRepository, ModelMapper modelMapper) {
        this.userRepository = userRepository;
        this.subjectRepository = subjectRepository;
        this.modelMapper = modelMapper;
    }

    @Override
    public EnrollmentDto enroll(EnrollmentDto enrollmentDto) {
        Integer userid = enrollmentDto.userId();
        SubjectIDDto subjectIDDto = enrollmentDto.subjectIDDto();
        SubjectId subjectId = modelMapper.map(subjectIDDto, SubjectId.class);
        Optional<User> user = userRepository.findById(enrollmentDto.userId());
        Optional<Subject> subject = subjectRepository.findById(subjectId);
        if (checkUserAndSubjectExist(user, subject)) {
            if (checkSubjectAlreadyEnrolled(user.get(), subject.get())) {
                saveEnrollmentToDatabase(user.get(), subject.get());
                return EnrollmentDto.builder()
                        .userId(userid)
                        .subjectIDDto(subjectIDDto)
                        .build();
            }
            throw CustomException.throwException(ENROLLMENT, DUPLICATE_ENTITY, userid.toString(), subjectIDDto.toString());
        }
        throw CustomException.throwException(ENROLLMENT, ENTITY_NOT_FOUND, userid.toString(), subjectIDDto.toString());
    }

    @Override
    public void unregister(EnrollmentDto enrollmentDto) {
        Integer userid = enrollmentDto.userId();
        SubjectIDDto subjectIDDto = enrollmentDto.subjectIDDto();
        SubjectId subjectId = modelMapper.map(subjectIDDto, SubjectId.class);
        Optional<User> user = userRepository.findById(userid);
        Optional<Subject> subject = subjectRepository.findById(subjectId);
        if (checkUserAndSubjectExist(user, subject) && checkSubjectAlreadyEnrolled(user.get(), subject.get())) {
            deleteEnrollmentFromDatabase(user.get(), subject.get());
        }
        throw CustomException.throwException(ENROLLMENT, ENTITY_NOT_FOUND, userid.toString(), subjectIDDto.toString());
    }

    @Override
    public List<SubjectDto> findAllSubjectsEnrolledByUser(Integer userid) {
        Optional<User> user = userRepository.findById(userid);
        if (user.isPresent()) {
            return user.get().getSubjects()
                    .stream()
                    .map(subject -> modelMapper.map(subject, SubjectDto.class))
                    .collect(Collectors.toList());
        }
        throw CustomException.throwException(USER, ENTITY_EXCEPTION, userid.toString());
    }

    @Override
    public List<UserDto> findAllUsersTakeSubject(SubjectIDDto subjectIDDto) {
        SubjectId subjectId = modelMapper.map(subjectIDDto, SubjectId.class);
        Optional<Subject> subject = subjectRepository.findById(subjectId);
        if (subject.isPresent()) {
            return subject.get().getUsers()
                    .stream()
                    .map(user -> modelMapper.map(user, UserDto.class))
                    .collect(Collectors.toList());
        }
        throw CustomException.throwException(SUBJECT, ENTITY_NOT_FOUND, subjectIDDto.toString());
    }

    private boolean checkUserAndSubjectExist(Optional<User> user, Optional<Subject> subject) {
        return user.isPresent() && subject.isPresent();
    }

    private boolean checkSubjectAlreadyEnrolled(User user, Subject subject) {
        return user.getSubjects().contains(subject);
    }

    private void saveEnrollmentToDatabase(User user, Subject subject) {
        user.getSubjects().add(subject);
        userRepository.save(user);
    }

    private void deleteEnrollmentFromDatabase(User user, Subject subject) {
        user.getSubjects().remove(subject);
        userRepository.save(user);
    }
}
