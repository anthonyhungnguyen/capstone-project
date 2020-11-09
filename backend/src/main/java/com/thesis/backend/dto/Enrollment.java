package com.thesis.backend.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.RequiredArgsConstructor;

import javax.persistence.*;

@AllArgsConstructor
@RequiredArgsConstructor
@Entity
@Data
@Table(name = "enrollment")
public class Enrollment {

    @Id
    @Column(name = "user_id")
    private int userId;

    @Id
    @Column(name = "subject_id")
    private String subjectId;

    @Id
    @Column(name ="group_code")
    private String groupCode;

    @Id
    private int semester;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id")
    private User user;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "subject_id")
    @JoinColumn(name = "group_code")
    @JoinColumn(name = "semester")
    private Subject subject;
}
