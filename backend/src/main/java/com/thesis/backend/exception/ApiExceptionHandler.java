package com.thesis.backend.exception;

import com.thesis.backend.dto.Message;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.time.LocalDateTime;
import java.time.ZoneId;

@RestControllerAdvice
public class ApiExceptionHandler {

    @ExceptionHandler(DataIntegrityViolationException.class)
    @ResponseStatus(value = HttpStatus.BAD_REQUEST)
    public Message handleDataIntegrityViolationException(DataIntegrityViolationException ex) {
        return new Message(false, ex.getMessage());
    }
}
