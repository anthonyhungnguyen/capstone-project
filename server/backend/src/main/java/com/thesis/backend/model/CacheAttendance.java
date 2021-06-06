package com.thesis.backend.model;


import lombok.*;

import java.io.Serializable;
import java.util.List;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
@ToString
public class CacheAttendance implements Serializable {
    private static final long serialVersionUID = 1L;
    private String classCode;
    private String startTime;
    private String endTime;
    private List<Integer> studentList;
    private List<Integer> studentHaveAttendances;
}
