package com.thesis.backend.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

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
    private int semester;

    @Field(value = "groupCode")
    private String groupCode;

    @Field(value = "subjectID")
    private String subjectID;

    @Field(value = "teacherID")
    private String teacherID;

    @Field(value = "timestamp")
    private String timestamp;

    @Field(value = "deviceID")
    private String deviceID;

    @Field(value = "imgSrcBase64")
    private String imgSrcBase64;
}
