package com.thesis.backend.controller;


import com.thesis.backend.dto.model.UserDto;
import com.thesis.backend.service.UserServiceImpl;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;

@RestController(value = "User controller")
@RequestMapping(value = "/api/user", produces = MediaType.APPLICATION_JSON_VALUE)
@Tag(name = "User")
@Slf4j
public class UserController {
    private final UserServiceImpl userServiceImpl;

    @Autowired
    public UserController(UserServiceImpl userServiceImpl) {
        this.userServiceImpl = userServiceImpl;
    }

    @Operation(description = "Retrieve user based on id")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "Found"),
            @ApiResponse(responseCode = "404", description = "Not found")
    })
    @GetMapping
    public ResponseEntity<UserDto> get(@RequestParam(value = "id") Integer id) {
        return ResponseEntity.ok(userServiceImpl.find(id));
    }

    @Operation(description = "Create a user")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "Success"),
            @ApiResponse(responseCode = "400", description = "Already exists")
    })
    @PostMapping
    public ResponseEntity<UserDto> create(@Valid @RequestBody UserDto userDto) {
        return ResponseEntity.ok(userServiceImpl.create(userDto));
    }

    @Operation(description = "Delete existing user")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "Success"),
            @ApiResponse(responseCode = "404", description = "Not found")
    })
    @DeleteMapping
    public ResponseEntity<String> delete(@RequestParam(value = "id") int id) {
        userServiceImpl.delete(id);
        return ResponseEntity.ok("Success");
    }

    @Operation(description = "Update existing user")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "Success"),
            @ApiResponse(responseCode = "404", description = "Not found")
    })
    @PutMapping
    public ResponseEntity<UserDto> update(@RequestBody @Valid UserDto userDto) {
        return ResponseEntity.ok(userServiceImpl.update(userDto));
    }
}
