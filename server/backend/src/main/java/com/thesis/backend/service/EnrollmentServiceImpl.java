package com.thesis.backend.service;

import com.thesis.backend.dto.model.EnrollmentDto;
import com.thesis.backend.dto.model.SubjectDto;
import com.thesis.backend.dto.model.SubjectIDDto;
import com.thesis.backend.dto.model.UserDto;
import com.thesis.backend.exception.CustomException;
import com.thesis.backend.model.User;
import com.thesis.backend.repository.EnrollmentRepository;
import com.thesis.backend.repository.SubjectRepository;
import com.thesis.backend.repository.UserRepository;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

import static com.thesis.backend.constant.EntityType.ENROLLMENT;
import static com.thesis.backend.constant.ExceptionType.DUPLICATE_ENTITY;
import static com.thesis.backend.constant.ExceptionType.ENTITY_NOT_FOUND;

@Service
public class EnrollmentServiceImpl implements EnrollmentService {
    private final UserRepository userRepository;
    private final SubjectRepository subjectRepository;
    private final ModelMapper modelMapper;
    private final UserServiceImpl userService;
    private final SubjectServiceImpl subjectService;
    private final EnrollmentRepository enrollmentRepository;

    @Autowired
    public EnrollmentServiceImpl(UserRepository userRepository, SubjectRepository subjectRepository, ModelMapper modelMapper, UserServiceImpl userService, SubjectServiceImpl subjectService, EnrollmentRepository enrollmentRepository) {
        this.userRepository = userRepository;
        this.subjectRepository = subjectRepository;
        this.modelMapper = modelMapper;
        this.userService = userService;
        this.subjectService = subjectService;
        this.enrollmentRepository = enrollmentRepository;
    }

    @Override
    public EnrollmentDto enroll(EnrollmentDto enrollmentDto) {
        Integer userid = enrollmentDto.userId();
        SubjectIDDto subjectIDDto = enrollmentDto.subjectIDDto();
        UserDto user = userService.find(userid);
        SubjectDto subject = subjectService.find(subjectIDDto);
        if (!checkDidEnrolled(user, subject)) {
            saveEnrollmentToDatabase(user, subject);
            return EnrollmentDto.builder()
                    .userId(userid)
                    .subjectIDDto(subjectIDDto)
                    .build();
        }
        throw CustomException.throwException(ENROLLMENT, DUPLICATE_ENTITY, userid.toString(), subjectIDDto.toString());
    }


    @Override
    public void unregister(EnrollmentDto enrollmentDto) {
        Integer userid = enrollmentDto.userId();
        SubjectIDDto subjectIDDto = enrollmentDto.subjectIDDto();
        UserDto user = userService.find(userid);
        SubjectDto subject = subjectService.find(subjectIDDto);
        if (checkDidEnrolled(user, subject)) {
            deleteEnrollmentFromDatabase(user, subject);
            return;
        }
        throw CustomException.throwException(ENROLLMENT, ENTITY_NOT_FOUND, userid.toString(), subjectIDDto.toString());
    }

    @Override
    public List<UserDto> findAllUsersTakeSubject(SubjectIDDto subjectIDDto) {

        SubjectDto subjectDto = subjectService.find(subjectIDDto);
        return new ArrayList<>(subjectDto.getUserDtos());
    }

    @Override
    public List<SubjectDto> findAllSubjectsTakenByUser(Integer userid) {
        UserDto userDto = userService.find(userid);
        return new ArrayList<>(userDto.getSubjects());
    }

    @Override
    public List<SubjectIDDto> findAllSubjectIdsTakenByUser(Integer userid) {
        return findAllSubjectsTakenByUser(userid)
                .stream()
                .map(SubjectDto::getSubjectIDDto)
                .collect(Collectors.toList());
    }


    public boolean checkDidEnrolled(UserDto user, SubjectDto subject) {
        return findAllSubjectIdsTakenByUser(user.getId())
                .contains(subject.getSubjectIDDto());
    }

    private void saveEnrollmentToDatabase(UserDto user, SubjectDto subject) {
        enrollmentRepository.insertEnrollment(user.getId(), subject.getSubjectIDDto().getId(), subject.getSubjectIDDto().getGroupCode(), subject.getSubjectIDDto().getSemester());
    }

    private void deleteEnrollmentFromDatabase(UserDto user, SubjectDto subject) {
        user.getSubjects().remove(subject);
        User userToSave = modelMapper.map(user, User.class);
        userRepository.save(userToSave);
    }
}
