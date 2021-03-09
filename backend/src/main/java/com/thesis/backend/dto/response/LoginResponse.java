package com.thesis.backend.dto.response;

import lombok.Data;

import java.util.List;

@Data
public class LoginResponse {
    public LoginResponse(String accessToken, Integer userid, List<String> roles) {
        this.accessToken = accessToken;
        this.userid = userid;
        this.roles = roles;
    }

    private String accessToken;
    private String tokenType = "Bearer";
    private Integer userid;
    private List<String> roles;
}
