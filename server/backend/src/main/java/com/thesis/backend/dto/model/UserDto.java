package com.thesis.backend.dto.model;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.thesis.backend.model.Register;
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

    public UserDto(int id) {
        this.id = id;
    }

    private List<SubjectDto> subjects;
    private List<RoleDto> roles;
    private List<Register> registers;
    private List<SubjectDto> teachSubjects;
}
