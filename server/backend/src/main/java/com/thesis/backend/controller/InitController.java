package com.thesis.backend.controller;

import com.thesis.backend.service.InitService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;
import java.util.Map;

@CrossOrigin(origins = "*", maxAge = 3600)
@RestController
@RequestMapping(value = "/api/init")
public class InitController {
    private final InitService initService;

    @Autowired
    public InitController(InitService initService) {
        this.initService = initService;
    }

    @PostMapping("/register_full")
    public ResponseEntity<String> registerFull(@RequestBody Map<String, Object> requestData) throws IOException {
        return ResponseEntity.ok(initService.registerFull(requestData));
    }

    @GetMapping("/fill_register_image")
    public ResponseEntity<String> fillRegisterImage() {
        return ResponseEntity.ok(initService.initFillRegisterImages());
    }
}
