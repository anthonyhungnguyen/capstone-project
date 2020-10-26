package com.thesis.backend.controller;

import com.thesis.backend.dto.SubjectTimetable;
import com.thesis.backend.dto.User;
import com.thesis.backend.repository.SubjectTimetableRepository;
import com.thesis.backend.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import java.util.Map;
import java.util.Optional;

@RestController
@RequestMapping("api/update")
public class UpdateController {
    private final UserRepository userRepository;
    private final SubjectTimetableRepository subjectTimetableRepository;

    @Autowired
    public UpdateController(UserRepository userRepository, SubjectTimetableRepository subjectTimetableRepository) {
        this.userRepository = userRepository;
        this.subjectTimetableRepository = subjectTimetableRepository;
    }

    @PutMapping("user/{id}")
    public ResponseEntity<String> updateUserImage(@Valid @PathVariable("id") String id, @RequestBody String imageUrl) {
        Optional<User> userToUpdate = userRepository.findById(id);
        if (userToUpdate.isPresent()) {
            userToUpdate.get().setImage_link(imageUrl);
            // Save is used both for persisting and updating
            userRepository.save(userToUpdate.get());
            return ResponseEntity.ok().body("Successfully");
        } else {
            return ResponseEntity.badRequest().body("Error");
        }
    }

    @PutMapping("subject/timetable/{id}")
    public ResponseEntity<Boolean> updateSubjectTimetable(@PathVariable Integer id, @RequestBody Map<String, Object> toUpdate) {
        System.out.println(id);
        System.out.println(toUpdate);
        Optional<SubjectTimetable> subjectExist = subjectTimetableRepository.findById(id);
        if (subjectExist.isPresent()) {
            SubjectTimetable toUpdateSubjectTimetable = subjectExist.get();
            toUpdateSubjectTimetable.getSubject().setId((String) toUpdate.get("subjectID"));
            toUpdateSubjectTimetable.getSubject().setName((String) toUpdate.get("subjectName"));
            toUpdateSubjectTimetable.setStart_time((String) toUpdate.get("startTime"));
            toUpdateSubjectTimetable.setEnd_time((String) toUpdate.get("endTime"));
            toUpdateSubjectTimetable.setDay_in_week((Integer) toUpdate.get("weekDay"));
            subjectTimetableRepository.save(toUpdateSubjectTimetable);
            return ResponseEntity.ok().body(Boolean.TRUE);
        } else {
            return ResponseEntity.badRequest().body(Boolean.FALSE);
        }
    }
}
