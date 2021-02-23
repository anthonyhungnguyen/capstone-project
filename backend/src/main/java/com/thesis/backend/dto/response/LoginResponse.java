package com.thesis.backend.dto.response;

import lombok.Data;
import lombok.RequiredArgsConstructor;

import javax.validation.constraints.NotNull;

@Data
public class LoginResponse {
    public LoginResponse(String accessToken) {
        this.accessToken = accessToken;
    }

    private String accessToken;
    private String tokenType = "Bearer";
}
