package com.thesis.backend.controller;

import com.thesis.backend.dto.Subject;
import com.thesis.backend.repository.SubjectRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Optional;

@RestController
@RequestMapping("/api/remove")
public class RemoveController {
    private final SubjectTimetableRepository subjectTimetableRepository;
    private final SubjectRepository subjectRepository;

    @Autowired
    public RemoveController(SubjectTimetableRepository subjectTimetableRepository, SubjectRepository subjectRepository) {
        this.subjectTimetableRepository = subjectTimetableRepository;
        this.subjectRepository = subjectRepository;
    }

    @DeleteMapping("timetable/{id}")
    public ResponseEntity<Boolean> removeTimetable(@PathVariable("id") Integer id) {
        Optional<SubjectTimetable> timetableExist = subjectTimetableRepository.findById(id);
        if (timetableExist.isPresent()) {
            subjectTimetableRepository.delete(timetableExist.get());
            return ResponseEntity.ok().body(true);
        } else {
            return ResponseEntity.badRequest().body(false);
        }
    }

    @DeleteMapping("subject/{id}")
    public ResponseEntity<Boolean> removeSubject(@PathVariable("id") String id) {
        Optional<Subject> subjectExist = subjectRepository.findById(id);
        if (subjectExist.isPresent()) {
            subjectRepository.delete(subjectExist.get());
            return ResponseEntity.ok().body(true);
        } else {
            return ResponseEntity.badRequest().body(false);
        }
    }
}
