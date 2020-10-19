package com.thesis.backend.service;

import com.thesis.backend.repository.SubjectRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class RegisterService {
    private final SubjectRepository subjectRepository;

    @Autowired
    public RegisterService(SubjectRepository subjectRepository) {
        this.subjectRepository = subjectRepository;
    }

    public boolean checkSubjectExist(String subjectId) {
        return subjectRepository.existsById(subjectId);
    }
}
