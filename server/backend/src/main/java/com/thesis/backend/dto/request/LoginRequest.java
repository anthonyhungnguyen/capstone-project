package com.thesis.backend.dto.request;

import lombok.Data;

@Data
public class LoginRequest {
    private String userid;
    private String password;
}
