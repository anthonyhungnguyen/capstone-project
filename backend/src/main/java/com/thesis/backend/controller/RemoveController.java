package com.thesis.backend.controller;

import com.thesis.backend.dto.Subject;
import com.thesis.backend.dto.SubjectId;
import com.thesis.backend.dto.User;
import com.thesis.backend.repository.SubjectRepository;
import com.thesis.backend.repository.UserRepository;
import org.apache.coyote.Response;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import javax.validation.Path;
import javax.validation.Valid;
import java.util.Optional;

@RestController
@RequestMapping("/api/remove")
public class RemoveController {
    private final SubjectRepository subjectRepository;
    private final UserRepository userRepository;

    @Autowired
    public RemoveController(SubjectRepository subjectRepository, UserRepository userRepository) {
        this.subjectRepository = subjectRepository;
        this.userRepository = userRepository;
    }

    @DeleteMapping("user/{id]")
    public ResponseEntity<String> removeUser(@PathVariable("id") int id) {
        if (userRepository.existsById(id)) {
            return ResponseEntity.badRequest().body("Fail");
        } else {
            userRepository.deleteById(id);
            return ResponseEntity.ok().body("Successfully");
        }
    }

    @DeleteMapping("subject/{semester}/{groupCode}/{id}")
    public ResponseEntity<String> deleteSubject(@PathVariable("semester") int semester, @PathVariable("groupCode") String groupCode, @PathVariable("id") String id) {
        SubjectId subjectId = new SubjectId(id, groupCode, semester);
        if (subjectRepository.existsById(subjectId)) {
            subjectRepository.deleteById(subjectId);
            return ResponseEntity.ok().body("Successfully");
        } else {
            return ResponseEntity.badRequest().body("Fail");
        }
    }

    @DeleteMapping("enrollment/{userId}/{semester}/{groupCode}/{subjectId}")
    public ResponseEntity<String> addEnrollment(@PathVariable int userId, @PathVariable int semester, @PathVariable String groupCode, @PathVariable String subjectId) {
        Optional<User> existingUser = userRepository.findById(userId);
        Optional<Subject> existingSubject = subjectRepository.findById(new SubjectId(subjectId, groupCode, semester));
        if (existingUser.isEmpty()) {
            return ResponseEntity.badRequest().body("User not found");
        } else if (existingSubject.isEmpty()) {
            return ResponseEntity.badRequest().body("Subject not found");
        } else if (existingUser.get().getSubjects().contains(existingSubject.get())) {
            return ResponseEntity.badRequest().body("Subject is already existed");
        } else {
            // TODO: add remove enrollment
            return ResponseEntity.ok().body("Successfully");
        }
    }
}
