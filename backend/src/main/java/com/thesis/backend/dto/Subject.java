package com.thesis.backend.dto;

import com.fasterxml.jackson.annotation.*;
import lombok.*;

import javax.persistence.*;
import javax.validation.constraints.NotBlank;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

@AllArgsConstructor
@RequiredArgsConstructor
@Builder
@Getter
@Setter
@Entity
@Table(name = "subject")
@IdClass(SubjectId.class)
public class Subject implements Serializable {

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

    @ManyToMany(mappedBy = "subjects", fetch = FetchType.LAZY)
    @JsonIgnore
    private List<User> users = new ArrayList<>();
}
