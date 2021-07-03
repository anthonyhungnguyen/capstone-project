package com.thesis.backend.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/verify")
public class AuthVerifyController {
    @GetMapping
    public ResponseEntity<Boolean> verifyAuthorizedUser() {
        return ResponseEntity.ok(true);
    }
}
