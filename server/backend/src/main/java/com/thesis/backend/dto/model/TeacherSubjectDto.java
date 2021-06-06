package com.thesis.backend.dto.model;


import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@AllArgsConstructor
@NoArgsConstructor
@Builder
@Data
public class TeacherSubjectDto {
    private Integer userID;

    private String subjectID;

    private String groupCode;

    private Integer count;
}
