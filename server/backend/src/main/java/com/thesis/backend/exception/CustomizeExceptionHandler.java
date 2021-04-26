package com.thesis.backend.exception;

import com.thesis.backend.dto.response.ResponseError;
import com.thesis.backend.util.DateUtil;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.context.request.WebRequest;
import org.springframework.web.servlet.mvc.method.annotation.ResponseEntityExceptionHandler;

@ControllerAdvice
@RestController
public class CustomizeExceptionHandler extends ResponseEntityExceptionHandler {
    @ExceptionHandler(CustomException.EntityNotFoundException.class)
    public ResponseEntity<ResponseError> handleNotFoundException(Exception ex, WebRequest request) {
        ResponseError response = ResponseError.builder()
                .message(ex.getMessage())
                .timestamp(DateUtil.today())
                .details(request.getDescription(false))
                .build();
        return new ResponseEntity<>(response, HttpStatus.NOT_FOUND);
    }

    @ExceptionHandler(CustomException.DuplicateEntityException.class)
    public ResponseEntity<ResponseError> handleDuplicateException(Exception ex, WebRequest request) {
        ResponseError response = ResponseError.builder()
                .message(ex.getMessage())
                .timestamp(DateUtil.today())
                .details(request.getDescription(false))
                .build();
        return new ResponseEntity<>(response, HttpStatus.CONFLICT);
    }

    @ExceptionHandler(CustomException.TimeNotMatchException.class)
    public ResponseEntity<ResponseError> handleTimeNotMatchException(Exception ex, WebRequest request) {
        ResponseError response = ResponseError.builder()
                .message(ex.getMessage())
                .timestamp(DateUtil.today())
                .details(request.getDescription(false))
                .build();
        return new ResponseEntity<>(response, HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ResponseError> handleGlobalException(Exception ex, WebRequest request) {
        ResponseError responseError = ResponseError.builder()
                .message(ex.getMessage())
                .timestamp(DateUtil.today())
                .details(request.getDescription(false))
                .build();
        return new ResponseEntity<>(responseError, HttpStatus.INTERNAL_SERVER_ERROR);
    }
}
