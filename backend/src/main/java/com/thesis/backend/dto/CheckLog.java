package com.thesis.backend.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

import java.time.LocalDateTime;

@Document(collection = "check_log")
@AllArgsConstructor
@RequiredArgsConstructor
@Data
public class CheckLog {
    @Id
    private String id;

    @Field(value = "student_id")
    private String studentID;

    @Field(value = "subject_id")
    private String subjectID;

    @Field(value = "type")
    private String type;

    @Field(value = "timestamp")
    private LocalDateTime timestamp = LocalDateTime.now();
}
