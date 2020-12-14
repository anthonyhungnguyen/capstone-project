package com.thesis.backend.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import lombok.ToString;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

import java.time.LocalDateTime;
import java.time.ZoneId;

@Document(collection = "log")
@Data
@ToString
public class CheckLog {

    public CheckLog(int studentID, int semester, String groupCode, String subjectID, String type) {
        this.studentID = studentID;
        this.semester = semester;
        this.groupCode = groupCode;
        this.subjectID = subjectID;
        this.type = type;
    }

    @Field(value = "student_id")
    private int studentID;

    @Field(value = "semester")
    private int semester;

    @Field(value = "group_code")
    private String groupCode;

    @Field(value = "subject_id")
    private String subjectID;

    @Field(value = "type")
    private String type;

    @Field(value = "timestamp")
    private LocalDateTime timestamp = LocalDateTime.now(ZoneId.of("Asia/Ho_Chi_Minh"));
}
