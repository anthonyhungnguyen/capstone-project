package com.thesis.backend.controller;

import com.thesis.backend.dto.request.SubjectRegister;
import com.thesis.backend.service.TeacherService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.validation.Valid;
import java.io.IOException;

@RestController
@RequestMapping(value = "/api/teacher")
public class TeacherController {

    private final TeacherService teacherService;

    @Autowired
    public TeacherController(TeacherService teacherService) {
        this.teacherService = teacherService;
    }

    @PostMapping
    public ResponseEntity<Boolean> register(@Valid @RequestBody SubjectRegister subjectRegister) throws IOException {
        return ResponseEntity.ok(teacherService.registerIOTDevice(subjectRegister));
    }
}
