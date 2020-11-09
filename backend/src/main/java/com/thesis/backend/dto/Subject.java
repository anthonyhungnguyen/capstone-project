package com.thesis.backend.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.RequiredArgsConstructor;

import javax.persistence.*;
import javax.validation.constraints.NotBlank;
import java.util.List;

@AllArgsConstructor
@RequiredArgsConstructor
@Data
@Builder
@Entity
@Table(name = "subject")
public class Subject {

    @Id
    private String id;

    @Id
    @Column(name = "group_code")
    private String groupCode;

    @Id
    private int semester;
    //The string is not null and the trimmed length is greater than zero.
    @NotBlank(message = "Subject Name is required")
    private String name;

    @NotBlank(message = "Week Day is required")
    @Column(name = "week_day")
    private int weekDay;

    @NotBlank(message = "Time Range is required")
    @Column(name = "time_range")
    private String timeRange;

    private String room;

    private String base;

    @Column(name = "week_learn")
    private String weekLearn;

    @OneToMany(targetEntity = Enrollment.class, mappedBy = "subject", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<Enrollment> enrollmentList;
}
