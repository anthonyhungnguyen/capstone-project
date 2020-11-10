package com.thesis.backend.controller;

import com.thesis.backend.repository.SubjectRepository;
import com.thesis.backend.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("api/update")
public class UpdateController {
    private final UserRepository userRepository;
    private final SubjectRepository subjectRepository;

    @Autowired
    public UpdateController(UserRepository userRepository, SubjectRepository subjectRepository) {
        this.userRepository = userRepository;
        this.subjectRepository = subjectRepository;
    }

//    @PutMapping("user/{id}")
//    public ResponseEntity<String> updateUserImage(@Valid @PathVariable("id") int id, @RequestBody Blob imageUrl) {
//        Optional<User> userToUpdate = userRepository.findById(id);
//        if (userToUpdate.isPresent()) {
//            userToUpdate.get().setImageUrl(imageUrl);
//            // Save is used both for persisting and updating
//            userRepository.save(userToUpdate.get());
//            return ResponseEntity.ok().body("Successfully");
//        } else {
//            return ResponseEntity.badRequest().body("Error");
//        }
//    }
//
//    @PutMapping("subject")
//    public ResponseEntity<Boolean> updateSubjectTimetable(@Valid @RequestBody Subject subject) {
//        Optional<Subject> subjectExist = subjectRepository.findById(subject.getId());
//        if (subjectExist.isPresent()) {
//            return ResponseEntity.ok().body(Boolean.TRUE);
//        } else {
//            return ResponseEntity.badRequest().body(Boolean.FALSE);
//        }
//    }
}
