package com.thesis.backend.service;

import com.thesis.backend.dto.model.EnrollmentDto;
import com.thesis.backend.dto.model.SubjectDto;
import com.thesis.backend.dto.model.SubjectIDDto;
import com.thesis.backend.dto.model.UserDto;
import com.thesis.backend.exception.CustomException;
import com.thesis.backend.repository.EnrollmentRepository;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

import static com.thesis.backend.constant.EntityType.ENROLLMENT;
import static com.thesis.backend.constant.ExceptionType.DUPLICATE_ENTITY;

@Service
public class EnrollmentService {
    private final UserService userService;
    private final SubjectService subjectService;
    private final EnrollmentRepository enrollmentRepository;

    public EnrollmentService(UserService userService, SubjectService subjectService, EnrollmentRepository enrollmentRepository) {
        this.userService = userService;
        this.subjectService = subjectService;
        this.enrollmentRepository = enrollmentRepository;
    }


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


    public List<UserDto> findAllUsersTakeSubject(SubjectIDDto subjectIDDto) {

        SubjectDto subjectDto = subjectService.find(subjectIDDto);
        return new ArrayList<>(subjectDto.getUserDtos());
    }

    public List<SubjectDto> findAllSubjectsTakenByUser(Integer userid) {
        UserDto userDto = userService.find(userid);
        return new ArrayList<>(userDto.getSubjects());
    }

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
}
