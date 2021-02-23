package com.thesis.backend.dto.model;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

import java.util.List;

@Data
@Builder
@Accessors(chain = true)
@AllArgsConstructor
@NoArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonIgnoreProperties(ignoreUnknown = true)
public class UserDto {
    private int id;
    private String name;
    private int gender;
    private String majorCode;
    private String role;

    public UserDto(int id, String name, int gender, String majorCode, String role) {
        this.id = id;
        this.name = name;
        this.gender = gender;
        this.majorCode = majorCode;
        this.role = role;
    }

    private List<SubjectDto> subjectDtos;
}
