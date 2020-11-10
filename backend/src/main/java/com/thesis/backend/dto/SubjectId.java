package com.thesis.backend.dto;

import lombok.*;

import javax.persistence.Id;
import java.io.Serializable;


@Getter
@Setter
@Data
@AllArgsConstructor
@NoArgsConstructor
public class SubjectId implements Serializable {
    @Id
    private String id;
    @Id
    private String groupCode;
    @Id
    private int semester;
}
