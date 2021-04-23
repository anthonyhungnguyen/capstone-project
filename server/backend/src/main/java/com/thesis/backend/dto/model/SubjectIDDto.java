package com.thesis.backend.dto.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

import javax.validation.constraints.NotBlank;

@Data
@Builder
@Accessors(chain = true)
@AllArgsConstructor
@NoArgsConstructor
public class SubjectIDDto {
    @NotBlank
    private String id;
    @NotBlank
    private String groupCode;
    @NotBlank
    private int semester;
}
