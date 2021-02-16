package com.thesis.backend.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

import java.io.Serializable;

@Data
@Accessors(chain = true, fluent = true)
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class SubjectId implements Serializable {
    private String id;
    private String groupCode;
    private int semester;
}
