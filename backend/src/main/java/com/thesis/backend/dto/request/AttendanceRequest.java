package com.thesis.backend.dto.request;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

import java.sql.Timestamp;
import java.util.Hashtable;
import java.util.List;

@Data
@Accessors(chain = true)
@Builder
@AllArgsConstructor
@NoArgsConstructor
@JsonIgnoreProperties(ignoreUnknown = true)
@JsonInclude(JsonInclude.Include.NON_NULL)
public class AttendanceRequest {
    @JsonProperty("userID")
    private Integer userID;

    @JsonProperty("semester")
    private Integer semester;

    @JsonProperty("groupCode")
    private String groupCode;

    @JsonProperty("subjectID")
    private String subjectID;

    @JsonProperty("timestamp")
    private String timestamp;

    @JsonProperty("feature")
    private List<List<Float>> feature;

    @JsonProperty("deviceID")
    private Integer deviceID;

    @JsonProperty("imgSrcBase64")
    private String imgSrcBase64;

    @JsonProperty("teacherID")
    private Integer teacherID;

    @JsonProperty("isMatched")
    private Boolean isMatched;

}
