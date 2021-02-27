package com.thesis.backend.controller;

import com.thesis.backend.model.Face;
import com.thesis.backend.service.FaceService;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;

@RestController
@RequestMapping(value = "/api/face", produces = MediaType.APPLICATION_JSON_VALUE)
@Tag(name = "Face controller")
@Slf4j
public class FaceController {
    private final FaceService faceService;

    @Autowired
    public FaceController(FaceService faceService) {
        this.faceService = faceService;
    }

    @GetMapping
    public ResponseEntity<List<Face>> getFaces(@RequestParam("username") Integer username) {
        return ResponseEntity.ok(faceService.findAllFacesByUserId(username));
    }

    @PostMapping
    public ResponseEntity<Boolean> saveCroppedPhoto(@RequestParam("username") Integer userid,
                                                    @RequestParam("image") MultipartFile multipartFile) throws IOException {
        return ResponseEntity.ok(faceService.saveFace(userid, multipartFile));
    }
}
