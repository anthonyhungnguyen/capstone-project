package com.thesis.backend.model;

import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.*;
import lombok.experimental.Accessors;

import javax.persistence.*;
import java.io.Serializable;
import java.util.List;

@Data
@Accessors(chain = true)
@Builder
@Entity
@AllArgsConstructor
@NoArgsConstructor
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

    private String name;

    @Column(name = "week_day")
    private int weekDay;

    @Column(name = "time_range")
    private String timeRange;

    private String room;

    private String base;

    @Column(name = "week_learn")
    private String weekLearn;

    @ManyToMany(targetEntity = User.class,
            mappedBy = "subjects", fetch = FetchType.LAZY)
    @ToString.Exclude
    @JsonIgnore
    private List<User> users;
}
