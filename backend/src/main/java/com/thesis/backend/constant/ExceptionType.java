package com.thesis.backend.constant;

public enum ExceptionType {
    ENTITY_NOT_FOUND("not.found"),
    DUPLICATE_ENTITY("duplicate"),
    ENTITY_EXCEPTION("exception"),
    TIME_NOT_MATCH("time.not.match");

    String value;

    ExceptionType(String value) {
        this.value = value;
    }

    public String getValue() {
        return value;
    }
}
