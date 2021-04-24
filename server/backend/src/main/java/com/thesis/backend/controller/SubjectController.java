package com.thesis.backend.controller;

import com.thesis.backend.dto.model.SubjectDto;
import com.thesis.backend.dto.model.SubjectIDDto;
import com.thesis.backend.service.SubjectServiceImpl;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import java.util.List;

@RestController(value = "Subject controller")
@RequestMapping(value = "/api/subject",
        produces = MediaType.APPLICATION_JSON_VALUE)
@Slf4j
@Tag(name = "Subject")
public class SubjectController {
    private final SubjectServiceImpl subjectServiceImpl;

    @GetMapping("/all")
    public ResponseEntity<List<SubjectDto>> findAll() {
        return ResponseEntity.ok(subjectServiceImpl.findAll());
    }

    @Autowired
    public SubjectController(SubjectServiceImpl subjectServiceImpl) {
        this.subjectServiceImpl = subjectServiceImpl;
    }

    @GetMapping
    public ResponseEntity<SubjectDto> find(@RequestParam String id,
                                           @RequestParam String groupCode,
                                           @RequestParam int semester) {
        return ResponseEntity.ok(subjectServiceImpl.find(new SubjectIDDto(id, groupCode, semester)));
    }


    @PostMapping
    public ResponseEntity<SubjectDto> create(@RequestBody @Valid SubjectDto subjectDto) {
        return ResponseEntity.ok(subjectDto);
    }


    @DeleteMapping
    public ResponseEntity<String> delete(@RequestBody @Valid SubjectIDDto subjectIDDto) {
        subjectServiceImpl.delete(subjectIDDto);
        return ResponseEntity.ok("Success");
    }


    @PutMapping
    public ResponseEntity<SubjectDto> update(@RequestBody @Valid SubjectDto subjectDto) {
        return ResponseEntity.ok(subjectServiceImpl.update(subjectDto));
    }


}
