package com.thesis.backend.dto.request;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Builder;
import lombok.Data;
import lombok.experimental.Accessors;

import java.time.LocalDateTime;

@Data
@Builder
@Accessors(chain = true)
@JsonIgnoreProperties(ignoreUnknown = true)
public class ScheduleRequest {
    private Integer teacherID;
    private Integer deviceID;
    private String subjectID;
    private String groupCode;
    private int semester;
    private String startTime;
    private String endTime;
}
