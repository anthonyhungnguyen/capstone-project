package com.thesis.backend.dto.request;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
@JsonIgnoreProperties(ignoreUnknown = true)
@JsonInclude(JsonInclude.Include.NON_NULL)
public class AttendanceRequest {
    @JsonProperty("userID")
    private Integer userID;

    @JsonProperty("semester")
    private int semester;

    @JsonProperty("groupCode")
    private String groupCode;

    @JsonProperty("subjectID")
    private String subjectID;

    @JsonProperty("timestamp")
    private String timestamp;

    @JsonProperty("deviceID")
    private String deviceID;

    @JsonProperty("imgSrcBase64")
    private String imgSrcBase64;

    @JsonProperty("teacherID")
    private String teacherID;
}
