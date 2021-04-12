package com.thesis.backend.constant;

public enum ERole {
    STUDENT("student"),
    TEACHER("teacher"),
    ADMIN("admin");

    String value;

    ERole(String value) {
        this.value = value;
    }

    public String getValue() {
        return value;
    }
}
