package com.thesis.backend.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

import java.sql.Time;
import java.sql.Timestamp;
import java.time.LocalDateTime;

@Document(collection = "attendance_log")
@Data
@Builder
@Accessors(chain = true)
@AllArgsConstructor
@NoArgsConstructor
public class Log {
    @Field(value = "userId")
    private Integer userID;

    @Field(value = "semester")
    private Integer semester;

    @Field(value = "groupCode")
    private String groupCode;

    @Field(value = "subjectID")
    private String subjectID;

    @Field(value = "teacherID")
    private Integer teacherID;

    @Field(value = "timestamp")
    private LocalDateTime timestamp;

    @Field(value = "deviceID")
    private Integer deviceID;

    @Field(value = "imgSrcBase64")
    private String imgSrcBase64;
}
