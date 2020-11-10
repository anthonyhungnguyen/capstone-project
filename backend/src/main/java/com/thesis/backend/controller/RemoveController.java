package com.thesis.backend.controller;

import com.thesis.backend.repository.SubjectRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/remove")
public class RemoveController {
    private final SubjectRepository subjectRepository;

    @Autowired
    public RemoveController(SubjectRepository subjectRepository) {
        this.subjectRepository = subjectRepository;
    }

//    @DeleteMapping("enrollment")
//    public ResponseEntity<Boolean> removeTimetable() {
//        Optional<Enrollment> enrollmentExist = enrollmentRepository.findById(id);
//        if (timetableExist.isPresent()) {
//            subjectTimetableRepository.delete(timetableExist.get());
//            return ResponseEntity.ok().body(true);
//        } else {
//            return ResponseEntity.badRequest().body(false);
//        }
//    }

//    @DeleteMapping("subject/{id}")
//    public ResponseEntity<Boolean> removeSubject(@PathVariable("id") String id) {
//        Optional<Subject> subjectExist = subjectRepository.findById(id);
//        if (subjectExist.isPresent()) {
//            subjectRepository.delete(subjectExist.get());
//            return ResponseEntity.ok().body(true);
//        } else {
//            return ResponseEntity.badRequest().body(false);
//        }
//    }
}
