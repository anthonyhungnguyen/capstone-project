package com.thesis.backend.controller;

import com.thesis.backend.dto.request.LoginRequest;
import com.thesis.backend.dto.request.SignUpRequest;
import com.thesis.backend.dto.response.LoginResponse;
import com.thesis.backend.security.jwt.JwtUtils;
import com.thesis.backend.security.services.UserDetailsImpl;
import com.thesis.backend.service.UserServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import java.util.List;
import java.util.stream.Collectors;

@CrossOrigin(origins = "*", maxAge = 3600)
@RestController
@RequestMapping("/api/auth")
public class AuthController {
    private final AuthenticationManager authenticationManager;

    private final JwtUtils jwtUtils;

    private final UserServiceImpl userService;

    @Autowired
    public AuthController(AuthenticationManager authenticationManager, JwtUtils jwtUtils, UserServiceImpl userService) {
        this.authenticationManager = authenticationManager;
        this.jwtUtils = jwtUtils;
        this.userService = userService;
    }


    @PostMapping("/login")
    public ResponseEntity<LoginResponse> authenticateUser(@Valid @RequestBody LoginRequest loginRequest) {
        Authentication authentication = authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(
                        loginRequest.getUserid(),
                        loginRequest.getPassword()
                )
        );

        SecurityContextHolder.getContext().setAuthentication(authentication);
        String jwt = jwtUtils.generateJwtToken(authentication);

        UserDetailsImpl userDetails = (UserDetailsImpl) authentication.getPrincipal();
        List<String> roles = userDetails.getAuthorities().stream()
                .map(GrantedAuthority::getAuthority)
                .collect(Collectors.toList());

        return ResponseEntity.ok().body(new LoginResponse(jwt,
                userDetails.getUser().getId(),
                roles));
    }

    @PostMapping("/signup")
    public ResponseEntity<Boolean> register(@Valid @RequestBody SignUpRequest signUpRequest) {
        return ResponseEntity.ok(userService.register(signUpRequest));
    }
}
