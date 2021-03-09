package com.thesis.backend.dto.request;


import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
@AllArgsConstructor
@NoArgsConstructor
@JsonIgnoreProperties(ignoreUnknown = true)
public class SubjectRegister {
    private String semester;
    private String groupCode;
    private String subjectID;
    private String teacherID;
    private String startTime;
    private String endTime;
    private String deviceID;
}
