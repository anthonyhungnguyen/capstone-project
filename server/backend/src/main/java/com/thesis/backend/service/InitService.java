package com.thesis.backend.service;

import com.thesis.backend.dto.model.*;
import com.thesis.backend.dto.request.SignUpRequest;
import com.thesis.backend.repository.RegisterRepository;
import lombok.extern.slf4j.Slf4j;
import org.modelmapper.ModelMapper;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
@Slf4j
public class InitService {
    private final SubjectServiceImpl subjectService;
    private final ModelMapper modelMapper;
    private final UserServiceImpl userService;
    private final EnrollmentService enrollmentService;
    private final FirebaseService firebaseService;
    private final RegisterRepository registerRepository;

    public InitService(SubjectServiceImpl subjectService, ModelMapper modelMapper, UserServiceImpl userService, EnrollmentService enrollmentService, FirebaseService firebaseService, RegisterRepository registerRepository) {
        this.subjectService = subjectService;
        this.modelMapper = modelMapper;
        this.userService = userService;
        this.enrollmentService = enrollmentService;
        this.firebaseService = firebaseService;
        this.registerRepository = registerRepository;
    }

    public String registerFull(Map<String, Object> requestData) throws IOException {
        int semester = (int) requestData.get("semester");
        String subjectID = (String) requestData.get("subjectID");
        String groupCode = (String) requestData.get("groupCode");
        String name = (String) requestData.get("name");
        SubjectIDDto subjectIDDto = SubjectIDDto.builder().id(subjectID).groupCode(groupCode).semester(semester).build();
        SubjectDto subjectDto = SubjectDto.builder().subjectIDDto(subjectIDDto).name(name).build();
        List<Integer> studentList = (List<Integer>) requestData.get("studentList");
        initSubject(subjectDto);
        initUser(studentList);
        initEnrollment(studentList, subjectIDDto);
        initFirebaseSubject(semester, subjectID, groupCode);
        return "Finish";
    }

    private void initSubject(SubjectDto subjectDto) {
        try {
            SubjectDto createdSubject = subjectService.create(subjectDto);

        } catch (Exception e) {
            log.warn("[Register full | Subject]: {}", e.toString());
        }
    }

    private void initUser(List<Integer> studentList) {
        studentList.forEach(s -> {
            try {
                SignUpRequest signUpRequest = new SignUpRequest(s, String.valueOf(s));
                userService.register(signUpRequest);
            } catch (Exception e) {
                log.info("[Register full | User]: {}", e.toString());
            }
        });
    }

    private void initEnrollment(List<Integer> studentList, SubjectIDDto subjectIDDto) {
        studentList.forEach(s -> {
            try {
                EnrollmentDto enrollmentDto = EnrollmentDto.builder().subjectIDDto(subjectIDDto).userId(s).build();
                enrollmentService.enroll(enrollmentDto);
            } catch (Exception e) {
                log.info("[Register full | Enrollment]: {}", e.toString());
            }
        });
    }

    private void initFirebaseSubject(int semester, String subjectID, String groupCode) throws IOException {
        String subjectIDCompose = String.format("%s_%s_%s", semester, subjectID, groupCode);
        firebaseService.initSubject(subjectIDCompose);
    }

    public String initFillRegisterImages() {
        List<Integer> studentList = userService.findAll().stream()
                .filter(s -> s.getRoleDtos().contains(new RoleDto("STUDENT")))
                .map(UserDto::getId)
                .collect(Collectors.toList());
        Map<Integer, List<String>> registerPaths = firebaseService.requestRegisterPaths();
        for (Integer s : studentList) {
            try {
                registerRepository.deleteRegisterByUserId(s);
            } catch (Exception e) {
                log.warn("[initFillRegisterImages] cannot delete userid - {} - {}", s, e.getMessage());
            }
            try {
                List<String> imageLinkList = registerPaths.get(s);
                imageLinkList.forEach(link -> {
                    registerRepository.insertRegisterByUserId(s, link);
                });
            } catch (Exception e) {
                log.warn("[initFillRegisterImages] find student in hashmap {}", e.getMessage());
            }
        }
        return "Successfully";
    }
}
